import golly as g
from itertools import chain, product

def find_all_subpatterns(haystack, needle):
  if len(haystack) == 0 or len(needle) == 0:
    return []

  haystack = zip(haystack[::2], haystack[1::2])
  haystack_lookup = set(haystack)

  needle = zip(needle[::2], needle[1::2])
  p, q = needle[0]

  found_needles = []
  for x, y in haystack:
    needle_lookup = set()
    xmin, ymin, xmax, ymax = x, y, x, y
    for i, j in needle:
      xrel, yrel = x+i-p, y+j-q
      needle_lookup.add((xrel, yrel))
      if xrel < xmin:
        xmin = xrel
      if xrel > xmax:
        xmax = xrel
      if yrel < ymin:
        ymin = yrel
      if yrel > xmax:
        ymax = yrel

    spot = product(range(xmin-1, xmax+2), range(ymin-1, ymax+2))
    if all([ ((i, j) in haystack_lookup) is ((i, j) in needle_lookup) for i, j in spot ]):
      found_needles.append([coord for coord in chain(*needle_lookup)])

  return found_needles

TARGETS = dict([
  (3, [
    g.parse('3o$!'), # blinker
  ]),
  (4, [
    g.parse('2o$2o!'), # block
    g.parse('bo$obo$bo!'), # tub
  ]),
  (5, [
    g.parse('b2o$obo$bo!'), # boat
  ]),
  (6, [
    g.parse('b2o$o2bo$b2o!'), # hive
    g.parse('b2o$obo$2o!'), # ship
  ]),
  (7, [
    g.parse('b2o$o2bo$bobo$2bo!'), # loaf
    g.parse('2b2o$bobo$obo$bo!'), # long boat
  ]),
  (8, [
    g.parse('b2o$o2bo$o2bo$b2o!'), # pond
  ]),
  (12, [
    g.parse('2b3o2$o5bo$o5bo$o5bo2$2b3o!'), # traffic light
  ]),
  (24, [
    g.parse('6bo$5bobo$5bobo$6bo2$b2o7b2o$o2bo5bo2bo$b2o7b2o2$6bo$5bobo$5bobo$6bo!'), # honey farm
  ]),
])

MAX_POPULATION = 50
MAX_WEIGHT = 5

def get_pattern_variants(cells):
  variants = []
  for p in range(0, 2):
    for t in range(0, 4):
      if all([len(find_all_subpatterns(p, cells)) == 0 for p in variants]):
        variants.append(cells)
      cells = g.transform(cells, 0, 0, 0, -1, 1, 0)
    cells = g.evolve(cells, 1)
  return variants

def get_start_targets():
  ret = []
  for t in chain(*TARGETS.values()):
    ret.extend(chain(*[(v, g.transform(v, 1, 0)) for v in get_pattern_variants(t)]))
  return ret

g.new('')
i = 0
for p in get_start_targets():
  g.putcells(p, i, 0)
  i += 50

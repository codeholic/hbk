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
      elif xrel > xmax:
        xmax = xrel
      if yrel < ymin:
        ymin = yrel
      elif yrel > xmax:
        ymax = yrel

    spot = product(range(xmin-1, xmax+2), range(ymin-1, ymax+2))
    if all([ ((i, j) in haystack_lookup) is ((i, j) in needle_lookup) for i, j in spot ]):
      found_needles.append([coord for coord in chain(*needle_lookup)])

  return found_needles

TARGET_PATTERNS = [
  ('blinker', '3o$!', 4),
  ('block', '2o$2o!', 4),
  ('tub', 'bo$obo$bo!', 4),
  ('boat', 'b2o$obo$bo!', 1),
  ('hive', 'b2o$o2bo$b2o!', 2),
  ('ship', 'b2o$obo$2o!', 2),
  ('loaf', 'b2o$o2bo$bobo$2bo!', 1),
  ('lboat', '2b2o$bobo$obo$bo!', 1),
  ('pond', 'b2o$o2bo$o2bo$b2o!', 4),
  ('tlight', '4bo$4bo$4bo2$3o3b3o2$4bo$4bo$4bo!', 4),
  ('hfarm', '6bo$5bobo$5bobo$6bo2$b2o7b2o$o2bo5bo2bo$b2o7b2o2$6bo$5bobo$5bobo$6bo!', 4),
]

GLIDER = g.parse('3o$2bo$bo!')

MAX_POPULATION = 50
MAX_WEIGHT = 5
MAX_GLIDERS_PER_SCAN = 10
LANES = range(-38, 38, 2)

def get_pattern_bounding_box(cells):
  xmin, ymin, xmax, ymax = cells[0], cells[1], cells[0], cells[1]
  for x in cells[::2]:
    if x < xmin:
      xmin = x
    elif x > xmax:
      xmax = x
  for y in cells[1::2]:
    if y < ymin:
      ymin = y
    elif y > ymax:
      ymax = y
  return xmin, ymin, xmax, ymax

def center_pattern(cells):
  xmin, ymin, xmax, ymax = get_pattern_bounding_box(cells)
  return list(chain(*[(x - xmin, y - ymin) for x, y in zip(cells[::2], cells[1::2])]))

def get_pattern_variants(cells, symmetry):
  variants = []
  for t in range(0, 4, symmetry):
    variants.append(center_pattern(cells))
    cells = g.transform(cells, 0, 0, 0, -1, 1, 0)
  return variants

TARGETS = dict()
for name, pattern, symmetry in TARGET_PATTERNS:
  cells = g.parse(pattern)
  variants = get_pattern_variants(cells, symmetry)
  p = len(cells) / 2
  TARGETS.setdefault(p, {}).update(dict([(name + str(i), cells) for i, cells in zip(range(0, len(variants)), variants)]))

def patterns_identical(cells1, cells2):
  if len(cells1) != len(cells2):
    return False
  return set(zip(cells1[::2], cells1[1::2])) == set(zip(cells2[::2], cells2[1::2]))

def get_pattern_period(cells):
  temp_cells = cells
  for p in range(0, 2):
    temp_cells = evolve(temp_cells, 1)
    if patterns_identical(cells, temp_cells):
      return p+1
  return None

def get_lanes_to_try(cells):
  xmin, ymin, xmax, ymax = get_pattern_bounding_box(cells)
  minlane, maxlane = xmin + ymin - 6, xmax + ymax + 3
  return filter(lambda(lane): minlane <= lane <= maxlane, LANES)

def get_pattern_to_try(cells, lane, parity):
  glider = g.transform(GLIDER, lane - 25, 25)
  if parity % 2:
    glider = g.evolve(glider, 1)
  return list(chain(cells, glider))

g.new('')
i = 0
#for p in TARGETS:
#  g.putcells(p, i, 0)
#  i += 50

cells = TARGETS[24]['hfarm0']
for lane in get_lanes_to_try(cells):
  g.putcells(get_pattern_to_try(cells, lane, 0), i, 0)
  i += 50

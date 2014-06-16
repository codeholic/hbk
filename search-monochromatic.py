import golly as g

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
      needle_lookup.append((xrel, yrel))
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
      found_needles.append([item for point in needle_lookup for item in point])

  return found_needles

TARGETS = dict([
  (3, [
    ('blinker', g.parse('3o$!'), 2, 1),
  ]),
  (4, [
    ('block', g.parse('2o$2o!'), 1, 1),
    ('tub', g.parse('bo$obo$bo!'), 1, 1),
  ]),
  (5, [
    ('boat', g.parse('b2o$obo$bo!'), 1, 4)
  ]),
  (6, [
    ('hive', g.parse('b2o$o2bo$b2o!'), 1, 2),
    ('ship', g.parse('b2o$obo$2o!'), 1, 2),
  ]),
  (7, [
    ('loaf', g.parse('b2o$o2bo$bobo$2bo!'), 1, 4),
    ('long_boat', g.parse('2b2o$bobo$obo$bo!'), 1, 4),
  ]),
  (8, [
    ('pond', g.parse('b2o$o2bo$o2bo$b2o!'), 1, 1),
  ]),
  (12, [
    ('traffic_light', g.parse('2b3o2$o5bo$o5bo$o5bo2$2b3o!'), 2, 1),
  ]),
  (24, [
    ('honey_farm', g.parse('6bo$5bobo$5bobo$6bo2$b2o7b2o$o2bo5bo2bo$b2o7b2o2$6bo$5bobo$5bobo$6bo!'), 1, 1),
  ]),
])

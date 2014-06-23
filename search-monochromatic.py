import golly as g
from itertools import chain, product

def find_all_subpatterns(haystack, needle):
  if not haystack or not needle:
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
      elif yrel > ymax:
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

MAX_GENERATIONS = 400
MAX_POPULATION = 50
MAX_WEIGHT = 5
MAX_GLIDERS = 10
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

TARGETS = []
for name, pattern, symmetry in TARGET_PATTERNS:
  cells = g.parse(pattern)
  variants = get_pattern_variants(cells, symmetry)
  p = len(cells) / 2
  TARGETS.extend([(name + str(i), cells, p) for i, cells in zip(range(0, len(variants)), variants)])

def patterns_identical(cells1, cells2):
  if len(cells1) != len(cells2):
    return False
  return set(zip(cells1[::2], cells1[1::2])) == set(zip(cells2[::2], cells2[1::2]))

def get_pattern_period(cells):
  temp_cells = cells
  for p in range(0, 2):
    temp_cells = g.evolve(temp_cells, 1)
    if patterns_identical(cells, temp_cells):
      return p+1
  return None

def get_lanes_to_try(cells):
  xmin, ymin, xmax, ymax = get_pattern_bounding_box(cells)
  minlane, maxlane = xmin + ymin - 6, xmax + ymax + 3
  return filter(lambda(lane): minlane <= lane <= maxlane, LANES)

def get_pattern_to_try(cells, lane, parity, offset=50):
  glider = g.transform(GLIDER, lane - offset, offset)
  if parity % 2:
    glider = g.evolve(glider, 1)
  return list(chain(cells, glider))

def subtract(cells, sub):
  return list(chain(*(set(zip(cells[::2], cells[1::2])) ^ set(zip(sub[::2], sub[1::2])))))

g.new('')
#i = 0
#cells = [c for name, c, _ in TARGETS if name == 'hfarm0'][0]
#for lane in get_lanes_to_try(cells):
#  g.putcells(get_pattern_to_try(cells, lane, 0), i, 0)
#  i += 50

# start, lanes, last, period, weight, emitted = item
# name, x, y = start

def display_solution(start, lanes, weight, debug):
  name, x, y = start
  cells = g.transform([c for n, c, _ in TARGETS if n == name][0], x, y)
  i = 100
  for lane in lanes:
    lane_num, parity = lane
    cells = get_pattern_to_try(cells, lane_num, parity, i)
    i += 100
  g.new('')
  g.putcells(cells)
  for p, i in zip(debug, range(0, len(debug))):
    g.putcells(p, 100 + 100 * i, 0)
  g.fit()
  g.update()
  g.show(' '.join(chain([str(weight), str(start)], [str(lane) for lane in lanes])))
  while g.getkey() == '':
    pass
  g.show('')

queue = []
for name, cells, _ in TARGETS:
  period = get_pattern_period(cells)
  queue.append( ((name, 0, 0), [], cells, period, 0, False, []) )
  queue.append( ((name, 1, 0), [], g.transform(cells, 1, 0), period, 0, False, []) )

while len(queue):
  start, lanes, last, period, weight, emitted, debug = queue.pop(0)

  if lanes:
    pop = len(last) / 2
    candidates = [(name, c) for name, c, p in TARGETS if p == pop]
    found = False
    for name, c in candidates:
      for gen in range(0, period):
        needles = find_all_subpatterns(last, c)
        if needles:
          if emitted:
            display_solution(start, lanes, weight, debug)
          found = True
          break
      if found:
        break
    if found:
      continue

  if len(lanes) >= MAX_GLIDERS:
    continue

  last_lane = lanes[-1] if len(lanes) else (-40, 0) # TODO: start with other parity
  for lane_num in get_lanes_to_try(last):
    new_weight = weight
    parities = [weight + lane_num / 2 % 2] if period == 1 else [last_lane[1], last_lane[1]+1]
    for parity in parities:
      if lane_num > last_lane[0]:
        if period == 2 and (lane_num - last_lane[0]) / 2 % 2 != parity - last_lane[1]:
          new_weight += 1
      else:
        if period == 2 and (lane_num - last_lane[0]) / 2 % 2 == parity - last_lane[1]:
          new_weight += 2
        else:
          new_weight += 1

      if new_weight > MAX_WEIGHT:
        continue

      lane = (lane_num, parity)
      new_cells = get_pattern_to_try(last, lane[0], lane[1])
      new_debug = list(debug)
      new_debug.append(new_cells)
      new_cells = g.evolve(new_cells, MAX_GENERATIONS)
      if len(new_cells) > MAX_POPULATION:
        continue

      emitted_gliders = [0, 0, 0, 0]
      for gen in range(0, 4):
        for t in range(0, 4):
          for e in find_all_subpatterns(new_cells, GLIDER):
            new_cells = subtract(new_cells, e)
            emitted_gliders[t] += 1
          new_cells = g.transform(new_cells, 0, 0, 0, -1, 1, 0)
        new_cells = g.evolve(new_cells, 1)

      if not new_cells:
        continue

      if emitted_gliders[0] + emitted_gliders[2] > 0:
        continue

      new_emitted = None
      if emitted_gliders[1] + emitted_gliders[3] == 0:
        new_emitted = emitted
      elif emitted_gliders[1] + emitted_gliders[3] == 1:
        if emitted:
          continue
        else:
          new_emitted = True
      else:
        continue

      new_period = get_pattern_period(new_cells)
      if new_period is None:
        continue

      new_lanes = list(lanes)
      new_lanes.append(lane)
      queue.append( (start, new_lanes, new_cells, new_period, new_weight, new_emitted, new_debug) )

  queue.sort(lambda a, b: cmp(a[4], b[4]))

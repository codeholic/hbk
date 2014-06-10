import golly as g
from itertools import combinations, product

def get_invariants(cells):
  invariants = []

  for t in range(0, 4):
    gliders = []
    temp_cells = cells[:]

    for gen in range(0, 4):
      gliders.extend([coords + (gen,) for coords in find_all_gliders(temp_cells)])
      temp_cells = g.evolve(temp_cells, 1)

    glider_pairs = combinations(gliders, 2)
    invariants.extend([item for pair in glider_pairs for item in compute_invariants(pair)])

    cells = g.transform(cells, 0, 0, 0, -1, 1, 0)

  seen = set()
  return [ item for item in invariants if item not in seen and not seen.add(item) ]

def find_all_gliders(cells):
  gliders = []

  cells_dict = dict.fromkeys(zip(cells[::2], cells[1::2]))

  for x, y in zip(cells[::2], cells[1::2]):
    glider_dict = dict.fromkeys([(x, y), (x, y+2), (x+1, y+1), (x+1, y+2), (x+2, y+1)])

    spot = product(range(x-1, x+4), range(y-1, y+4))
    if all([ ((i, j) in cells_dict) is ((i, j) in glider_dict) for i, j in spot ]):
      gliders.append( (x, y) )

  return gliders

def compute_invariants(glider_pair):
  (x1, y1, t1), (x2, y2, t2) = glider_pair

  dx = x2 - x1
  dy = y2 - y1
  dt = t2 - t1

  hd = dx - dy
  tr = float(hd) / 2 * 47

  return [abs(dt - 4 * dy - tr), abs(4 * dx - dt - tr)]

invariants = get_invariants(g.getcells(g.getselrect()))
g.show(' '.join([str(item) for item in invariants]))

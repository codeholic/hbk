import golly as g
from itertools import product
import re

def find_all_gliders(cells):
  gliders = []

  cells_dict = dict.fromkeys(zip(cells[::2], cells[1::2]))

  for x, y in zip(cells[::2], cells[1::2]):
    glider_dict = dict.fromkeys([(x, y), (x, y+2), (x+1, y+1), (x+1, y+2), (x+2, y+1)])

    spot = product(range(x-1, x+4), range(y-1, y+4))
    if all([ ((i, j) in cells_dict) is ((i, j) in glider_dict) for i, j in spot ]):
      gliders.append( (x, y) )

  return gliders

def get_glider_color(glider):
  return (glider[0] % 2) == (glider[1] % 2)

filename = '/Users/ifomichev/work/gencols/hbsynth/hf.col'
infile = open(filename, 'r')
outfile = open(filename + '.out', 'w')

for line in infile:
  pattern, _, _, pattern_type = re.split('\s', line, 5)[:4]
  if pattern_type != 'other':
    continue

  pattern = re.sub('!', '.\n', pattern)

  cells = g.parse(pattern)

  gliders = []
  temp_cells = cells[:]
  for gen in range(0, 4):
    gliders.extend(find_all_gliders(temp_cells))
    temp_cells = g.evolve(temp_cells, 1)

  if len(gliders) < 2:
    continue

  sample = get_glider_color(gliders[0])
  if not all([get_glider_color(glider) == sample for glider in gliders[1:]]):
    continue

  # check that pattern emits exactly one orthogonal glider
  new_cells = g.evolve(cells, 700)
  emitted_gliders = []
  for t in range(0, 4):
    emitted_gliders.append(0)

    temp_cells = new_cells
    for gen in range(0, 4):
      emitted_gliders[-1] += len(find_all_gliders(temp_cells))
      temp_cells = g.evolve(temp_cells, 1)

    new_cells = g.transform(new_cells, 0, 0, 0, -1, 1, 0)

  if emitted_gliders[0] + emitted_gliders[2] == 0 and emitted_gliders[1] + emitted_gliders[3] == 1:
    outfile.write(line)

infile.close()
outfile.close()

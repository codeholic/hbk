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
  pattern = re.split('\s', line, 2)[0]
  pattern = re.sub('!', '.\n', pattern)

  gliders = []
  for gen in range(0, 4):
    gliders.extend(find_all_gliders(g.parse(pattern)))

  if len(gliders) < 2:
    continue

  sample = get_glider_color(gliders[0])
  if all([get_glider_color(glider) == sample for glider in gliders[1:]]):
    outfile.write(line)

infile.close()
outfile.close()

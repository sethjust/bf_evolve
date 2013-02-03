#!/usr/bin/env python

from random import choice
from bisect import insort

import oo_bf

prog_chars = list("<>+-[].")

class BF_Program:
  def __init__(self, length):
    self.program = ''.join([choice(prog_chars) for i in range(length)])

  def get_program(self):
    return self.program

  __repr__ = get_program

  def mutate(self, n=3):
    if (n<1): return self
    new = BF_Program(0)
    new.program = self.program

    i = choice(range(max(1, len(new.program))))
    act = choice([1, 2, 3])

    if (act == 1):
      # mutate
      new.program = new.program[:i] + choice(prog_chars) + new.program[i+1:]
    elif (act == 2):
      # insert
      new.program = new.program[:i] + choice(prog_chars) + new.program[i:]
    elif (act == 3):
      # delete
      new.program = new.program[:i] + new.program[i+1:]

    return new.mutate(n-1)

  def breed(self, other):
    new = BF_Program(0)

    i = choice(range(len(self.program)))
    j = choice(range(len(other.program)))
    act = choice([1,2])

    insert = choice(["", choice(prog_chars)])

    if (act == 1):
      # self first
      new.program = self.program[:i] + insert + other.program[j:]
    elif (act == 2):
      # other first
      new.program = self.program[:i] + insert + other.program[j:]

    return new.mutate(1)


class Evolver:
  def __init__(self, fitness, pop, prog_len):
    self.fitness = fitness
    self.pop = [BF_Program(prog_len) for i in range(pop)]

  def step(self):
    temp_pop = []

    for ind in self.pop:
      try:
        out = oo_bf.run(ind.get_program())
        fit = self.fitness(out)
        print fit, out
      except KeyboardInterrupt as ki:
        raise ki
      except:
        fit = 100000000
      # use the fact that tuples sort on the first key, because bisect doesn't
      # take a key argument
      insort(temp_pop, (fit, ind))

    print temp_pop
    best_fit = temp_pop[0][0]

    num_keepers = len(temp_pop)/2
    num_new = len(temp_pop) - num_keepers

    keepers = [ind for (fit, ind) in temp_pop[:num_keepers]]

    self.pop = [keep for keep in keepers]
    for i in range(num_new):
      keep = choice(keepers)
      act = choice([1,2])
      if (act == 1):
        new = keep.mutate()
        self.pop.append(new)
        print "Mutated", keep, "to", new
      elif (act == 2):
        other = choice(keepers)
        new = keep.breed(other)
        self.pop.append(new)
        print "Bred", keep, "and", other, "to", new

    return best_fit

if __name__ == '__main__':
  target = list("hello world!")
  evolver = Evolver(lambda x : sum([abs(ord(o)-ord(e)) for (o,e) in zip(x, target)]) if len(x) == len(target) else 10000*abs(len(x)-len(target)), 20, 20)

  generation = 0
  fit = 1000000
  while (fit > 10):
    print "------------------------------"
    fit = evolver.step()
    print "Generation:", generation
    generation += 1
    print "Best fitness is", fit


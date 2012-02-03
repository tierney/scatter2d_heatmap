#!/usr/bin/env python
#
# Copyright (c) 2012, NYU.
# All rights reserved.
#
# GPLv2 License.
#
# Plot 2D heatmap projection of data output from Matlab antenna simulations.
#
# Author: tierney@cs.nyu.edu (Matt Tierney)

import gflags
import sys
import numpy as np
import matplotlib.pyplot as plt


FLAGS = gflags.FLAGS
gflags.DEFINE_string('filename', '', 'Name of data file.',
                     short_name = 'f')
gflags.DEFINE_integer('dimension', 0, 'X and Y dimension.',
                      short_name = 'd')

gflags.RegisterValidator('filename', lambda value: value is not '',
                         message = 'Filename required.', flag_values = FLAGS)
gflags.RegisterValidator('dimension', lambda value: value > 0,
                         message = 'Positive dimension required.',
                         flag_values = FLAGS)


def parse_file(filename):
  '''We assume the data is laid out as "X Y Z\n" per line in the file.'''
  with open(filename,'r') as fh:
    lines = fh.readlines()

  lines = [line.strip().split() for line in lines]
  return lines


def plot_data_from_filename(filename):
  lines = parse_file(filename)
  matrix = np.zeros((FLAGS.dimension, FLAGS.dimension))

  # Convert the indices to being zero-indexed. Also, ensure types are correct.
  for x, y, z in lines:
    matrix[int(x)-1, int(y)-1] = float(z)

  # Make everything pretty.
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.imshow(matrix, origin='lower') # This could also be upper.
  fig.savefig(FLAGS.filename + '.png')
  plt.show()


def main(argv):
  try:
    argv = FLAGS(argv) # Parse flags.
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
    sys.exit(1)

  plot_data_from_filename(FLAGS.filename)

if __name__ == '__main__':
  main(sys.argv)

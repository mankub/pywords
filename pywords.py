#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__authors__ = ()
__license__ = 'Public Domain'
__version__ = '2012.04.27'

# system modules
import sys

# own project modules
from words import *
from quiz import *


# prints usage of script
def usage():
     print "pywords.py <filename>"

def main(argv):

     if len(argv) == 2:
          # get first argument
          path = argv[1]

          # read and parse input file
          Parser.readInput( path )
          Parser.process()

          # start quiz
          Quiz.start()

     else:
          usage()


# calls main if file is runned as a script
if __name__ == '__main__':
     main(sys.argv)


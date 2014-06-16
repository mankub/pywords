#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__authors__ = ()
__license__ = 'Public Domain'
__version__ = '2012.04.27'

# system modules
import sys

# own project modules
from words import *
from parser import *
from quiz import *
from console import *


class ObjectBroker:
     lc = None
     par = None
     con = None
     quiz = None

     def __init__( self ):
          self.lc = LanguageContainerReaderWriter.load()
          self.con = Console( self )
          self.par = Parser( self )
          self.quiz = Quiz( self )

     def getParser( self ):
          return self.par

     def getConsole( self ):
          return self.con

     def getLanguageContainer( self ):
          return self.lc

     def getQuiz( self ):
          return self.quiz



def main(argv):
     ob = ObjectBroker()

     ob.getConsole().main_loop()

     LanguageContainerReaderWriter.save( ob.getLanguageContainer() )


# calls main if file is runned as a script
if __name__ == '__main__':
     main(sys.argv)


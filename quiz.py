#!/usr/bin/env python
# -*- coding: latin2 -*-

__authors__ = ()
__license__ = 'Public Domain'
__version__ = '2012.04.27'

from words import *
import random

class Quiz():

     lang_from = None
     lang_to = None

     """
     Dumb quiz class
     """

     def _green_str( self, str1 ):
          return "\033[1;32m\033[40m" + str1 + "\033[0m"

     def _red_str( self, str1 ):
          return "\033[1;31m\033[40m" + str1 + "\033[0m"

     def __init__( self, ob ):
          self._ob = ob

     def start( self, lang_from_str, lang_to_str ):
          space = "   "
          lc = self._ob.getLanguageContainer()

          lang_from = lc.get( lang_from_str )
          lang_to = lc.get( lang_to_str )

          print ""
          print lang_from.getName() + " -> " + lang_to.getName()
          print ""

          from_list = lang_from.getWords()
          rand_list = random.sample( range( len(from_list) ), len(from_list) )
          good = 0
          total = 0

          for word_num in rand_list:
               word = from_list[ word_num ]

               try:
                    answ = raw_input( space + word + "? " )
               except:
                    break

               ww = lang_from.getWord( word )

               if len( answ ) > 0 and ww.isTranslation( answ ):
                    good += 1
                    print space + self._green_str( "good" ) + "\n"
               else:
                    print space + self._red_str("wrong") + "\n"
                    for tr in  ww.getTranslations():
                         print space + "  + " + tr
               print
               total += 1

          print ""
          print good, " / ", total
          print ""



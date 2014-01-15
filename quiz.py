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

     def __init__( self ): pass

     @staticmethod
     def start():
          space = "   "

          print "<< quiz >>\n"

          langs = Languages.getAllNames()
          print langs

          lang_str = raw_input( "select question language: " )
          Quiz.lang_from = Languages.get( lang_str )
          lang_str = raw_input( "select answer language: " )
          Quiz.lang_to = Languages.get( lang_str )

          assert Quiz.lang_from != Quiz.lang_to, "very bad.."

          print "\n" + Quiz.lang_from.getName() + " -> " + Quiz.lang_to.getName() + "\n"

          from_list = Quiz.lang_from.getWords()
          rand_list = random.sample( range( len(from_list) ), len(from_list) )
          good = 0

          for word_num in rand_list:
               word = from_list[ word_num ]
               answ = raw_input( space + word + "? " )
               ww = Quiz.lang_from.getWord( word )

               if len( answ ) > 0 and ww.isTranslation( answ ):
                    good += 1
                    print space + "\033[1;32m\033[40m" + "good" + "\033[0m"
               else:
                    print space + "\033[1;31m\033[40m" + "wrong" + "\033[0m" + "\n"
                    for tr in  ww.getTranslations():
                         print space + "  + " + tr
               print

          print '\n', good, " / ", len( rand_list ), '\n'



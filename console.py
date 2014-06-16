#!/usr/bin/env python
# -*- coding: latin2 -*-

__authors__ = ()
__license__ = 'Public Domain'
__version__ = '2014.06.05'

import sys

class Console():

     _sign = None
     _commands = None
     _ob = None

     _quit = False

     def __init__( self, object_broker ):
          self._sign = "pywords> "
          self._commands = {
               "quiz"      : ( self.quiz, "quiz operations" ), 
               "dict"      : ( self.dict, "language operations" ), 
               "container" : ( self.container, "container operations" ), 
               "help"      : ( self.help, "prints this help message" ), 
               "quit"      : ( self.exit, "" ) 
          }
          self._ob = object_broker

     def main_loop( self ):

          while not self._quit:
               try:
                    str = raw_input( self._sign )
               except EOFError, err:
                    self.exit()
                    continue

               args = str.split()

               if len(args) > 0 and self._commands.has_key( args[0] ):
                    self._commands[ args[0] ][0]( args[1:] )
               else:
                    pass


     def quiz( self, args = None ):
          help_msg = \
"""
quiz start <A> <B>           - starts quiz with direction A to B
quiz help                   - print this message
"""
          if len(args) == 0 or args[0] == "help":
               print help_msg
          elif args[0] == "start":

               if len(args) != 3:
                    print "error: too few parameters"
                    return None

               if args[1] == args[2]:
                    print "error: cannot start quiz on the same dictionary"
                    return None

               lc = self._ob.getLanguageContainer()
               
               if lc.get( args[1] ) == None or lc.get( args[2] ) == None:
                    print "error: no such dictionary in container"
                    return None

               quiz = self._ob.getQuiz()
               try:
                    quiz.start( args[1], args[2] )
               except:
                    print "error: "

          else:
               print "Unknown command"
               print help_msg
               

     def dict( self, args = None ):
          help_msg = \
"""
dict list <lang>            - list words from <lang>
dict del  <lang> <word>     - list words from <lang>
dict help                   - print this message
"""
          if len(args) == 0 or args[0] == "help":
               print help_msg

          elif args[0] == "list":
               if len(args) != 2:
                    print "error: please provide dictionary name"
                    return None

               lc = self._ob.getLanguageContainer()
               try:
                    dt = lc.get( args[1] )
               except:
                    print "error: no such dictionary"
                    return None
               
               print ""
               print "Languages:"
               for name in dt.getWords():
                    print "+", name
               print ""
               
          elif args[0] == "del":
               if len(args) != 3:
                    print "error: please provide dictionary name and word"
                    return None

               lc = self._ob.getLanguageContainer()
               dt = None
               try:
                    dt = lc.get( args[1] )
               except:
                    print "error: no such dictionary"
                    return None

               try:
                    dt.delWord( args[2] )
               except:
                    print "error: no such word"
                    return None
               
               
          else:
               print "Unknown command"
               print help_msg
               

     def container( self, args = None ):
          help_msg = \
"""
container import <filename> - import translations from <filename>
container list              - list stored languages
container del <dict>        - list stored languages
container info              - print info about container
container help              - print this message
"""
          lc = self._ob.getLanguageContainer()

          if len(args) == 0 or args[0] == "help":
               print help_msg

          elif args[0] == "import":
               if len(args) != 2:
                    print "error: please provide filename"
                    return None

               parser = self._ob.getParser()
               parser.readInput( args[1] )
               parser.process()
               parser.clear()

          elif args[0] == "info":
               print ""
               print "filename : ", lc.name
               print "stored languages : ", len( lc.getAll() )
               print ""

          elif args[0] == "list":
               print ""
               print "Languages:"
               for name in lc.getAllNames():
                    print "+", name
               print ""

          elif args[0] == "del":
               if len(args) != 2:
                    print "error: please provide dictionary name"
                    return None
               try:
                    lc.rem( args[1] )
               except:
                    print "error: Not found such dictionary"

          else:
               print "Unknown command"
               print help_msg


     def help( self, args = None ):
          print ""
          for command in self._commands.keys():
               print command, "-", self._commands[ command ][1]
          print ""
          print "For most commands you can type <command> help, for more information"
          print ""


     def exit( self, args = None ):
          self._quit = True


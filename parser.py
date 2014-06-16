#!/usr/bin/env python
# -*- coding: latin2 -*-

__authors__ = ()
__license__ = 'Public Domain'
__version__ = '2012.04.27'

from words import *


class Parser:

     """
     Parser class ... ?
     """

     _content = ""
     _atoms = []

     _dict_from = None
     _dict_to = None

     # LanguageContainer
     _lc = None

     class ParserError(Exception): pass

     # dictionary with operators and their actions
     _operators = [ ",", "->", ":", ";" ]

     def _preprocess ( self ):

          """
          procedure prepares content before _atomize.
          """

          for operator in Parser._operators:
               self._content = self._content.replace( operator, " " + operator + " " )

     def _atomize ( self ):

          """
          transform _content into _atoms list with operators and operands
          """

          stack=[]
          atoms=[]

          for fraction in self._content.split():
               if fraction in Parser._operators:
                    opnd = " ".join(stack)
                    if opnd != "":
                         self._atoms.append( opnd ) 
                    self._atoms.append( fraction )
                    stack=[]
               else:
                    stack.append( fraction )

          opnd = " ".join(stack)
          if opnd != "":
               self._atoms.append( opnd ) 

     def _reduce( self ):

          """
          reduce ';' and ':' in '->X:'
          """

          i = 1
          while i < len( self._atoms ):
               # -> X : to -> X
               if self._atoms[i] == ':' and self._atoms[i-2] == '->':
                    self._atoms.pop(i)
                    continue
               elif self._atoms[i] == ';':
                    self._atoms.pop(i)
                    continue
               i += 1

     def _concat( self ):

          """
          concantantate a , b , c into one atom [a,b,c] list
          """

          i = 1
          while i < len( self._atoms ):
               if self._atoms[i] == ',':
                    if isinstance( self._atoms[i-1], list ):
                         self._atoms[i-1].append( self._atoms[i+1] )
                    else:
                         self._atoms[i-1] = [ self._atoms[i-1], self._atoms[i+1] ]
                    self._atoms.pop(i+1)
                    self._atoms.pop(i)
               else:
                    i += 1
                         
     def _interpret( self ):

          """
          interpret remaining atoms.
          """

          i = 1
          while i < len( self._atoms ):
               if self._atoms[i] == '->':

                    langto = self._atoms.pop(i+1)
                    self._atoms.pop(i)
                    langfrom = self._atoms.pop(i-1)

                    if not self._lc.isLang( langto ):
                         self._dict_to = self._lc.add( langto )
                    else:
                         self._dict_to = self._lc.get( langto )

                    if not self._lc.isLang( langfrom ):
                         self._dict_from = self._lc.add( langfrom )
                    else:
                         self._dict_from = self._lc.get( langfrom )

                    continue

               elif self._atoms[i] == ':':

                    if self._dict_from == None or self._dict_to == None:
                         raise ParserError("Translation languages not set.")

                    wordto = self._atoms.pop(i+1)
                    self._atoms.pop(i)
                    wordfrom = self._atoms.pop(i-1)

                    wf = None; wt = None

                    if not self._dict_from.isWord( wordfrom ):
                         wf = self._dict_from.addWord( wordfrom )
                    else:
                         wf = self._dict_from.getWord( wordfrom )
                         print wf, "already in dictionary"

                    if not isinstance( wordto, list ):
                         wordto = [ wordto ]
                         
                    for w in wordto:
                         if not self._dict_to.isWord( w ):
                              wt = self._dict_to.addWord( w )
                         else:
                              wt = self._dict_to.getWord( w )
                              print wt, "already in dictionary"
                         
                         try:
                              Dictionary.bind(wf, wt)
                         except:
                              print "translation", wf, "->", wt, "already exist"

                    continue

               i += 1

     # public:

     def __init__ ( self, object_broker ):
          self._lc = object_broker.getLanguageContainer()

     def readInput( self, path ):

          """
          procedure reads content from path and prepare content
          for further processing. path can be path to file or -
          to read from stdin
          """

          # try to open path or read from stdin
          try:
               if path == '-':
                    fd = sys.stdin
               else:
                    fd = open(path)

          except IOError, err:
               sys.exit("error: unable to open file")

          # read lines
          try:
               for line in fd:
                    # ommit comments
                    if line[0] == '#':
                         continue

                    # remove indents and newline
                    clear_line = line.strip()

                    # ommit empty lines
                    if len(clear_line) == 0:
                         continue

                    # add semicolon on line end, if not already there
                    if not clear_line.endswith(";"):
                         clear_line += ";"

                    self._content += clear_line.lower()
          finally:
               fd.close()

     def getContent( self ): return self._content

     def setContent( self, content ): self._content = content

     def getAtoms( self ): return self._atoms

     def process( self ):
          self._preprocess()  # add spaces on left and right side of operators
          self._atomize()     # build atom list from content string
          self._reduce()      # remove exceeding operators
          self._concat()      # join listed comma separated atoms into list of atoms
          self._interpret()   # interpret remaining content, build dictionaries

     def clear( self ):
          self._content = ""


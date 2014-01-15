#!/usr/bin/env python
# -*- coding: latin2 -*-

__authors__ = ()
__license__ = 'Public Domain'
__version__ = '2012.04.27'


class Word(str):

     """
     Word class describing word entity,
     relations and actions
     """

     trans = None        # list of translations
     dictionary = None   # dictionary of this word

     # class Exceptions
     class NotAWordError(Exception): pass
     class WordExistError(Exception): pass
     class NoSuchWordError(Exception): pass

     def __init__( self, word ):
          str.__init__( self, word )
          self.trans = list()

     def isTranslation( self, word ):
          if self.trans.count( word ) > 0:
               return True
          else:
               return False

     def addTranslation( self, word ):
          if not isinstance( word, Word ):
               raise NotAWordError("Argument must be Word.")

          if not self.isTranslation( word ):
               self.trans.append( word )
          else:
               raise WordExistError("Word already in translations.")

     def getTranslations( self ):
          return self.trans

     def setDictionary( self, dictionary ):
          self.dictionary = dictionary

     def getDictionary( self ):
          return self.dictionary

     def printAll( self ):
          for t in self.trans:
               print "    " + t


class Dictionary:

     """
     Dictionary class aggregating words from
     language
     """

     name = None    # language name
     words = None   # words in language

     def __init__( self, name ):
          self.name = name
          self.words = list()

     def getName( self ):
          return self.name

     def isWord( self, word ):
          if self.words.count( word ) > 0:
               return True
          else:
               return False

     def addWord( self, word ):
          if not self.isWord( word ):
               w = Word( word )
               w.setDictionary( self )
               self.words.append( w )
               return w
          else:
               raise Word.WordExistError("Word already in dictionary.")

     def getWord( self, word ):
          if self.isWord( word ):
               return self.words[ self.words.index( word ) ]
          else:
               raise Word.NoSuchWordError("No such Word in dictionary.")

     def getWords( self ):
          return self.words

     def printAll( self ):
          for w in self.words:
               print "  " + w + ":"
               w.printAll()

     @staticmethod
     def bind( word1, word2 ):
          word1.addTranslation( word2 )
          word2.addTranslation( word1 )


class Languages:

     """
     Languages static class encapsules dictionaries
     of languages and acitons
     """

     _langs = []    # list with dictionaries

     class LangExistError (Exception): pass
     class NoSuchLangError (Exception): pass

     @staticmethod
     def isLang( name ):
          for lang in Languages._langs:
               if lang.getName() == name:
                    return True
          else:
               return False

     @staticmethod
     def add( name ):
          if not Languages.isLang( name ):
               d = Dictionary( name )
               Languages._langs.append( d )
               return d
          else:
               raise LangExistError("Language already exists.")
               
     @staticmethod
     def get( name ):
          for lang in Languages._langs:
               if lang.getName() == name:
                    return lang
          else:
               raise NoSuchLangError("No such Language.")
          
     @staticmethod
     def getAll():
          return Languages._langs

     @staticmethod
     def getAllNames():
          return [ l.getName() for l in Languages._langs ]

     @staticmethod
     def printAll():
          for l in Languages._langs:
               print l.getName()
               l.printAll()


class Parser:

     """
     Parser class ... ?
     """

     _content = ""
     _atoms = []

     _dict_from = None
     _dict_to = None

     class ParserError(Exception): pass

     # dictionary with operators and their actions
     _operators = [ ",", "->", ":", ";" ]

     @staticmethod
     def _preprocess ():

          """
          procedure prepares content before _atomize.
          """

          for operator in Parser._operators:
               Parser._content = Parser._content.replace( operator, " " + operator + " " )

     @staticmethod
     def _atomize ():

          """
          transform _content into _atoms list with operators and operands
          """

          stack=[]
          atoms=[]

          for fraction in Parser._content.split():
               if fraction in Parser._operators:
                    opnd = " ".join(stack)
                    if opnd != "":
                         Parser._atoms.append( opnd ) 
                    Parser._atoms.append( fraction )
                    stack=[]
               else:
                    stack.append( fraction )

          opnd = " ".join(stack)
          if opnd != "":
               Parser._atoms.append( opnd ) 

     @staticmethod
     def _reduce():

          """
          reduce ';' and ':' in '->X:'
          """

          i = 1
          while i < len( Parser._atoms ):
               # -> X : to -> X
               if Parser._atoms[i] == ':' and Parser._atoms[i-2] == '->':
                    Parser._atoms.pop(i)
                    continue
               elif Parser._atoms[i] == ';':
                    Parser._atoms.pop(i)
                    continue
               i += 1

     @staticmethod
     def _concat():

          """
          concantantate a , b , c into one atom [a,b,c] list
          """

          i = 1
          while i < len( Parser._atoms ):
               if Parser._atoms[i] == ',':
                    if isinstance( Parser._atoms[i-1], list ):
                         Parser._atoms[i-1].append( Parser._atoms[i+1] )
                    else:
                         Parser._atoms[i-1] = [ Parser._atoms[i-1], Parser._atoms[i+1] ]
                    Parser._atoms.pop(i+1)
                    Parser._atoms.pop(i)
               else:
                    i += 1
                         
     @staticmethod
     def _interpret():

          """
          interpret remaining atoms.
          """

          i = 1
          while i < len( Parser._atoms ):
               if Parser._atoms[i] == '->':

                    langto = Parser._atoms.pop(i+1)
                    Parser._atoms.pop(i)
                    langfrom = Parser._atoms.pop(i-1)

                    if not Languages.isLang( langto ):
                         Parser._dict_to = Languages.add( langto )
                    else:
                         Parser._dict_to = Languages.get( langto )

                    if not Languages.isLang( langfrom ):
                         Parser._dict_from = Languages.add( langfrom )
                    else:
                         Parser._dict_from = Languages.get( langfrom )

                    continue

               elif Parser._atoms[i] == ':':

                    if Parser._dict_from == None or Parser._dict_to == None:
                         raise ParserError("Translation languages not set.")

                    wordto = Parser._atoms.pop(i+1)
                    Parser._atoms.pop(i)
                    wordfrom = Parser._atoms.pop(i-1)

                    wf = None; wt = None

                    if not Parser._dict_from.isWord( wordfrom ):
                         wf = Parser._dict_from.addWord( wordfrom )
                    else:
                         wf = Parser._dict_from.getWord( wordfrom )

                    if not isinstance( wordto, list ):
                         wordto = [ wordto ]
                         
                    for w in wordto:
                         if not Parser._dict_to.isWord( w ):
                              wt = Parser._dict_to.addWord( w )
                         else:
                              wt = Parser._dict_to.getWord( w )

                         Dictionary.bind(wf, wt)

                    continue

               i += 1

     # public:

     @staticmethod
     def readInput( path ):

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

                    Parser._content += clear_line.lower()
          finally:
               fd.close()

     @staticmethod
     def getContent(): return Parser._content

     @staticmethod
     def setContent( content ): Parser._content = content

     @staticmethod
     def getAtoms(): return Parser._atoms

     @staticmethod
     def process():
          Parser._preprocess()  # add spaces on left and right side of operators
          Parser._atomize()     # build atom list from content string
          Parser._reduce()      # remove exceeding operators
          Parser._concat()      # join listed comma separated atoms into list of atoms
          Parser._interpret()   # interpret remaining content, build dictionaries




#!/usr/bin/env python
# -*- coding: latin2 -*-

__authors__ = ()
__license__ = 'Public Domain'
__version__ = '2012.04.27'

import os
import pickle

class Word(str):

     """
     Word class describing word entity,
     relations and actions
     """

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
               raise Word.NotAWordError("Argument must be Word.")

          if not self.isTranslation( word ):
               self.trans.append( word )
          else:
               raise Word.WordExistError("Word already in translations.")

     def delTranslation( self, word ):
          if not isinstance( word, Word ):
               raise Word.NotAWordError("Argument must be Word.")

          if self.isTranslation( word ):
               self.trans.remove( word )
          else:
               raise Word.NoSuchWordError("Cannot remove. Word not found in translations.")

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
               raise Word.WordExistError("word already in dictionary.")

     def delWord( self, word ):
          ww = self.getWord( word )

          for word_trans in ww.trans:
               word_trans.delTranslation( ww )

          self.words.remove( ww )

     def getWord( self, word ):
          if self.isWord( word ):
               return self.words[ self.words.index( word ) ]
          else:
               raise Word.NoSuchWordError("no such Word in dictionary.")

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

     @staticmethod
     def unbind( word1, word2 ):
          word1.delTranslation( word2 )
          word2.delTranslation( word1 )


class LanguageContainer:

     """
     LanguageContainer class encapsules dictionaries
     of languages and actions
     """

     class LangExistError (Exception): pass
     class NoSuchLangError (Exception): pass

     def isLang( self, name ):
          for lang in self.langs:
               if lang.getName() == name:
                    return True
          else:
               return False

     def add( self, name ):
          if not self.isLang( name ):
               d = Dictionary( name )
               self.langs.append( d )
               return d
          else:
               raise LangExistError("Language already exists.")
               
     def rem( self, name ):
          dd = self.get( name )

          for word in dd.getWords():
               dd.delWord( word )
     
          self.langs.remove( dd )
               
     def get( self, name ):
          for lang in self.langs:
               if lang.getName() == name:
                    return lang
          else:
               raise NoSuchLangError("No such Language.")
          
     def getAll( self ):
          return self.langs

     def getAllNames( self ):
          return [ l.getName() for l in self.langs ]

     def printAll( self ):
          for l in self.langs:
               print l.getName()
               l.printAll()

     def __init__( self ):
          self.langs = list()


class LanguageContainerReaderWriter:

     """
     LanguageContainerReaderWriter class for saving and reading LanguageContainer
     """

     _default_lc_path = ".languagecontainer.pywords"

     @staticmethod
     def load( path = _default_lc_path ):

          if not os.access( path, os.F_OK | os.R_OK ):
               os.mknod( path )

          lc = None
          fd = None

          try:
               fd = open( path, "rb" )
               lc = pickle.load( fd )
               
          except IOError, err:
               print("error: unable to open " + path)
          except EOFError, err:
               lc = LanguageContainer()

          if fd != None:
               fd.close()

          lc.name = path

          return lc

     @staticmethod
     def save( lc, path = _default_lc_path ):

          if not os.access( path, os.F_OK | os.W_OK ):
               print("error: container file does not exist")

          try:
               fd = open( path, "wb" )
               pickle.dump( lc, fd, pickle.HIGHEST_PROTOCOL )
               
          except IOError, err:
               print("error: unable to open file")

          if fd != None:
               fd.close()



################################################################################
#
# Copyright (c) 2005, Rocky Burt <rocky@serverzen.com>, and the respective
# authors. All rights reserved.  For a list of Archetypes contributors see
# docs/CREDITS.txt.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the author nor the names of its contributors may be used
#   to endorse or promote products derived from this software without specific
#   prior written permission.
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
################################################################################

"""
"""
__author__ = 'Rocky Burt'

__all__ = ('getSkinPaths', 'setSkinPaths', 'addSkinPaths',
           'removeSkinPaths', 'installPathsFromDir',)

import os.path

from Products.CMFCore.utils import getToolByName, minimalpath
from Products.Archetypes import types_globals
from Globals import package_home

from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.DirectoryView import manage_listAvailableDirectories

class _SkinManager:
    """Functionality for manipulating skins and skin paths mostly consisting
    of working with SkinsTool (portal_skins).
    """

    def getSkinPaths(self, context, skinName=None):
        """Returns all of the elements of a path for the named skin in the
        form of a tuple.  If no skinName is requested, then all skins are
        returned as a dict keyed by skin name with tuples as values.

        >>> len(getSkinPaths(portal)) >= 0
        True
        >>> len(getSkinPaths(portal, 'Nouvelle')) >= 0
        True
        """
        
        result = None

        skinsTool = getToolByName(context, 'portal_skins')
        if skinName:
            result = tuple(self._getPathList(skinsTool, skinName))
        else:
            result = {}
            for skinName in skinsTool.getSkinSelections():
                result[skinName] = tuple(self._getPathList(skinsTool, skinName))
                
        return result

    def setSkinPaths(self, context, paths, skinName=None):
        """Sets the path for the named skin.  The paths type should be one of
        list, tuple, or string.  If the paths type is string, all elements
        should be separated by a comma (ie "abc, def, ghi").


        Set the new paths for all skins to the elements contained within
        testing.
        >>> testing = ['abc', 'def']
        >>> originalPaths = getSkinPaths(portal)
        >>> firstSkin = originalPaths.keys()[0]
        >>> setSkinPaths(portal, testing)
        >>> newPaths = getSkinPaths(portal)
        >>> newPaths[firstSkin][0] == testing[0]
        True
        >>> newPaths[firstSkin][1] == testing[1]
        True

        Set the new paths for all skins to the value 'onemore'.
        >>> setSkinPaths(portal, 'onemore', 'Nouvelle')
        >>> newPaths = getSkinPaths(portal, 'Nouvelle')
        >>> len(newPaths) == 1 and newPaths[0] == 'onemore'
        True
        """
        
        skinsTool = getToolByName(context, 'portal_skins')

        if skinName:
            skinNames = (skinName,)
        else:
            skinNames = skinsTool.getSkinSelections()
            
        for skinName in skinNames:
            if isinstance(paths, list) or isinstance(paths, tuple):
                skinsTool.addSkinSelection(skinName, ','.join(paths))
            else:
                skinsTool.addSkinSelection(skinName, str(paths))

    def addSkinPaths(self, context, paths, skinName=None, position=None):
        """Adds the specified paths to the named skin.  The paths type should
        be one of list, tuple, or string.  If the paths type is string,
        all elements should be separated by a comma (ie "abc, def, ghi").  The
        position parameter can be used to specify an ordered position within the
        existing path to add the new path items.  The position parameter can
        be of type int or string.  If the position is of type int, then an index
        position is used, otherwise, the string is used as the key representing
        an existing path element name, in which case the items are inserted
        before the found item.  If no position is specified then the items
        get appended to the end.


        Add all path elements in testing to all skins (will be appended to the
        end).
        >>> originalPaths = getSkinPaths(portal)
        >>> firstSkin = originalPaths.keys()[0]
        >>> testing = ['abc', 'def']
        >>> addSkinPaths(portal, testing)
        >>> newPaths = getSkinPaths(portal)
        >>> newPaths[firstSkin][-1] == testing[1]
        True
        >>> newPaths[firstSkin][-2] == testing[0]
        True

        Insert all path elements in testing to all skins at the very beginning
        of their paths.
        >>> testing = ['ghi', 'jkl']
        >>> addSkinPaths(portal, testing, position=0)
        >>> newPaths = getSkinPaths(portal)
        >>> newPaths[firstSkin][0] == testing[0]        
        True
        >>> newPaths[firstSkin][1] == testing[1]
        True

        Insert all path elements in testing at the position starting at 2, which
        would be following the elements inserted from the previous example.
        >>> testing = ['aaaa', 'bbbb']
        >>> addSkinPaths(portal, testing, position=2)
        >>> newPaths = getSkinPaths(portal)
        >>> newPaths[firstSkin][2] == testing[0]
        True
        >>> newPaths[firstSkin][3] == testing[1]
        True
        """
        
        skinsTool = getToolByName(context, 'portal_skins')

        if skinName:
            skinNames = (skinName,)
        else:
            skinNames = skinsTool.getSkinSelections()
            
        for skinName in skinNames:
            if isinstance(paths, list) or isinstance(paths, tuple):
                pathsToAdd = paths
            else:
                pathsToAdd = [i.strip() for i in paths.split(',')]
        
            newPaths = self._getPathList(skinsTool, skinName)
            pos = None
            if position == None:
                newPaths.extend(pathsToAdd)
            elif isinstance(position, str):
                try:
                    pos = newPaths.index(position)
                except ValueError:
                    pass
            elif isinstance(position, int):
                pos = position

            if pos is not None:
                for x in range(len(pathsToAdd)):
                    newPaths.insert(pos+x, pathsToAdd[x])

            self.setSkinPaths(context, newPaths, skinName)

    def removeSkinPaths(self, context, paths, skinName=None):
        """Removes the specified paths from the named skin.  The paths type
        should be one of list, tuple, or string.  If the paths type is string,
        all elements should be separated by a comma (ie "abc, def, ghi").  If
        paths is of type list or tuple then the individual elements can be
        either string's or int's.  If an individual element is an int then
        it represents a path index to be removed.  If the element is a string
        then it represents an item to be searched for and then removed.  If the
        element cannot be found, nothing happens.


        Try removing two items specified by one string and one index
        position.
        >>> setSkinPaths(portal, ['one', 'two', 'three'], 'Nouvelle')
        >>> removeSkinPaths(portal, ['two', 2], 'Nouvelle')
        >>> getSkinPaths(portal, 'Nouvelle')
        ('one',)
       
        Try removing two elements by specifying one string with the names
        separated by a comma.
        >>> setSkinPaths(portal, ['one', 'two', 'three', 'four'], 'Nouvelle')
        >>> removeSkinPaths(portal, 'three,one', 'Nouvelle')
        >>> getSkinPaths(portal, 'Nouvelle')
        ('two', 'four')
        
        Try removing two elements by specifying one string with the names
        separated by a comma.  One of the elements will silently be ignored
        because it does not exist.
        >>> setSkinPaths(portal, ['one', 'two', 'three', 'four'])
        >>> removeSkinPaths(portal, 'three,nothere')
        >>> getSkinPaths(portal, 'Nouvelle')
        ('one', 'two', 'four')
        
        """

        skinsTool = getToolByName(context, 'portal_skins')

        if skinName:
            skinNames = (skinName,)
        else:
            skinNames = skinsTool.getSkinSelections()
            
        for skinName in skinNames:
            if isinstance(paths, list) or isinstance(paths, tuple):
                pathsToRemove = paths
            else:
                pathsToRemove = [i.strip() for i in paths.split(',')]

            currentPaths = self.getSkinPaths(context, skinName)
            newPaths = list(currentPaths)
            for x in pathsToRemove:
                if isinstance(x, int):
                    newPaths[x] = None
                elif isinstance(x, str):
                    try:
                        pos = newPaths.index(x)
                        newPaths[pos] = None
                    except ValueError:
                        pass

            done = False
            x = 0
            while x < len(newPaths):
                if newPaths[x] == None:
                    del newPaths[x]
                    x = 0
                else:
                    x = x + 1
                
            self.setSkinPaths(context, newPaths, skinName)

    def installPathsFromDir(self, context, dirPath,
                            paths=None, skinNames=None, position=None,
                            globals=types_globals):
        """Adds all subdirectories found at dirPath as paths.  The paths type
        should be one of list, tuple, or string.  If the paths type is string,
        all elements should be separated by a comma (ie "abc, def, ghi").  The
        position parameter can be used to specify an ordered position within the
        existing path to add the new path items.  The position parameter can
        be of type int or string.  If the position is of type int, then an index
        position is used, otherwise, the string is used as the key representing
        an existing path element name, in which case the items are inserted
        before the found item.  If no position is specified then the items
        get appended to the end.

        >>> setSkinPaths(portal, 'oneentry')
        >>> getSkinPaths(portal, 'Nouvelle')
        ('oneentry',)
        >>> installPathsFromDir(portal, portal, 'input/skins')
        >>> getSkinPaths(portal, 'Nouvelle')
        ('oneentry', 'skinpath1', 'skinpath2',)
        """

        skinsTool = getToolByName(context, 'portal_skins')

        absPath = os.path.join(package_home(globals), dirPath)
        relDirPath = minimalpath(absPath)

        registered_directories = manage_listAvailableDirectories()
        if relDirPath not in registered_directories:
            try:
                registerDirectory(dirPath, globals)
            except OSError, ex:
                if ex.errno == 2: # No such file or directory
                    return
                raise
        
        try:
            addDirectoryViews(skinsTool, dirPath, globals)
        except BadRequestException, e:
            pass  # directory view has already been added
        
        
        pass
    

    def _getPathList(self, skinsTool, skinName):
        path = skinsTool.getSkinPath(skinName)
        return [i.strip() for i in path.split(',')]

_skinManager = _SkinManager()

getSkinPaths = _skinManager.getSkinPaths
setSkinPaths = _skinManager.setSkinPaths
addSkinPaths = _skinManager.addSkinPaths
removeSkinPaths = _skinManager.removeSkinPaths
installPathsFromDir = _skinManager.installPathsFromDir

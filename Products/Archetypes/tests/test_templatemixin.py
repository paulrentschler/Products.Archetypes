# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2002-2005, Benjamin Saller <bcsaller@ideasuite.com>, and
#                              the respective authors. All rights reserved.
# For a list of Archetypes contributors see docs/CREDITS.txt.
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

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase

from zope.component import getUtility

from Products.Archetypes.atapi import *
from Products.Archetypes.config import TOOL_NAME
from Products.Archetypes.interfaces import IArchetypeTool
from Products.Archetypes.tests.atsitetestcase import ATSiteTestCase
from Products.Archetypes.TemplateMixin import TemplateMixin


class TemplateMixinTest(ATSiteTestCase):

    def test_isTemplateEnabled(self):
        at = getUtility(IArchetypeTool)
        self.failUnless(at.isTemplateEnabled(TemplateMixin))

    def test_isTemplateEnabledType(self):
        at = getUtility(IArchetypeTool)
        self.failUnless(at.isTemplateEnabled(dict(klass=TemplateMixin)))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TemplateMixinTest))
    return suite

if __name__ == '__main__':
    framework()
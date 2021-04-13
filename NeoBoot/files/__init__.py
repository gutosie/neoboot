# -*- coding: utf-8 -*-

from __future__ import print_function
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import os
import gettext
PluginLanguageDomain = 'NeoBoot'
PluginLanguagePath = 'Extensions/NeoBoot/locale'


def localeInit():
    lang = language.getLanguage()[:2]
    os.environ['LANGUAGE'] = lang
    print("[NeoBoot] set language to "), lang
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        print("[NeoBoot] fallback to default translation for"), txt
        t = gettext.dgettext('enigma2', txt)
    return t


localeInit()
language.addCallback(localeInit)

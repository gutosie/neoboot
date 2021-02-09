# -*- coding: utf-8 -*-
# system modules
 
from __future__ import print_function
#from Plugins.Extensions.NeoBoot.__init__ import _  
import codecs
from enigma import getDesktop
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.ConfigList import ConfigListScreen
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, NoSave
from Plugins.Extensions.NeoBoot.plugin import Plugins, PLUGINVERSION, UPDATEVERSION
from Plugins.Plugin import PluginDescriptor
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, fileExists, pathExists, createDir, fileCheck
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
from enigma import eTimer
from Plugins.Extensions.NeoBoot.files.stbbranding import getNeoLocation, getImageNeoBoot, getKernelVersionString, getBoxHostName, getCPUtype, getBoxVuModel, getTunerModel, getCPUSoC, getImageATv 
import os
import time
import sys
import struct, shutil
if fileExists('/etc/vtiversion.info') or fileExists('/usr/lib/python3.8') and fileExists('/.multinfo'):   
    from Screens.Console import Console                   
else:
    from Plugins.Extensions.NeoBoot.files.neoconsole import Console
LinkNeoBoot = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'                                              

class ForceReboot(Screen):
    __module__ = __name__
    skin = """<screen name="TunerInfo" title="NeoBoot - Sat Tuners " position="center,center" size="700,300" flags="wfNoBorder">
        <widget name="lab1" position="20,20" size="660,210" font="baslk;25" halign="center" valign="center" transparent="1" />
        <ePixmap position="200,250" size="34,34" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red.png" alphatest="blend" zPosition="1" />
        <widget name="key_red" position="250,250" zPosition="2" size="280,35" font="baslk;30" halign="left" valign="center" backgroundColor="red" transparent="1" foregroundColor="red" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('Force reboot to flash ?'))
        self['key_red'] = Label(_('To reboot press red!'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.iNFO})
         
    def iNFO(self):
        try:
            cmd = "echo -e '\n\n%s '" % _('Please wait, NeoBoot is working...')
            cmd1 = 'chmod 0755 ' + LinkNeoBoot + '/files/mountpoint.sh'
            cmd2 = '' + LinkNeoBoot + '/files/mountpoint.sh'
            cmd3 = "echo -e '\n\n%s '" % _('NeoBoot: Force reboot to flash image now...')            
            cmd4 = 'sleep 8; reboot -dfhi'            
            self.session.open(Console, _('NeoBoot: Backu to flash!'), [cmd,
             cmd1,
             cmd2,
             cmd3,             
             cmd4])
            out = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'w' )
            out.write('Flash')
            out.close()            
            self.close()

        except:
            False

def main(session, **kwargs):
        try:
            session.open(ForceReboot)
        except:
            False


def startSetup(menuid):
    if menuid != 'setup':
        return []
    return [(_('NeoReboot'),
      main,
      'NeoReboot',
      50)]

def Plugins(path, **kwargs):
    global plugin_path
    plugin_path = path
    list = [PluginDescriptor(name=_('NeoReboot'), description=_('Force reboot to flash.'), where=PluginDescriptor.WHERE_MENU, fnc=startSetup)]
    return list   
    
            
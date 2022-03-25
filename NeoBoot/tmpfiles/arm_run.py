# -*- coding: utf-8 -*-

#from __init__ import _
from Plugins.Extensions.NeoBoot.__init__ import _
from Plugins.Extensions.NeoBoot.files.stbbranding import getSupportedTuners, getCPUtype, getCPUSoC, getImageNeoBoot, getBoxHostName, getTunerModel, getNeoLocation, getNeoMount, getNeoMount2, getNeoMount3, getNeoMount4, getNeoMount5, getMountPointNeo2
from enigma import getDesktop
from enigma import eTimer
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Components.About import about
from Screens.Console import Console
from Components.Sources.List import List
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
import os
import time
LinkNeoBoot = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'


class StartImage(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center, center" size="1241, 850" title="NeoBoot">
        \n\t\t\t<ePixmap position="399,590" zPosition="-2" size="452,214" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />
        <widget source="list" render="Listbox" position="20, 171" size="1194, 290" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
        \n                    \t\t\t],
        \n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}
        \n            \t\t</convert>\n\t\t</widget>
        \n         <widget name="label1" position="21, 29" zPosition="1" size="1184, 116" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        <widget name="label2" position="22, 480" zPosition="-2" size="1205,101" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        </screen>"""
    else:
        skin = """<screen position="center, center" size="835, 500" title="NeoBoot">
        \n\t\t\t           <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />
        <widget source="list" render="Listbox" position="16, 150" size="800, 40"    selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/listselection800x35.png" scrollbarMode="showOnDemand">
        \n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (180, 0), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
        \n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],
        \n                    \t\t\t"itemHeight": 35\n               \t\t}\n            \t\t</convert>
        \n\t\t</widget>\n<widget name="label1" font="Regular; 26" position="15, 70" size="803, 58" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        <widget name="label2" position="40, 232" zPosition="2" size="806, 294" font="Regular;25" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        \n\t\t        </screen>"""

    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.select()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})
        self['label1'] = Label(_('Start the chosen system now ?'))
        self['label2'] = Label(_('Select OK to run the image.'))

    def select(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('OK Start image...'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        if getImageNeoBoot() != 'Flash':
                os.system('rm -rf %sImageBoot/%s/usr/bin/enigma2_pre_start.sh' % (getNeoLocation(), getImageNeoBoot()))
                self.StartImageInNeoBoot()
        else:
            os.system('rm -rf %sImageBoot/%s/usr/bin/enigma2_pre_start.sh' % (getNeoLocation(), getImageNeoBoot()))
            self.StartImageInNeoBoot()

        #---------------------------------------------
        getMountPointNeo2()
        system('touch /tmp/.init_reboot')
        #---------------------------------------------

    def StartImageInNeoBoot(self):
        if getImageNeoBoot() != 'Flash':
            if fileExists('%sImageBoot/%s/.control_ok' % (getNeoLocation(), getImageNeoBoot())):
                system('touch /tmp/.control_ok ')
            else:
                system('touch %sImageBoot/%s/.control_boot_new_image ' % (getNeoLocation(), getImageNeoBoot()))
        if fileExists('/.multinfo') and getCPUtype() == 'ARMv7':
                os.system(' ' + LinkNeoBoot + '/files/findsk.sh; mkdir -p /media/InternalFlash; mount /tmp/root /media/InternalFlash; sleep 1')

        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            if not fileExists('/bin/busybox.nosuid'):
                os.system('ln -sf "busybox" "/bin/busybox.nosuid" ')
            if fileExists('/media/InternalFlash/etc/init.d/neomountboot.sh'):
                os.system('rm -f /media/InternalFlash/etc/init.d/neomountboot.sh;')
            if fileExists('/media/InternalFlash/linuxrootfs1/etc/init.d/neomountboot.sh'):
                os.system('rm -f /media/InternalFlash/linuxrootfs1/etc/init.d/neomountboot.sh;')
            if fileExists('/media/InternalFlash/linuxrootfs2/etc/init.d/neomountboot.sh'):
                os.system('rm -f /media/InternalFlash/linuxrootfs2/etc/init.d/neomountboot.sh;')
            if fileExists('/media/InternalFlash/linuxrootfs3/etc/init.d/neomountboot.sh'):
                os.system('rm -f /media/InternalFlash/linuxrootfs3/etc/init.d/neomountboot.sh;')
            if fileExists('/media/InternalFlash/linuxrootfs4/etc/init.d/neomountboot.sh'):
                os.system('rm -f /media/InternalFlash/linuxrootfs4/etc/init.d/neomountboot.sh;')
#            else:
#                pass
            #_____ARM procesor____
            if (getSupportedTuners()):
                        if getImageNeoBoot() == 'Flash':
                            if fileExists('/.multinfo'):                    
                                if fileExists('/media/InternalFlash/linuxrootfs1/sbin/neoinitarm'):
                                        os.system('ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs1/sbin/init"')
                                if fileExists('/media/InternalFlash/linuxrootfs2/sbin/neoinitarm'):
                                        os.system('ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs2/sbin/init"')
                                if fileExists('/media/InternalFlash/linuxrootfs3/sbin/neoinitarm'):
                                        os.system('ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs3/sbin/init"')
                                if fileExists('/media/InternalFlash/linuxrootfs4/sbin/neoinitarm'):
                                        os.system('ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs4/sbin/init"')
                                if fileExists('/media/InternalFlash/sbin/init'):
                                        os.system('ln -sfn "init.sysvinit" "/media/InternalFlash/sbin/init"')
                                if fileExists('/media/InternalFlash'):
                                        self.session.open(TryQuitMainloop, 2)
                                else:
                                        self.session.open(TryQuitMainloop, 2)
                            elif not fileExists('/.multinfo'):
                                cmd = 'ln -sfn /sbin/init.sysvinit /sbin/init'
                                rc = os.system(cmd)
                                self.session.open(TryQuitMainloop, 2)
                            else:
                                cmd = 'ln -sfn /sbin/init.sysvinit /sbin/init'
                                rc = os.system(cmd)
                                self.session.open(TryQuitMainloop, 2)
                        elif getImageNeoBoot() != 'Flash':
                            if fileExists('/.multinfo'):
                                if fileExists('/media/InternalFlash/linuxrootfs1/sbin/neoinitarm'):
                                        cmd = 'cd /media/InternalFlash/linuxrootfs1; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs1/sbin/init'
                                        rc = os.system(cmd)
                                        self.session.open(TryQuitMainloop, 2)
                                elif fileExists('/media/InternalFlash/linuxrootfs2/sbin/neoinitarm'):
                                        cmd = 'cd /media/InternalFlash/linuxrootfs2; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs2/sbin/init'
                                        rc = os.system(cmd)
                                        self.session.open(TryQuitMainloop, 2)
                                elif fileExists('/media/InternalFlash/linuxrootfs3/sbin/neoinitarm'):
                                        cmd = 'cd /media/InternalFlash/linuxrootfs3; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs3/sbin/init'
                                        rc = os.system(cmd)
                                        self.session.open(TryQuitMainloop, 2)
                                elif fileExists('/media/InternalFlash/linuxrootfs4/sbin/neoinitarm'):
                                        cmd = 'cd /media/InternalFlash/linuxrootfs4; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs4/sbin/init'
                                        rc = os.system(cmd)
                                        self.session.open(TryQuitMainloop, 2)
                                else:                            
                                    self.session.open(TryQuitMainloop, 2) 
                            elif not fileExists('/.multinfo'):
                                cmd = 'ln -sfn /sbin/neoinitarm /sbin/init'
                                rc = os.system(cmd)
                                self.session.open(TryQuitMainloop, 2)
                            else:
                                cmd = 'ln -sfn /sbin/init.sysvinit /sbin/init'
                                rc = os.system(cmd)
                                self.session.open(TryQuitMainloop, 2)
                        else:
                            os.system('echo "Flash "  >> ' + getNeoLocation() + 'ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('It looks like it that multiboot does not support this STB.'), MessageBox.TYPE_INFO, 8)
                            self.close()

            else:
                            os.system('echo "Flash "  >> ' + getNeoLocation() + 'ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('It looks like it that multiboot does not support this STB.'), MessageBox.TYPE_INFO, 8)
                            self.close()
                            

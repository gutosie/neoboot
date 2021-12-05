# -*- coding: utf-8 -*-

#from __init__ import _
from Plugins.Extensions.NeoBoot.__init__ import _
from Plugins.Extensions.NeoBoot.files.stbbranding import getNeoLocation, getCPUtype, getCPUSoC, getImageNeoBoot, getBoxVuModel, getBoxHostName, getNeoMount, getNeoMount2, getNeoMount3, getNeoMount4, getNeoMount5, getMountPointNeo2
from enigma import getDesktop
from enigma import eTimer
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Screens.Console import Console
from Components.About import about
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
        skin = """<screen position="center,center" size="1241,885" title="NeoBoot">
        \n\t\t\t<ePixmap position="450,410" zPosition="-2" size="537,303" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />
        <eLabel position="33,801" size="1180,3" backgroundColor="red" foregroundColor="blue" name="linia" />
        <widget source="list" render="Listbox" position="20, 171" size="1194,141" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_CENTER|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
        \n                    \t\t\t],
        \n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}
        \n            \t\t</convert>\n\t\t</widget>
        \n         <widget name="label1" position="21, 29" zPosition="1" size="1184, 116" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        <widget name="label2" position="15,347" zPosition="-2" size="1205,60" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
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
        mypath = '' + LinkNeoBoot + ''
        if not fileExists(mypath + 'icons'):
            mypixmap = '' + LinkNeoBoot + '/images/ok.png'
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
        #---------------------------------------------')

    def StartImageInNeoBoot(self):
        if getImageNeoBoot() != 'Flash':
            if fileExists('%sImageBoot/%s/.control_ok' % (getNeoLocation(), getImageNeoBoot())):
                system('touch /tmp/.control_ok ')
            else:
                system('touch %sImageBoot/%s/.control_boot_new_image ' % (getNeoLocation(), getImageNeoBoot()))

        if fileExists('/.multinfo') and getCPUtype() == 'ARMv7':
                if getBoxVuModel() == 'duo4kse':
                    os.system('mkdir -p /media/InternalFlash; mount /dev/mmcblk0p9 /media/InternalFlash')

        system('chmod 755 ' + LinkNeoBoot + '/files/kernel.sh')
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            if fileExists('/media/InternalFlash/etc/init.d/neobootmount.sh'):
                os.system('rm -f /media/InternalFlash/etc/init.d/neobootmount.sh;')
            if not fileExists('/bin/busybox.nosuid'):
                os.system('ln -sf "busybox" "/bin/busybox.nosuid" ')
#################_____ARM____##########################

            #VUPLUS ARM - Duo4kse vu_mmcblk0p6.sh
            if getCPUSoC() == '7444s' or getBoxHostName() == 'vuduo4kse' and getBoxHostName() != 'vuultimo4k':
                        if not fileExists('%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName())):
                            mess = (_('Error - in the location %sImagesUpload/.kernel/ \nkernel file not found flash-kernel-%s.bin') % (getNeoLocation(), getBoxHostName()))
                            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                        else:
                            if getImageNeoBoot() == 'Flash':
                                if fileExists('/.multinfo'):
                                    cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT - REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')
                                    cmd1 = 'cd /media/InternalFlash; ln -sf "init.sysvinit" "/media/InternalFlash/sbin/init"; ' + LinkNeoBoot + '/files/kernel.sh '

                                elif not fileExists('/.multinfo'):
                                    cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT - REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')
                                    cmd1 = 'sleep 5; ln -sf "init.sysvinit" "/sbin/init"; reboot -dfhi'

                            elif getImageNeoBoot() != 'Flash':
                                if not fileExists('/.multinfo'):
                                    if not fileExists('%sImageBoot/%s/boot/zImage.%s' % (getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT - REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')
                                        cmd1 = 'sleep 5; ln -sfn /sbin/neoinitarm /sbin/init; /etc/init.d/reboot'

                                    elif fileExists('%sImageBoot/%s/boot/zImage.%s' % (getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT - REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')
                                        cmd1 = 'ln -sfn /sbin/neoinitarmvu /sbin/init; ' + LinkNeoBoot + '/files/kernel.sh '

                                elif fileExists('/.multinfo'):
                                    if not fileExists('%sImageBoot/%s/boot/zImage.%s' % (getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT - REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')
                                        cmd1 = 'dd if=' + getNeoLocation() + 'ImagesUpload/.kernel/flash-kernel-' + getBoxHostName() + '.bin of=/dev/mmcblk0p6; cd /media/InternalFlash; ln -sf "neoinitarm" "/media/InternalFlash/sbin/init" ; sleep 2; reboot -dfhi '

                                    elif fileExists('%sImageBoot/%s/boot/zImage.%s' % (getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('...............NEOBOOT - REBOOT...............\nPlease wait, in a moment the decoder will be restarted...')
                                        cmd1 = 'cd /media/InternalFlash; ln -sf "neoinitarmvu" "/media/InternalFlash/sbin/init"; ' + LinkNeoBoot + '/files/kernel.sh '

                            self.session.open(Console, _('NeoBoot ARM '), [cmd, cmd1])
                            self.close()

            else:
                            os.system('echo "Flash "  >> ' + getNeoLocation() + 'ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('It looks like it that multiboot does not support this STB.'), MessageBox.TYPE_INFO, 8)
                            self.close()

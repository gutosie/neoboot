# -*- coding: utf-8 -*-

from Plugins.Extensions.NeoBoot.__init__ import _
from enigma import getDesktop
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from enigma import eTimer
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
from Components.ConfigList import ConfigListScreen
from Components.config import getConfigListEntry, config, ConfigSelection, NoSave, configfile
from Components.Console import Console
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Extensions.NeoBoot.files.Harddisk import Harddisk
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, resolveFilename, SCOPE_CURRENT_SKIN
from os import system, rename, path, mkdir, remove, listdir
from time import sleep
import re
import os
from Screens.VirtualKeyBoard import VirtualKeyBoard
import gettext
from Plugins.Extensions.NeoBoot.files.stbbranding import getTunerModel, getCheckExt, getBoxHostName, getMyUUID
if not fileExists('/usr/lib/python2.7'):
    open = file
    getoutput = "os.system"    
else:
    from commands import getoutput
LinkNeoBoot = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'

class ManagerDevice(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:

        skin = """<screen name="ManagerDevice" position="400,150" size="1235,748">
            <widget name="key_red" position="14,17" zPosition="1" size="271,49" font="dugme;30" halign="center" valign="center" backgroundColor="red" transparent="1"   foregroundColor="red" />
            <widget name="key_green" position="289,17" zPosition="1" size="369,49" font="dugme;30" halign="center" valign="center" backgroundColor="green" transparent="1"   foregroundColor="green" />
            <widget name="key_yellow" position="661,17" zPosition="1" size="302,49" font="dugme;30" halign="center" valign="center" backgroundColor="yellow" transparent="1"   foregroundColor="yellow" />
            <widget name="key_blue" position="967,17" zPosition="1" size="257,49" font="dugme;30" halign="center" valign="center" backgroundColor="blue" transparent="1"   foregroundColor="blue" />
            <eLabel position="18,70" size="1204,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
            <eLabel position="18,670" size="1204,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
            <eLabel backgroundColor="black" font="dugme; 30" foregroundColor="orange" position="536,674" size="197,56" text="Exit - Back" transparent="1" />
            <widget source="list" render="Listbox" position="14,137" size="1210,530" scrollbarMode="showOnDemand">
            <convert type="TemplatedMultiContent">\n\n\t\t\t\t{"template": [\n\n\t\t\t\t MultiContentEntryText(pos = (90, 5), size = (600, 75), font=0, text = 0),\n\n\t\t\t\t MultiContentEntryText(pos = (110, 60), size = (900, 80), font=1, flags = RT_VALIGN_TOP, text = 1),\n\n\t\t\t\t MultiContentEntryPixmapAlphaBlend(pos = (0, 0), size = (150, 130,)),\n\n\t\t\t\t],\n\t\t\t\t"fonts": [gFont("Regular", 33),gFont("Regular", 33)],\n\n\t\t\t\t"itemHeight": 140\n\t\t\t\t}</convert>
            </widget>
            <widget name="lab1" zPosition="2" position="28,163" size="1182,69" font="baslk;30" halign="center" transparent="1" />
            </screen>"""
    else:
        skin = """<screen name="ManagerDevice" position="center,center" size="752,460">
        <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="orange" position="315,405" size="169,51" text="Exit - Back" transparent="1" />
        <widget name="key_red" position="21,0" zPosition="1" size="151,47" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" foregroundColor="red" />
        <widget name="key_green" position="216,0" zPosition="1" size="140,47" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" foregroundColor="green" />
        <widget name="key_yellow" position="400,0" zPosition="1" size="140,47" font="Regular;20" halign="center" valign="center" backgroundColor="yellow" transparent="1" foregroundColor="yellow" />
        <widget name="key_blue" position="587,0" zPosition="1" size="149,46" font="Regular;20" halign="center" valign="center" backgroundColor="blue" transparent="1" foregroundColor="blue" />
        <widget source="list" render="Listbox" position="18,63" size="721,341" scrollbarMode="showOnDemand">
        <convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t MultiContentEntryText(pos = (90, 0), size = (600, 30), font=0, text = 0),\n\t\t\t\t MultiContentEntryText(pos = (110, 30), size = (600, 50), font=1, flags = RT_VALIGN_TOP, text = 1),\n\t\t\t\t MultiContentEntryPixmapAlphaBlend(pos = (0, 0), size = (80, 80)),\n\t\t\t\t],\n\t\t\t\t"fonts": [gFont("Regular", 24),gFont("Regular", 20)],\n\t\t\t\t"itemHeight": 85\n\t\t\t\t}\n\t\t\t</convert>
        </widget>
        <widget name="lab1" zPosition="2" position="29,111" size="699,40" font="Regular;22" halign="center" transparent="1" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        Screen.setTitle(self, _('Mount Manager'))
        self['key_red'] = Label(_('Initialize ext3'))
        self['key_green'] = Label(_('Mounts UUID'))
        self['key_yellow'] = Label(_('Initialize ext4'))
        self['key_blue'] = Label(_('Formatting Disk'))
        self['lab1'] = Label()
        self.onChangedEntry = []
        self.list = []
        self['list'] = List(self.list)
        self['list'].onSelectionChanged.append(self.selectionChanged)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'MenuActions'], {'back': self.close,
         'red': self.Format_ext3,
         'green': self.SetupMounts,
         'yellow': self.Format_ext4,
         'blue': self.InitializationNeoB,
         'back': self.close})
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateList2)
        self.updateList()
        self.onShown.append(self.setWindowTitle)

    def Format_ext3(self):
        try:
            if fileExists('/etc/vtiversion.info') or fileExists('/etc/bhversion'):
                self.session.open(MessageBox, _("This option is available only from openpli or derivatives."), MessageBox.TYPE_INFO, timeout=10)
            else:
                from Harddisk import HarddiskSelection
                self.session.openWithCallback(self.updateList, HarddiskSelection)
        except:
            self.session.open(MessageBox, _("This option is available only from openpli or derivatives."), MessageBox.TYPE_INFO, timeout=10)

    def Format_ext4(self):
        from Screens.HarddiskSetup import HarddiskSelection
        self.session.openWithCallback(self.updateList, HarddiskSelection)

    def InitializationNeoB(self):
        if fileExists('/.multinfo'):
                self.session.open(MessageBox, _("This option is available only from Flash"), MessageBox.TYPE_INFO, timeout=10)
        else:
                from Plugins.Extensions.NeoBoot.files.tools import InitializationFormattingDisk
                self.session.open(InitializationFormattingDisk)
                
    def setWindowTitle(self):
        self.setTitle(_('Mount Manager'))

    def createSummary(self):
        return DeviceManagerSummary

    def selectionChanged(self):
        if len(self.list) == 0:
            return
        self.sel = self['list'].getCurrent()
        seldev = self.sel
        if self.sel:
            try:
                name = str(self.sel[0])
                desc = str(self.sel[1].replace('\t', '  '))
            except:
                name = ''
                desc = ''
        else:
            name = ''
            desc = ''
        for cb in self.onChangedEntry:
            cb(name, desc)

    def updateList(self, result=None, retval=None, extra_args=None):
        scanning = _('Wait please while scanning for devices...')
        self['lab1'].setText(scanning)
        self.activityTimer.start(10)

    def updateList2(self):
        self.activityTimer.stop()
        self.list = []
        list2 = []
        f = open('/proc/partitions', 'r')
        for line in f.readlines():
            parts = line.strip().split()
            if not parts:
                continue
            device = parts[3]
            if not re.search('sd[a-z][1-9]', device):
                continue
            if device in list2:
                continue
            self.buildMy_rec(device)
            list2.append(device)

        f.close()
        self['list'].list = self.list
        self['lab1'].hide()

    def buildMy_rec(self, device):
        mypath = SkinPath()
        device2 = re.sub('[0-9]', '', device)
        devicetype = path.realpath('/sys/block/' + device2 + '/device')
        d2 = device
        name = _('HARD DISK: ')
        mypixmap = '' + LinkNeoBoot + '/images/dev_hdd.png'
        model = open('/sys/block/' + device2 + '/device/model').read()
        model = str(model).replace('\n', '')
        des = ''
        if devicetype.find('usb') != -1:
            name = _('USB: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_usb.png'
        if devicetype.find('usb1') != -1:
            name = _('USB1: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_usb.png'
        if devicetype.find('usb2') != -1:
            name = _('USB2: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_usb.png'
        if devicetype.find('card') != -1:
            name = _('CARD: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_sd.png'

        name = name + model
        self.Console = Console()
        self.Console.ePopen("sfdisk -l /dev/sd? | grep swap | awk '{print $(NF-9)}' >/tmp/devices.tmp")
        sleep(0.5)
        f = open('/tmp/devices.tmp', 'r')
        swapdevices = f.read()
        f.close()
        if path.exists('/tmp/devices.tmp'):
            remove('/tmp/devices.tmp')
        swapdevices = swapdevices.replace('\n', '')
        swapdevices = swapdevices.split('/')
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find(device) != -1:
                parts = line.strip().split()
                d1 = parts[1]
                dtype = parts[2]
                rw = parts[3]
                break
                continue
            elif device in swapdevices:
                parts = line.strip().split()
                d1 = _('None')
                dtype = 'swap'
                rw = _('None')
                break
                continue
            else:
                d1 = _('None')
                dtype = _('unavailable')
                rw = _('None')

        f.close()
        size = Harddisk(device).diskSize()
        if float(size) / 1024 / 1024 >= 1:
            des = _('Size: ') + str(round(float(size) / 1024 / 1024, 2)) + _('TB')
        elif size / 1024 >= 1:
            des = _('Size: ') + str(round(float(size) / 1024, 2)) + _('GB')
        elif size >= 1:
            des = _('Size: ') + str(size) + _('MB')
        else:
            des = _('Size: ') + _('unavailable')
        if des != '':
            if rw.startswith('rw'):
                rw = ' R/W'
            elif rw.startswith('ro'):
                rw = ' R/O'
            else:
                rw = ''
            des += '\t' + _('Mount: ') + d1 + '\n' + _('Device: ') + '/dev/' + device + '\t' + _('Type: ') + dtype + rw
            png = LoadPixmap(mypixmap)
            res = (name, des, png)
            self.list.append(res)

    def SetupMounts(self):
        if getCheckExt() != 'vfat' and getCheckExt() == 'ext3' or getCheckExt() == 'ext4' :    
            self.SetupMountsGo()
        else:
            self.session.open(MessageBox, _('Disk the directory HDD or USB is not a ext2, ext3 or ext4.\nMake sure you select a valid partition type to install neoboot.'), type=MessageBox.TYPE_ERROR)

    def SetupMountsGo(self):
        if not fileExists('/etc/fstab.org'):
            os.system('cp -f /etc/fstab /etc/fstab.org')
        elif fileExists('/etc/fstab.org'):
            os.system('rm -f /etc/fstab; cp /etc/fstab.org /etc/fstab; rm /etc/fstab.org')
        self.session.openWithCallback(self.updateList, DevicesConf)

    def Unmount(self):
        sel = self['list'].getCurrent()
        if sel:
            des = sel[1]
            des = des.replace('\n', '\t')
            parts = des.strip().split('\t')
            mountp = parts[1].replace(_('Mount: '), '')
            device = parts[2].replace(_('Device: '), '')
            system('umount ' + mountp)
            try:
                mounts = open('/proc/mounts')
                mountcheck = mounts.readlines()
                mounts.close()
                for line in mountcheck:
                    parts = line.strip().split(' ')
                    if path.realpath(parts[0]).startswith(device):
                        self.session.open(MessageBox, _("Can't unmount partition, make sure it is not being used for swap or record/timeshift paths"), MessageBox.TYPE_INFO, timeout=10)

            except IOError:
                return -1

            self.updateList()

    def saveMypoints(self):
        sel = self['list'].getCurrent()
        if sel:
            parts = sel[1].split()
            self.device = parts[5]
            self.mountp = parts[3]
            self.Console.ePopen('umount ' + self.device)
            if self.mountp.find('/media/hdd') < 0:
                self.Console.ePopen('umount /media/hdd')
                self.Console.ePopen('/sbin/blkid | grep ' + self.device, self.add_fstab, [self.device, self.mountp])
            else:
                self.session.open(MessageBox, _('This Device is already mounted as HDD.'), MessageBox.TYPE_INFO, timeout=10, close_on_any_key=True)

    def add_fstab(self, result=None, retval=None, extra_args=None):
        self.device = extra_args[0]
        self.mountp = extra_args[1]
        self.device_uuid = 'UUID=' + result.split('UUID=')[1].split(' ')[0].replace('"', '')
        if not path.exists(self.mountp):
            mkdir(self.mountp, 493)
        open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if '/media/hdd' not in l])
        rename('/etc/fstab.tmp', '/etc/fstab')
        open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device not in l])
        rename('/etc/fstab.tmp', '/etc/fstab')
        open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device_uuid not in l])
        rename('/etc/fstab.tmp', '/etc/fstab')
        out = open('/etc/fstab', 'a')
        line = self.device_uuid + '\t/media/hdd\tauto\tdefaults\t0 0\n'
        out.write(line)
        out.close()
        self.Console.ePopen('mount -a', self.updateList)
        
        
class DevicesConf(Screen, ConfigListScreen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen name="DevicesConfFullHD" position="400,150" size="976,728" title="Choose where to mount your devices to:">
        <eLabel backgroundColor="black" font="baslk; 25" foregroundColor="red" position="150,900" size="800,30" text=" Exit - Back " transparent="1" />
        <widget name="key_red" position="110,13" zPosition="1" size="335,67" font="baslk;30" halign="center" valign="center" backgroundColor="red" transparent="1" foregroundColor="red" />
        <widget name="key_green" position="549,15" zPosition="1" size="362,65" font="baslk;30" halign="center" valign="center" backgroundColor="green" transparent="1" foregroundColor="green" />
        <widget name="config" position="33,179" size="891,385" font="Regular;21" scrollbarMode="showOnDemand" />
        </screen>"""
    else:
        skin = """<screen name="DevicesConfHD" position="171,130" size="903,460" title="Choose where to mount your devices to:">
        <eLabel backgroundColor="black" font="Regular;30" foregroundColor="orange" position="366,388" size="295,65" text="Exit - Back" transparent="1" />
        <widget name="key_red" position="36,0" zPosition="1" size="363,59" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        <widget name="key_green" position="548,0" zPosition="1" size="332,60" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
        <widget name="config" position="31,85" size="839,279" scrollbarMode="showOnDemand" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        ConfigListScreen.__init__(self, self.list)
        Screen.setTitle(self, _('Choose where to mount your devices to:'))
        self['key_green'] = Label(_('Save'))
        self['key_red'] = Label(_('Cancel'))
        self['Linconn'] = Label(_('Wait please while scanning your %s %s devices...n\\ Looking for a disk...'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'green': self.saveMypoints,
         'red': self.close,
         'back': self.close})
        self.updateList()

    def updateList(self):
        self.list = []
        list2 = []
        self.Console = Console()
        self.Console.ePopen("sfdisk -l /dev/sd? | grep swap | awk '{print $(NF-9)}' >/tmp/devices.tmp")
        sleep(0.5)
        f = open('/tmp/devices.tmp', 'r')
        swapdevices = f.read()
        f.close()
        if path.exists('/tmp/devices.tmp'):
            remove('/tmp/devices.tmp')
        swapdevices = swapdevices.replace('\n', '')
        swapdevices = swapdevices.split('/')
        f = open('/proc/partitions', 'r')
        for line in f.readlines():
            parts = line.strip().split()
            if not parts:
                continue
            device = parts[3]
            if not re.search('sd[a-z][1-9]', device):
                continue
            if device in list2:
                continue
            if device in swapdevices:
                continue
            self.buildMy_rec(device)
            list2.append(device)

        f.close()
        self['config'].list = self.list
        self['config'].l.setList(self.list)
        self['Linconn'].hide()

    def buildMy_rec(self, device):
        mypath = SkinPath()
        device2 = re.sub('[0-9]', '', device)
        devicetype = path.realpath('/sys/block/' + device2 + '/device')
        d2 = device
        name = _('HARD DISK: ')
        mypixmap = '' + LinkNeoBoot + '/images/dev_hdd.png'
        model = open('/sys/block/' + device2 + '/device/model').read()
        model = str(model).replace('\n', '')
        des = ''
        if devicetype.find('usb') != -1:
            name = _('USB: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_usb.png'
        if devicetype.find('usb1') != -1:
            name = _('USB1: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_usb.png'
        if devicetype.find('usb2') != -1:
            name = _('USB2: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_usb.png'
        if devicetype.find('card') != -1:
            name = _('CARD: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_sd.png'
        if devicetype.find('mmc') != -1:
            name = _('MMC: ')
            mypixmap = '' + LinkNeoBoot + '/images/dev_sd.png'            
            

        name = name + model
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find(device) != -1:
                parts = line.strip().split()
                d1 = parts[1]
                dtype = parts[2]
                break
                continue
            else:
                d1 = _('None')
                dtype = _('unavailable')

        f.close()
        size = Harddisk(device).diskSize()
        if float(size) / 1024 / 1024 >= 1:
            des = _('Size: ') + str(round(float(size) / 1024 / 1024, 2)) + _('TB')
        elif size / 1024 >= 1:
            des = _('Size: ') + str(round(float(size) / 1024, 2)) + _('GB')
        elif size >= 1:
            des = _('Size: ') + str(size) + _('MB')
        else:
            des = _('Size: ') + _('unavailable')
        item = NoSave(ConfigSelection(default='/media/' + device, choices=[('/media/' + device, '/media/' + device),
         ('/media/hdd', '/media/hdd'),
         ('/media/hdd2', '/media/hdd2'),
         ('/media/hdd3', '/media/hdd3'),
         ('/media/usb', '/media/usb'),
         ('/media/usb1', '/media/usb1'),
         ('/media/usb2', '/media/usb2'),
         ('/media/usb3', '/media/usb3'),
         ('/media/usb3', '/media/cf'),
         ('/media/usb3', '/media/card'),
         ('/media/cf', '/media/cf'),
         ('/media/mmc', '/media/mmc'),         
         ('/media/card', '/media/card')]))
        if dtype == 'Linux':
            dtype = 'ext2', 'ext3', 'ext4'
        else:
            dtype = 'auto'
        item.value = d1.strip()
        text = name + ' ' + des + ' /dev/' + device
        res = getConfigListEntry(text, item, device, dtype)
        if des != '' and self.list.append(res):
            pass

    def saveMypoints(self):
        self.Console = Console()
        mycheck = False
        for x in self['config'].list:
            self.device = x[2]
            self.mountp = x[1].value
            self.type = x[3]
            self.Console.ePopen('umount ' + self.device)
            self.Console.ePopen('/sbin/blkid | grep ' + self.device + ' && opkg list-installed ntfs-3g', self.add_fstab, [self.device, self.mountp])

        message = _('Continues mounting equipment...')
        ybox = self.session.openWithCallback(self.delay, MessageBox, message, type=MessageBox.TYPE_INFO, timeout=5, enable_input=False)
        ybox.setTitle(_('Please, wait....'))

    def delay(self, val):
        if fileExists('/etc/init.d/volatile-media.sh') and getBoxHostName() == "vusolo2":
            system('mv /etc/init.d/volatile-media.sh /etc/init.d/volatile-media.sh.org')
        message = _('GUI needs a restart.\nDo you want to Restart the GUI now?')
        ybox = self.session.openWithCallback(self.myclose, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('MOUNTING....'))

    def myclose(self, answer):
        if answer is True:
            os.system('reboot -f')                             
        else:
            self.messagebox = self.session.open(MessageBox, _('Return to installation...'), MessageBox.TYPE_INFO)
            self.close()

    def add_fstab(self, result=None, retval=None, extra_args=None):
        print("[MountManager] RESULT:"), result
        if result:
            self.device = extra_args[0]
            self.mountp = extra_args[1]
            if fileExists('/usr/lib/python2.7'):
                self.device_uuid = 'UUID=' + result.split('UUID=')[1].split(' ')[0].replace('"', '')
                self.device_type = result.split('TYPE=')[1].split(' ')[0].replace('"', '')
            else:              
                self.device_uuid = 'UUID=' + getMyUUID()
                self.device_type = getCheckExt()                        
            if self.device_type.startswith('ext'):
                self.device_type = 'auto'
            elif self.device_type.startswith('ntfs') and result.find('ntfs-3g') != -1:
                self.device_type = 'ntfs-3g'
            elif self.device_type.startswith('ntfs') and result.find('ntfs-3g') == -1:
                self.device_type = 'ntfs'
            if not path.exists(self.mountp):
                mkdir(self.mountp, 493)
            open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device not in l])
            rename('/etc/fstab.tmp', '/etc/fstab')
            open('/etc/fstab.tmp', 'w').writelines([l for l in open('/etc/fstab').readlines() if self.device_uuid not in l])
            rename('/etc/fstab.tmp', '/etc/fstab')
            out = open('/etc/fstab', 'a')
            if fileExists('/usr/lib/python2.7'):
                line = self.device_uuid + '\t' + self.mountp + '\t' + self.device_type + '\tdefaults\t0 0\n'
            else:
                line = 'UUID=' + getMyUUID() + '\t' + self.mountp + '\t' + self.device_type + '\tdefaults\t0 0\n'                           
            out.write(line)
            out.close()
            if fileExists('/usr/lib/python2.7'):
                self.device_uuid2 = result.split('UUID=')[1].split(' ')[0].replace('"', '')
            else:
                self.device_uuid = getMyUUID()
                
#            if fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager2'):
#                out1 = open('/etc/devicemanager.cfg', 'a')
#                line1 = '"' + self.device_uuid2 + '"' + ':' + self.mountp + '\n'
#                out1.write(line1)
#                out1.close()
#            elif fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager'):
#                out2 = open('/usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager/devicemanager.cfg', 'a')
#                line2 = '"' + self.device_uuid2 + '"' + ':' + self.mountp + '\n'
#                out2.write(line2)
#                out2.close()


#SetDiskLabel - dziekuje autorowi
class SetDiskLabel(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen name="SetDiskLabel" position="400,188" size="1100,601" title="Set Disk Label v1.1">
      <widget name="infoTXT" position="22,62" zPosition="1" size="591,86" font="baslk;28" halign="left" valign="center" backgroundColor="transpBlack" transparent="1" />

      <widget name="devlist" position="685,60" size="310,132" font="Regular;20" valign="center" />

      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_left.png" position="628,86" size="40,40" alphatest="on" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_right.png" position="1015,85" size="40,40" alphatest="on" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_up.png" position="630,381" size="40,42" alphatest="on" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_down.png" position="1010,383" size="40,40" alphatest="on" />

      <widget name="labelname" position="22,209" zPosition="1" size="591,86" font="baslk;30" valign="center" backgroundColor="transpBlack" transparent="1" />
      <widget name="disklabel" position="697,212" size="290,77" zPosition="1" font="baslk;30" valign="left" />
      <widget name="labeltoset" position="22,363" zPosition="1" size="591,86" font="baslk;30" valign="center" backgroundColor="transpBlack" transparent="1" />
      <widget name="listlabel" position="685,354" size="310,145" zPosition="1" font="Regular;20" valign="center" />

      <ePixmap pixmap="skin_default/buttons/key_red.png" position="14,534" size="40,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/key_green.png" position="259,535" size="40,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/key_yellow.png" position="567,535" size="40,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/key_blue.png" position="814,532" size="40,40" alphatest="on" />

      <widget name="key_red" position="60,526" zPosition="1" size="196,40" font="baslk;25" halign="left" valign="left" backgroundColor="transpBlack" transparent="1" />
      <widget name="key_green" position="304,526" zPosition="1" size="255,40" font="baslk;25" halign="left" valign="left" backgroundColor="transpBlack" transparent="1" />
      <widget name="key_yellow" position="613,526" zPosition="1" size="196,40" font="baslk;25" halign="left" valign="left" backgroundColor="transpBlack" transparent="1" />
      <widget name="key_blue" position="860,526" zPosition="1" size="233,40" font="baslk;25" halign="left" valign="left" backgroundColor="transpBlack" transparent="1" />
      <eLabel text="%s" font="Regular; 25" position="23,-10" size="968,57" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
      </screen> """ % (_('!!!Do not set the label for /dev/mmcblk0p !!!'))
    else:
        skin = """<screen position="center,center" size="600,200" title="Set Disk Label v1.1" >
      <widget name="infoTXT" position="25,20" zPosition="1" size="310,38" font="Regular;20" halign="left" valign="center" backgroundColor="transpBlack" transparent="1" />
      <widget name="devlist" position="400,20" size="125,25" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_left.png" position="350,15" size="40,40" alphatest="on" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_right.png" position="550,15" size="40,40" alphatest="on" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_up.png" position="350,105" size="40,40" alphatest="on" />
      <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/k_down.png" position="550,105" size="40,40" alphatest="on" />
      <widget name="labelname" position="25,65" zPosition="1" size="310,25" font="Regular;20" halign="left" valign="center" backgroundColor="transpBlack" transparent="1"/>
      <widget name="disklabel" position="400,65" size="125,25" zPosition="1" font="Regular;20" halign="center" valign="left"/>
      <widget name="labeltoset" position="25,110" zPosition="1" size="310,25" font="Regular;20" halign="left" valign="center" backgroundColor="transpBlack" transparent="1"/>
      <widget name="listlabel" position="400,110" size="125,25" zPosition="1" font="Regular;20" valign="left"/>
      <ePixmap pixmap="skin_default/buttons/key_red.png" position="40,167" size="40,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/key_green.png" position="170,167" size="40,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/key_yellow.png" position="300,167" size="40,40" alphatest="on" />
      <ePixmap pixmap="skin_default/buttons/key_blue.png" position="430,167" size="40,40" alphatest="on" />
      <widget name="key_red" position="70,160" zPosition="1" size="90,40" font="Regular;14" halign="center" valign="left" backgroundColor="transpBlack" transparent="1" />
      <widget name="key_green" position="200,160" zPosition="1" size="90,40" font="Regular;14" halign="center" valign="left" backgroundColor="transpBlack" transparent="1" />
      <widget name="key_yellow" position="330,160" zPosition="1" size="90,40" font="Regular;14" halign="center" valign="left" backgroundColor="transpBlack" transparent="1" />
      <widget name="key_blue" position="460,160" zPosition="1" size="90,40" font="Regular;14" halign="center" valign="left" backgroundColor="transpBlack" transparent="1" />
      </screen>"""

    def __init__(self, session):
        global liczymy
        Screen.__init__(self, session)
        self.labList = ['hdd', 'usb', 'card', 'cf']
        self.list = []
        self.sprDev()
        self.devlist = []
        self.disklabel = []
        self['devlist'] = MenuList(self.devlist)
        self['disklabel'] = Label(self.disklabel)
        self['listlabel'] = MenuList(self.labList)
        liczymy = 0
        for x in lista:
            self.devlist.append(x)
            liczymy += 1

        self.sprLabel()
        self['labelname'] = Label(_('Current partition label:'))
        self['labeltoset'] = Label(_('Choice label to set:'))
        self['infoTXT'] = Label(_('Select partition to set label:'))
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Set label'))
        self['key_yellow'] = Button(_('Add label'))
        self['key_blue'] = Button(_('Delete label'))
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions', 'DirectionActions'], {'cancel': self.MyClose,
         'red': self.MyClose,
         'green': self.wlacz,
         'yellow': self.addlabel,
         'blue': self.dellabel,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down}, -2)

    def sprDev(self):
        global lista
        lista = ['']
        if getTunerModel() in ('sf8008', 'sf8008s', 'sf8008t'):
            blackL = 'mmcblk0'
        if getTunerModel() in ('h9se'):
            blackL = 'mmcblk1'
        else:
            blackL = getoutput('cat /etc/udev/mount-helper.sh | grep "BLACKLISTED="')
            blackL = blackL[13:-1]
        devL = getoutput('cat /proc/partitions | grep "sd\\|mmc" | awk \'{print $4}\'')
        devL = devL.split('\n')
        ilosc = len(devL)
        i = 0
        while i < ilosc:
            if len(devL[i]) == 9 or len(devL[i]) == 4:
                if devL[i][:7] != blackL:
                    if self.sprLinux(devL[i]) == True:
                        lista.append(devL[i])
            i += 1

        if ilosc > 0:
            lista.remove('')
        elif lista[0] == '':
            lista.remove('')
            lista.insert(0, 'No Disk')

    def cancel(self):
        self.close()

    def wlacz(self):
        self.session.openWithCallback(self.wlaczyes, MessageBox, _('Set label on %s?') % str(self['devlist'].getCurrent()), MessageBox.TYPE_YESNO, default=False)

    def wlaczyes(self, w):
        if w == True:
            os.system('e2label /dev/%s "%s"' % (str(self['devlist'].getCurrent()), self['listlabel'].getCurrent()))
            self.session.open(MessageBox, _('Selected label is set'), type=MessageBox.TYPE_INFO, timeout=10)
            self.sprLabel()

    def addlabel(self):
        self.session.openWithCallback(self.addlabeltolist, VirtualKeyBoard, title=_('Add new partition label:'), text=self['disklabel'].getText())

    def dellabel(self):
        self.session.openWithCallback(self.delabelyes, MessageBox, _('Delete label from %s?') % str(self['devlist'].getCurrent()), MessageBox.TYPE_YESNO, default=False)

    def delabelyes(self, k):
        if k == True:
            os.system('e2label /dev/%s ""' % str(self['devlist'].getCurrent()))
            self.session.open(MessageBox, _('Label is delete'), type=MessageBox.TYPE_INFO, timeout=10)
            self.sprLabel()

    def zamknij(self, data):
        self.close()

    def left(self):
        self['devlist'].up()
        self.sprLabel()

    def right(self):
        self['devlist'].down()
        self.sprLabel()

    def up(self):
        self['listlabel'].up()

    def down(self):
        self['listlabel'].down()

    def addlabeltolist(self, z):
        if z is not None:
            self.labList.insert(0, z)
        return

    def sprLabel(self):
        lab = getoutput('blkid /dev/' + self['devlist'].getCurrent())
        lab1 = lab.split(' ')
        licz1 = len(lab1)
        i = 0
        while i < licz1:
            if lab1[i][:5] == 'LABEL':
                self['disklabel'].setText(lab1[i][7:-1])
                break
            else:
                self['disklabel'].setText(_('No label'))
            i += 1

    def sprLinux(self, dev):
        lab = getoutput('blkid /dev/' + dev)
        lab1 = lab.split(' ')
        licz1 = len(lab1)
        jest = False
        j = 0
        while j < licz1:
            if lab1[j][:9] == 'TYPE="ext':
                jest = True
                return jest
            jest = False
            j += 1

        return jest
    
    def MyClose(self):
        message = _('GUI needs a restart.\nDo you want to Restart the GUI now?')
        ybox = self.session.openWithCallback(self.mbdelete, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('Label Disc'))

    def mbdelete(self, answer):
        if answer is True:
            os.system('reboot -f')                             
        else:
            self.messagebox = self.session.open(MessageBox, _('Return to installation...'), MessageBox.TYPE_INFO)
            self.close()    

            
class DeviceManagerSummary(Screen):
    def __init__(self, session, parent):
        Screen.__init__(self, session, parent=parent)
        self['entry'] = StaticText('')
        self['desc'] = StaticText('')
        self.onShow.append(self.addWatcher)
        self.onHide.append(self.removeWatcher)

    def addWatcher(self):
        self.parent.onChangedEntry.append(self.selectionChanged)
        self.parent.selectionChanged()

    def removeWatcher(self):
        self.parent.onChangedEntry.remove(self.selectionChanged)

    def selectionChanged(self, name, desc):
        self['entry'].text = name
        self['desc'].text = desc


def SkinPath():
    myskinpath = resolveFilename(SCOPE_CURRENT_SKIN, '')
    if myskinpath == '' + LinkNeoBoot + '/images/':
        myskinpath = '' + LinkNeoBoot + '/images/'
    return myskinpath

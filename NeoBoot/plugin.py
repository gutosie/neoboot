# -*- coding: utf-8 -*-  

####################### _q(-_-)p_ gutosie _q(-_-)p_ ####################### 
# Copyright (c) , gutosie  license
# 
# Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 
# Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialnoĹ›ci za skutki uĹĽtkowania tego programu oraz za wykorzystanie zawartych tu informacji.
# Modyfikacje przeprowadzasz na wlasne ryzyko!!!
# O wszelkich zmianach prosze poinformowaÄ‡ na  http://all-forum.cba.pl w temacie pod nazwa  -#[NEOBOOT]#-

# This text/program is free document/software. Redistribution and use in
# source and binary forms, with or without modification, ARE PERMITTED provided
# save this copyright notice. This document/program is distributed WITHOUT any
# warranty, use at YOUR own risk.
#neoboot modules                         
#--------------------------------------------- NEOBOOT ---------------------------------------------#
from __future__ import absolute_import
from . import _
from Plugins.Extensions.NeoBoot.files.stbbranding import  LogCrashGS, getSupportedTuners, getLabelDisck, getINSTALLNeo, getNeoLocation, getLocationMultiboot, getNeoMount, getNeoMount2, getNeoMount3, getNeoMount4, getNeoMount5, getFSTAB, getFSTAB2, getKernelVersionString, getKernelImageVersion, getCPUtype, getCPUSoC,  getImageNeoBoot, getBoxVuModel, getBoxHostName, getTunerModel, getImageDistroN, getFormat, getNEO_filesystems, getBoxModelVU                   
from Plugins.Extensions.NeoBoot.files import Harddisk 
from Components.About import about                                                                                                                                                    
from enigma import getDesktop, eTimer
from Screens.Screen import Screen                                                                                                                                               
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
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
#from Components.PluginComponent import plugins
from Components.ConfigList import ConfigListScreen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
import os
import time
from time import gmtime, strftime
from Tools.Testinout import getTestIn, getTestOut, getTestInTime, getTestOutTime, getAccessN, getAccesDate, getButtonPin, getTestToTest
if fileExists('/etc/vtiversion.info') or fileExists('/etc/bhversion') or fileExists('/usr/lib/python3.8') and fileExists('/.multinfo'):   
    from Screens.Console import Console                   
else:
    try:
            from Plugins.Extensions.NeoBoot.files.neoconsole import Console 
    except:
            from Screens.Console import Console
    	
loggscrash = time.localtime(time.time())
PLUGINVERSION = '9.22'
UPDATEVERSION = '9.22'
UPDATEDATE = '"+%Y04%d"'   
LinkNeoBoot = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot' 

try:
    from enigma import addFont
    font_osans = LinkNeoBoot + '/neoskins/osans.ttf'
    font_sagoe = LinkNeoBoot + '/neoskins/sagoe.ttf'
    addFont(font_osans, 'genel', 100, True)    
    addFont(font_sagoe, 'baslk', 100, True)
    addFont(font_sagoe, 'tasat', 100, True)
    addFont(font_sagoe, 'dugme', 90, True)
except:
    print ("ERROR INSERTING FONT")
       
def neoTranslator():
    neolang = ''
    usedlang = open('/etc/enigma2/settings', 'r')
    lang = 'config.osd.language=pl_PL'
    local = usedlang.read().find(lang)
    if local != -1:
        neolang = 'islangPL'
    else:
        neolang = 'isnotlangPL'
    return neolang

def getDS():
    s = getDesktop(0).size()
    return (s.width(), s.height())

def isFHD():
    desktopSize = getDS()
    return desktopSize[0] == 1920

def isHD():
    desktopSize = getDS()
    return desktopSize[0] >= 1280 and desktopSize[0] < 1920

def isUHD():
    desktopSize = getDS()
    return desktopSize[0] >= 1920 and desktopSize[0] < 3840

class MyUpgrade(Screen):
    if isFHD():
        from Plugins.Extensions.NeoBoot.neoskins.default import MyUpgradeFULLHD
        skin=MyUpgradeFULLHD 
    elif isUHD():
        from Plugins.Extensions.NeoBoot.neoskins.default import MyUpgradeUltraHD
        skin=MyUpgradeUltraHD
    else:
        from Plugins.Extensions.NeoBoot.neoskins.default import MyUpgradeHD
        skin=MyUpgradeHD 

    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.wybierz()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.changever})

    def changever(self):		
        ImageChoose = self.session.open(NeoBootImageChoose)
        if fileExists('' + LinkNeoBoot + '/.location'):
            out = open('%sImageBoot/.version' % getNeoLocation(), 'w')
            out.write(PLUGINVERSION)
            out.close()
            self.close()
        else:
            self.close(self.session.open(MessageBox, _('No file location NeoBot, do re-install the plugin.'), MessageBox.TYPE_INFO, 10))
            self.close()
        return ImageChoose

    def wybierz(self):
        self.list = []
        mypath = '' + LinkNeoBoot + ''
        if not fileExists(mypath + 'icons'):
            mypixmap = '' + LinkNeoBoot + '/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('Update neoboot in all images ?'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):		
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.goKeyOk():
            pass
        self.close()

    def goKeyOk(self):		
            try:      
                    from Plugins.Extensions.NeoBoot.files.tools import UpdateNeoBoot
                    self.session.open(UpdateNeoBoot)           	
            except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    self.session.open(MessageBox, _('Sorry cannot open neo menu.'), MessageBox.TYPE_INFO, 5)


class NeoBootInstallation(Screen):
    if isFHD():
        from Plugins.Extensions.NeoBoot.neoskins.default import NeoBootInstallationFULLHD
        skin=NeoBootInstallationFULLHD 
    elif isUHD():
        from Plugins.Extensions.NeoBoot.neoskins.default import NeoBootInstallationUltraHD
        skin=NeoBootInstallationUltraHD
    else:
        from Plugins.Extensions.NeoBoot.neoskins.default import NeoBootInstallationHD
        skin=NeoBootInstallationHD 

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Instruction'))
        self['key_green'] = Label(_('Installation'))
        self['key_yellow'] = Label(_('SetDiskLabel'))
        self['key_blue'] = Label(_('Device Manager'))
        self['label1'] = Label(_('Welcome to NeoBoot %s Plugin installation.') % PLUGINVERSION)
        self['label3'] = Label(_('It is recommended to give a label to the disk.'))
        self['label2'] = Label(_('Here is the list of mounted devices in Your STB\nPlease choose a device where You would like to install NeoBoot'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'red': self.Instrukcja,                  
         'green': self.checkinstall,
         'ok': self.checkinstall,
         'key_menu': self.datadrive,
         'yellow': self.SetDiskLabel,         
         'blue': self.devices, 
         'back': self.close})             
        self.updateList()
                
    if fileExists('/etc/fstab'):
        neoformat = getFormat() 
        writefile = open('/tmp/.neo_format' , 'w')
        writefile.write(neoformat)
        writefile.close()

    def SetDiskLabel(self):
            try:
                    from Plugins.Extensions.NeoBoot.files.devices import SetDiskLabel
                    self.session.open(SetDiskLabel)
            except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    mess = _('Sorry cannot open menu set disk label\nAccess Fails with Error code 0x01.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)                
                                
    def Instrukcja(self):
            try:
                    from Plugins.Extensions.NeoBoot.files.tools import MyHelpNeo
                    self.session.open(MyHelpNeo)
            except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    mess = _('Sorry cannot open menu set disk label\nAccess Fails with Error code 0x01.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                    
    def datadrive(self):
        try:
            message = "echo -e '\n"
            message += _('NeoBot checks the connected media.\nWAIT ...\n\nDISCS:')
            message += "'"
            os.system(" 'mount | sed '/sd/!d' | cut -d" " -f1,2,3,4,5' ")
            cmd = '/sbin/blkid '
            system(cmd)
            print ("[MULTI-BOOT]: "), cmd
            self.session.open(Console, _('    NeoBot - Available media:'), [message, cmd])
        except Exception as e:
            loggscrash = time.localtime(time.time())
            LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
            pass

    def updateList(self):
        mycf, myusb, myusb2, myusb3, mysd, mycard, myhdd, myssd = ('', '', '', '', '', '', '', '')
        myoptions = []
        if fileExists('/proc/mounts'):
            fileExists('/proc/mounts')
            f = open('/proc/mounts', 'r')
            for line in f.readlines():
                if line.find('/media/cf') != -1:
                    mycf = '/media/cf/'
                    continue
                if line.find('/media/usb') != -1:
                    myusb = '/media/usb/'
                    continue
                if line.find('/media/usb2') != -1:
                    myusb2 = '/media/usb2/'
                    continue
                if line.find('/media/usb3') != -1:
                    myusb3 = '/media/usb3/'
                    continue
                if line.find('/media/card') != -1:
                    mysd = '/media/card/'
                    continue
                if line.find('/hdd') != -1:
                    myhdd = '/media/hdd/'
                    continue
                if line.find('/ssd') != -1:
                    myhdd = '/media/ssd/'
                    continue

            f.close()
        else:
            self['label2'].setText(_('Sorry it seems that there are not Linux formatted devices mounted on your STB. To install NeoBoot you need a Linux formatted part1 device. Click on the blue button to open Devices Panel'))
            fileExists('/proc/mounts')
        if mycf:
            self.list.append(mycf)
        else:
            mycf
        if myusb:
            self.list.append(myusb)
        else:
            myusb
        if myusb2:
            self.list.append(myusb2)
        else:
            myusb2
        if myusb3:
            self.list.append(myusb3)
        else:
            myusb3
        if mysd:
            mysd
            self.list.append(mysd)
        else:
            mysd            
        if mycard:
            mycard
            self.list.append(mycard)
        else:
            mycard           
        if myhdd:
            myhdd
            self.list.append(myhdd)
        else:
            myhdd
        if myssd:
            myssd
            self.list.append(myssd)
        else:
            myssd

        self['config'].setList(self.list)
               
    def checkReadWriteDir(self, configele):
        supported_filesystems = frozenset(('ext4', 'ext3', 'ext2', 'nfs'))
        candidates = []
        mounts = Harddisk.getProcMounts()

        for partition in Harddisk.harddiskmanager.getMountedPartitions(False, mounts):
            if partition.filesystem(mounts) in supported_filesystems:
                candidates.append((partition.description, partition.mountpoint))
        
        if candidates:
            locations = []
            for validdevice in candidates:
                locations.append(validdevice[1])

            if Harddisk.findMountPoint(os.path.realpath(configele)) + '/' in locations or Harddisk.findMountPoint(os.path.realpath(configele)) in locations:
                if fileExists(configele, 'w'):
                    return True
                else:
                    dir = configele
                    self.session.open(MessageBox, _('The directory %s is not a ext2, ext3, ext4 or nfs partition.\nMake sure you select a valid partition type to install.') % dir, type=MessageBox.TYPE_ERROR)
                    return False

            elif getFormat() == 'ext4' or getFormat() == 'ext3' or getFormat() == 'ext2' or getFormat() == 'nfs' :
                return True

            else:
                dir = configele
                self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
                return False
        else:
            dir = configele
            self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.\nIt may be helpful to restart the stb device completely.') % dir, type=MessageBox.TYPE_ERROR)
            return False

    def devices(self):
        check = False
        if check == False:
            message = _('After selecting OK start Mounting Manager, option Mount - green\n')
            message += _('Do you want to run the manager to mount the drives correctly ?\n')
            ybox = self.session.openWithCallback(self.device2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Device Manager'))

    def device2(self, yesno):
        if yesno:
            from Plugins.Extensions.NeoBoot.files.devices import ManagerDevice
            self.session.open(ManagerDevice)
        else:
            self.close()

    def checkinstall(self):
        if fileExists('/.multinfo'):
            mess = _('Sorry, Neoboot can be installed or upgraded only when booted from Flash')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
        else:            
            self.checkinstall2()
            
    def checkinstall2(self):
        if fileExists('/media/usb/ImageBoot/') and fileExists('/media/hdd/ImageBoot/'):                     
            mess = _('An error was encountered, you have neoboot installed on usb and hdd.\nUninstall one directories from one drive.') 
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

        else:
             self.checkinstall3()

    def checkinstall3(self):
        if checkInternet():  
            self.check_LabelDisck()
        else:
            mess = _('Geen internet')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)             

    def check_LabelDisck(self):
            system('blkid -c /dev/null /dev/sd* > ' + LinkNeoBoot + '/bin/reading_blkid; chmod 755 ' + LinkNeoBoot + '/bin/reading_blkid ')   
            if getLabelDisck() != 'LABEL=':	
                message = _('NeoBot - First use yellow button and Set Disk Label!\nWithout labeling disc neoboot may not work properly') 
                ybox = self.session.openWithCallback(self.goSetDiskLabel, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))
            else:
                self.check_fstabUUID()

    def check_fstabUUID(self):                
            if getFSTAB2() != 'OKinstall':
                    message = (_('Disk UUID not found\n - Universally unique identifier (UUID) is not required.\nYou can proceed with further installation or give an ID to your disk.\nTo continue the installation neoboo, press OK or No to abort.'))
                    ybox = self.session.openWithCallback(self.SetMountPointFSTAB, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Install Confirmation'))

            else:
                self.first_installation()

    def goSetDiskLabel(self, yesno):
        if yesno:                 
            from Plugins.Extensions.NeoBoot.files.devices import SetDiskLabel
            self.session.open(SetDiskLabel)
        else:
                message = _('NeoBot - choose what you want to do, install or not !!!') 
                ybox = self.session.openWithCallback(self.goInstall, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))

    def SetMountPointFSTAB(self, yesno):
        if yesno:                 
                message = _('Proceed with further installation without providing a unique identifier for the disks ?') 
                ybox = self.session.openWithCallback(self.goInstall, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))
        else:
                self.devices()
                
    def goInstall(self, yesno):
        if yesno:
            self.first_installation()        
        else:
            self.myclose2(_('NeoBoot has not been installed !  :(' ))

    def first_installation(self):
        check = False
        if fileExists('/proc/mounts'):
            with open('/proc/mounts', 'r') as f:
                for line in f.readlines():
                    if line.startswith('/dev/sd') and line.find('/media/hdd') or line.find('/media/usb')  == -1 and (line.find('ext4') != -1 or line.find('ext3') != -1 or line.find('ext2') != -1):
                        check = True
                        break
                    
        if check == False:
            self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to install NeoBoot!'), MessageBox.TYPE_INFO)
        else:
            self.mysel = self['config'].getCurrent()
            if self.checkReadWriteDir(self.mysel):
                message = _('Do You really want to install NeoBoot in:\n ') + self.mysel + '  ?'
                ybox = self.session.openWithCallback(self.install2, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))
            else:
                self.close()

    def install2(self, yesno):		
        print ("yesno:"), yesno
        if yesno:                 
            self.first_installationNeoBoot()
        else:
            self.myclose2(_('NeoBoot has not been installed ! :(' ))

    def first_installationNeoBoot(self):                	    
            self.mysel = self['config'].getCurrent()
            os.system('cd ' + LinkNeoBoot + '/; chmod 0755 ./bin/neoini*; chmod 0755 ./ex_init.py; chmod 0755 ./tmpfiles/target/*.sh; chmod 0755 ./files/userscript.sh')                                    
            cmd1 = 'mkdir ' + self.mysel + 'ImageBoot;mkdir ' + self.mysel + 'ImagesUpload' 
            system(cmd1)
            cmd2 = 'mkdir ' + self.mysel + 'ImageBoot;mkdir ' + self.mysel + 'ImagesUpload/.kernel' 
            system(cmd2)                                               

            if os.path.isfile('' + LinkNeoBoot + '/.location'): 
                os.system('rm -f ' + LinkNeoBoot + '/.location')  		                                                                                          
            out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'w')
            out.write(self.mysel)
            out.close()     
	
            if os.path.isfile('%sImageBoot/.neonextboot' % getNeoLocation()): 
                        os.system('rm -f /etc/neoimage; rm -f /etc/imageboot; rm -f %sImageBoot/.neonextboot; rm -f %sImageBoot/.version; rm -f %sImageBoot/.Flash; rm -f %sImageBoot/.imagedistro; rm -f %sImageBoot/.initneo.log; rm -f %sImageBoot/.updateversion' % ( getNeoLocation(), getNeoLocation(), getNeoLocation(), getNeoLocation(), getNeoLocation(), getNeoLocation()) ) 

            if os.path.isfile('%sImageBoot/.neonextboot' % getNeoLocation()): 
                    os.system('rm -f /etc/neoimage; rm -f /etc/imageboot; rm -f %sImageBoot/.neonextboot; rm -f %sImageBoot/.version; rm -f %sImageBoot/.Flash; ' % (getNeoLocation(), getNeoLocation(), getNeoLocation()) )

            if os.path.isfile('%sImagesUpload/.kernel/zImage*.ipk or %sImagesUpload/.kernel/zImage*.bin' % ( getNeoLocation(), getNeoLocation()) ): 
                        os.system('rm -f %sImagesUpload/.kernel/zImage*.ipk; rm -f %sImagesUpload/.kernel/zImage*.bin' % ( getNeoLocation(),getNeoLocation()) )                    

            if fileExists('/etc/issue.net'):
                try:
                    lines = open('/etc/hostname', 'r').readlines()
                    imagename = lines[0][:-1]
                    image = imagename
                    open('%sImageBoot/.Flash' % getNeoLocation(), 'w').write(image)
                except:
                    False
                                                    
            if not fileExists('/usr/lib/periodon/.accessdate'):
                    os.system('date %s  > /usr/lib/periodon/.accessdate' % UPDATEDATE)

            out1 = open('%sImageBoot/.version' % getNeoLocation(), 'w')
            out1.write(PLUGINVERSION)
            out1.close()                        
            out2 = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'w')
            out2.write('Flash ')
            out2.close()
            out3 = open('' + LinkNeoBoot + '/.neo_info', 'w')
            out3.write('Kernel\n')
            out3.write('Kernel-Version: ' + about.getKernelVersionString() + '\n')
            out3.write('NeoBoot\n')
            out3.write('NeoBoot-Version: ' + PLUGINVERSION + '\n')
            out3.close() 
            out = open('%sImageBoot/.updateversion' % getNeoLocation(), 'w')
            out.write(UPDATEVERSION)
            out.close()

            if fileExists('/usr/lib/enigma2/python/boxbranding.so'):
                    from boxbranding import getImageDistro
                    imagedistro = getImageDistro() 
                    writefile = open('%sImageBoot/.imagedistro' % getNeoLocation(), 'w')
                    writefile.write(imagedistro)
                    writefile.close()
            elif fileExists('/usr/lib/enigma2/python/Plugins/PLi'):
                    obraz = open('/etc/issue.net', 'r').readlines()
                    imagetype = obraz[0][:-3]
                    image = imagetype                      
                    writefile = open('%sImageBoot/.imagedistro' % getNeoLocation(), 'w')
                    writefile.write(imagetype)
                    writefile.close()                                                                                                                           
            elif fileExists('/etc/vtiversion.info'):
                    f = open("/etc/vtiversion.info",'r') 
                    imagever = f.readline().strip().replace("Release ", " ")
                    f.close()
                    image = imagever
                    writefile = open('%sImageBoot/.imagedistro' % getNeoLocation(), 'w')
                    writefile.write(imagever)
                    writefile.close()
            elif fileExists('/etc/bhversion'):
                    f = open("/etc/bhversion",'r') 
                    imagever = f.readline().strip()
                    f.close()
                    image = imagever
                    writefile = open('%sImageBoot/.imagedistro' % getNeoLocation(), 'w')
                    writefile.write(imagever)
                    writefile.close()

            if not os.path.isfile('' + LinkNeoBoot + '/bin/install') :
                if os.system('opkg update; opkg list-installed | grep python-subprocess') != 0:
                            os.system('opkg install python-subprocess')
                if os.system('opkg list-installed | grep python-argparse') != 0:
                            os.system('opkg install python-argparse')
                if os.system('opkg list-installed | grep curl') != 0:
                            os.system('opkg install curl')                                                                    
                if getCPUtype() == 'MIPS':
                    if os.system('opkg list-installed | grep kernel-module-nandsim') != 0:
                            os.system('opkg install kernel-module-nandsim')  
                    if os.system('opkg list-installed | grep mtd-utils-jffs2') != 0:
                            os.system('opkg install mtd-utils-jffs2')
                    if os.system('opkg list-installed | grep lzo') != 0:                            
                            os.system('opkg install lzo') 
                    if os.system('opkg list-installed | grep python-setuptools') != 0:                            
                            os.system('opkg install python-setuptools')                             
                    if os.system('opkg list-installed | grep util-linux-sfdisk') != 0: 
                            os.system('opkg install util-linux-sfdisk') 
                    if os.system('opkg list-installed | grep packagegroup-base-nfs') != 0:                            
                            os.system('opkg install packagegroup-base-nfs')                       
                    if os.system('opkg list-installed | grep ofgwrite') != 0:                                                                                                                                                                                                                                                                                                                                                
                            os.system('opkg install ofgwrite')
                    if os.system('opkg list-installed | grep bzip2') != 0:                                                                                                                                                                                                                                                                                                                                                
                            os.system('opkg install bzip2')
                    if os.system('opkg list-installed | grep mtd-utils') != 0:
                            os.system('opkg install mtd-utils')
                    if os.system('opkg list-installed | grep mtd-utils-ubifs') != 0:                                                                                                                                                                                                                                                                                                                                                
                            os.system('opkg install mtd-utils-ubifs')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
            #_____Other ARM procesor____ - here you can add your tuner stb                                                                                                                                                                   
            if getCPUtype() == "ARMv7" and getBoxHostName() == "axashistwin" or getBoxHostName() == "i55plus " or getBoxHostName() == "zgemmai55plus " or getBoxHostName() == "h92s" or getBoxHostName() == "zgemmah92s" or getBoxHostName() == "h7" or getBoxHostName() == "zgemmah7" or getBoxHostName() == "h9" or getBoxHostName() == "zgemmah9" or getBoxHostName() == "h9s" or getBoxHostName() == "zgemmah9s" or getBoxHostName() == "h9se" or getBoxHostName() == "zgemmah9se" or getBoxHostName() == "h9twin" or getBoxHostName() == "zgemmah9twin" or getBoxHostName() == "h9combo" or getBoxHostName() == "h9combose" or getBoxHostName() == "h10" or getBoxHostName() == "zgemmahh10" or getBoxHostName() == "hd51" or getBoxHostName() == "ax51" or getBoxHostName() == "ax60" or getBoxHostName() == "ax61" or getBoxHostName() == "sf4008" or getBoxHostName() == "sf8008" or getBoxHostName() == "ustym4kpro" or getBoxHostName() == "tmtwin4k" or getBoxHostName() == "anadol4k" or getBoxHostName() == "protek4k" or getBoxHostName() == "maxytecmulti" or getBoxHostName() == "viper4k" or getBoxHostName() == "dm900" or getBoxHostName() == "dm920" or getBoxHostName() == "et1x000" or getBoxHostName() == "gbquad4k" or getBoxHostName() == "axashisc4k" or getBoxHostName() == "axmultitwin" or getBoxHostName() == "axmulticombo" or getBoxHostName() == "osmio4k" or getBoxHostName() == "osmio4kplus" :              
                        os.system('cp -f ' + LinkNeoBoot + '/bin/neoinitarm /sbin/neoinitarm; chmod 0755 /sbin/neoinitarm; ln -sfn /sbin/neoinitarm /sbin/init; mv ' + LinkNeoBoot + '/tmpfiles/runpy/arm_run.py ' + LinkNeoBoot + '/run.py; cd')                                                                          
            #VUPLUS ARM
            elif getCPUtype() == "ARMv7" and getBoxHostName() !=  "ustym4kpro":
                if getBoxHostName() == "vuduo4k":
                        os.system('cd ' + LinkNeoBoot + '/' )
                        os.system('cp -Rf ' + LinkNeoBoot + '/bin/neoinitarm /sbin/neoinitarm; cp -Rf ' + LinkNeoBoot + '/bin/neoinitarmvuDuo4k /sbin/neoinitarmvu; mv ' + LinkNeoBoot + '/tmpfiles/runpy/duo4k_run.py ' + LinkNeoBoot + '/run.py; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')                  
                        os.system('dd if=/dev/mmcblk0p6 of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()) )
                        os.system('mv ' + LinkNeoBoot + '/tmpfiles/target/vuDuo4Kmmcblk0p6.sh ' + LinkNeoBoot + '/files/kernel.sh; cd')                         

                elif getBoxHostName() == "vuduo4kse"  and getBoxHostName() !=  "vuultimo4k":
                        os.system('cd ' + LinkNeoBoot + '/' )
                        os.system('cp -Rf ' + LinkNeoBoot + '/bin/neoinitarm /sbin/neoinitarm; cp -Rf ' + LinkNeoBoot + '/bin/neoinitarmvuDuo4k /sbin/neoinitarmvu; mv ' + LinkNeoBoot + '/tmpfiles/runpy/duo4kse_run.py ' + LinkNeoBoot + '/run.py; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')                  
                        os.system('dd if=/dev/mmcblk0p6 of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()) )
                        os.system('mv ' + LinkNeoBoot + '/tmpfiles/target/vuDuo4Ksemmcblk0p6.sh ' + LinkNeoBoot + '/files/kernel.sh; cd') 

                elif getBoxHostName() == "vuzero4k":     
                        os.system('cd ' + LinkNeoBoot + '/' )
                        os.system('cp -Rf ' + LinkNeoBoot + '/bin/neoinitarm /sbin/neoinitarm; cp -Rf ' + LinkNeoBoot + '/bin/neoinitarmvu /sbin/neoinitarmvu; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')
                        os.system('dd if=/dev/mmcblk0p4 of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()) )      
                        os.system('mv ' + LinkNeoBoot + '/tmpfiles/target/vuZero4Kmmcblk0p4.sh ' + LinkNeoBoot + '/files/kernel.sh; mv ' + LinkNeoBoot + '/tmpfiles/runpy/zero4k_run.py ' + LinkNeoBoot + '/run.py; rm -f ' + LinkNeoBoot + '/bin/neoinitarmvuDuo4k; cd')                         
                                                                                                                                                                                                                                                                                                                                                                                         
                elif getBoxHostName() == "vuultimo4k" or getBoxHostName() == "vusolo4k" or getBoxHostName() == "vuuno4k" or getBoxHostName() == "vuuno4kse" :
                        os.system('cd ' + LinkNeoBoot + '/' )
                        os.system('cp -Rf ' + LinkNeoBoot + '/bin/neoinitarm /sbin/neoinitarm; cp -Rf ' + LinkNeoBoot + '/bin/neoinitarmvu /sbin/neoinitarmvu; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')                  
                        os.system('dd if=/dev/mmcblk0p1 of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()) )
                        os.system('mv ' + LinkNeoBoot + '/tmpfiles/target/vu_mmcblk0p1.sh ' + LinkNeoBoot + '/files/kernel.sh; mv ' + LinkNeoBoot + '/tmpfiles/runpy/vu4k_run.py ' + LinkNeoBoot + '/run.py; rm -f; rm -f ' + LinkNeoBoot + '/bin/neoinitarmvuDuo4k; cd')                         
                else:
                    self.messagebox = self.session.open(MessageBox, _('The tuner is not supported by NeoBoot.\nContact the author.\nNo proper STB for installation !!!!'), type=MessageBox.TYPE_ERROR)                                                                        
            # MIPS                                                                                                                                                                                                                 
            elif getCPUtype() == 'MIPS':
                if getBoxHostName() == "vuduo" or getBoxHostName() == "vusolo" or getBoxHostName() == "vuuno" or getBoxHostName() == "vuultimo" or getBoxHostName() == "vusolo2" or getBoxHostName() == "vuduo2" or getBoxHostName() == "vusolose" or getBoxHostName() == "vuzero" or getBoxHostName() == "mbmini" or getBoxHostName() == "mbultra" or getBoxHostName() == "osmini" or getBoxHostName() == "formuler4turbo" or getBoxHostName() == "h3" or getBoxHostName() == "formuler3" :                                                                                                                                                                                                
                        #vuplus stb mtd1
                        if getBoxHostName() == 'bm750' or getBoxHostName() == 'vuduo' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vuultimo':
                            if fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; /usr/sbin/nanddump /dev/mtd1  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            elif not fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; ' + LinkNeoBoot + '/bin/nanddump_mips /dev/mtd1  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            os.system('cd ' + LinkNeoBoot + '/; rm ./bin/fontforneoboot.ttf; rm ./bin/libpngneo; mv ' + LinkNeoBoot + '/tmpfiles/target/vu_dev_mtd1.sh ' + LinkNeoBoot + '/files/kernel.sh;mv ' + LinkNeoBoot + '/tmpfiles/runpy/vu_mtd1_run.py ' + LinkNeoBoot + '/run.py; cd')                         

                        #vuplus stb mtd2  
                        elif getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vusolose' or getBoxHostName() == 'vuzero':
                            if fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; /usr/sbin/nanddump /dev/mtd2  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            elif not fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; ' + LinkNeoBoot + '/bin/nanddump_mips /dev/mtd2  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            os.system('cd ' + LinkNeoBoot + '/; rm ./bin/fontforneoboot.ttf; rm ./bin/libpngneo; mv ' + LinkNeoBoot + '/tmpfiles/target/vu_dev_mtd2.sh ' + LinkNeoBoot + '/files/kernel.sh;mv ' + LinkNeoBoot + '/tmpfiles/runpy/vu_mtd2_run.py ' + LinkNeoBoot + '/run.py; cd')                         

                        #Other stb MIPS 
                        else:                                                                                                                                                                                                                                                              
                            os.system('cd ' + LinkNeoBoot + '/; chmod 755 ./bin/nandwrite; mv ./bin/fontforneoboot.ttf /usr/share/fonts; mv ./bin/libpngneo /usr/lib; cp -f ./bin/neoinitmips /sbin/neoinitmips; cp -f ./bin/neoinitmipsvu /sbin/neoinitmipsvu; chmod 0755 /sbin/neoinit*; rm -f ./bin/neobm; mv ./bin/neobmmips ./bin/neobm; chmod 0755 ./bin/neobm; chmod 0755 /usr/lib/libpngneo; cd; chmod 0755 /sbin/neoinitmips; ln -sf /media/neoboot/ImageBoot/.neonextboot /etc/neoimage; mv ' + LinkNeoBoot + '/tmpfiles/runpy/mips_run.py ' + LinkNeoBoot + '/run.py; cd')
                            
                        os.system('cp -Rf ' + LinkNeoBoot + '/bin/neoinitmips /sbin/neoinitmips; cp -Rf ' + LinkNeoBoot + '/bin/neoinitmipsvu /sbin/neoinitmipsvu; chmod 755 /sbin/neoinit*') 
                        os.system('chmod 755 ' + LinkNeoBoot + '/bin/nfidump; chmod 0755 ' + LinkNeoBoot + '/bin/nanddump_mips; rm -r ' + LinkNeoBoot + '/bin/neoinitar*; cd /')
                        if fileExists('' + LinkNeoBoot + '/bin/fontforneoboot.ttf'):
                            ('cd ' + LinkNeoBoot + '/;mv ./bin/fontforneoboot.ttf /usr/share/fonts; cd /')
                        if fileExists('' + LinkNeoBoot + '/bin/libpngneo'):
                            ('cd ' + LinkNeoBoot + '/;mv ./bin/libpngneo /usr/lib; chmod 0755 /usr/lib/libpngneo; cd /')                   
                        if fileExists('' + LinkNeoBoot + '/bin/neobm'):
                            ('cd ' + LinkNeoBoot + '/;chmod 0755 ./bin/neobm; cd /')
            else:
                self.messagebox = self.session.open(MessageBox, _('The tuner is not supported by NeoBoot.\nContact the author.\nNo proper STB for installation !!!!'), type=MessageBox.TYPE_ERROR)
                
            if fileExists('/home/root/vmlinux.gz'):
                            os.system('mv -f /home/root/vmlinux.gz %sImagesUpload/.kernel/%s.vmlinux.gz' % (getNeoLocation(), getBoxHostName()) )  
                                             
            if fileExists('' + LinkNeoBoot + '/ubi_reader'): 
                os.system('rm -r ' + LinkNeoBoot + '/ubi_reader ') 
                
            if getCPUtype() == 'ARMv7':                                                                                                                                     
                        os.system('cd ' + LinkNeoBoot + '/; mv ./bin/fbcleararm ./bin/fbclear; chmod 755 ./bin/fbclear; rm -f ./bin/nandwrite; rm -f ./bin/fbclearmips; mv ./ubi_reader_arm ./ubi_reader; rm -r ./ubi_reader_mips; rm ./bin/neoinitmips; rm ./bin/neoinitmipsvu; rm -r ./bin/nanddump_mips; rm ./bin/nfidump; rm ./bin/neobmmips; rm ./bin/neobm; mv ./bin/neobmarm ./bin/neobm; rm ./bin/fontforneoboot.ttf; rm ./bin/libpngneo; cd')   
            elif getCPUtype() == 'MIPS':       
                        os.system('cd ' + LinkNeoBoot + '/; mv ./bin/fbclearmips ./bin/fbclear; chmod 755 ./bin/fbclear; rm -f ./bin/fbcleararm; mv ./ubi_reader_mips ./ubi_reader; rm -r ./ubi_reader_arm; rm -f /bin/neoinitarm; rm -f /bin/neoinitarmvu; rm -r ./bin/nanddump_arm; rm -f /bin/neoinitarmvuDuo4k; ; rm -f ./bin/neobmarm')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
            os.system(' ln -sfn ' + getNeoLocation() + 'ImageBoot/.neonextboot /etc/neoimage; chmod 644 ' + getNeoLocation() + 'ImagesUpload/.kernel/*; ln -sfn ' + getNeoLocation() + 'ImageBoot /etc/imageboot; rm -r ' + LinkNeoBoot + '/tmpfiles; chmod 0755 ' + LinkNeoBoot + '/files/kernel.sh')
                                                                                                                                                                                                                                                                                                      
            if os.path.isfile('' + LinkNeoBoot + '/.location'): 		
                if getLabelDisck() != 'LABEL=':	
                    cmd = "echo -e '\n%s '" % _('NeoBoot has been installed succesfully!\nNeoBoot has detected that the disks do not have a label.\nFor correct neo boot operation, please give the disks the name LABEL\nRecommended total restart of the tuner.\n')
                elif getLabelDisck() == 'LABEL=':	
                    cmd = "echo -e '\n%s '" % _('Installed succesfully NEOBOOT!\nNeoBoot has detected that the disks have been marked.\nRecommended total restart of the tuner\n')                     
            else:                                                      	
                self.myclose2(_('NeoBoot has not been installed ! :(' ))

            closereboot = self.rebootSTBE2()    
            self.session.open(Console, _('NeoBoot Install....'), [cmd])             
            self.close(closereboot)                


    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        
    
    def rebootSTBE2(self):
            restartbox = self.session.openWithCallback(self.RebootSTB, MessageBox, _('Reboot stb now  ?'), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_('Reboot'))

    def RebootSTB(self, answer):
        if answer is True:
            #plugins.reloadPlugins()
            os.system('sync && echo 3 > /proc/sys/vm/drop_caches; reboot -d -f')
        else:
            #plugins.reloadPlugins()        
            self.close()        


class NeoBootImageChoose(Screen):
    if isFHD(): 
        from Plugins.Extensions.NeoBoot.usedskin import ImageChooseFULLHD
        skin=ImageChooseFULLHD
    elif isUHD():
        from Plugins.Extensions.NeoBoot.neoskins.default import ImageChooseULTRAHD
        skin=ImageChooseULTRAHD 
    else:
        from Plugins.Extensions.NeoBoot.neoskins.default import ImageChooseHD
        skin=ImageChooseHD   

    def __init__(self, session):				
        Screen.__init__(self, session)

        self.list = []
        self.setTitle('         NeoBoot  %s  - Menu' % PLUGINVERSION + '          ' + 'Ver. update:  %s' % UPDATEVERSION)
        self['device_icon'] = Pixmap()
        self['progreso'] = ProgressBar()
        self['linea'] = ProgressBar()
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Download Image'))
        self['key_green'] = Label(_('Installation'))
        self['key_yellow'] = Label(_('Remove Image '))
        self['key_blue'] = Label(_('Info'))
        self['key_menu'] = Label(_('More options'))
        self['key_1'] = Label(_('Update NeoBot'))
        self['key_2'] = Label(_('Reinstall NeoBoot'))
        self['key_3'] = Label(_('Reinstall kernel'))               
        self['label1'] = Label(_('Please choose an image to boot'))
        self['label2'] = Label(_('NeoBoot is running from:'))
        self['label3'] = Label('')
        self['label4'] = Label(_('NeoBoot is running image:'))
        self['label5'] = Label('')
        self['label6'] = Label('')
        self['label7'] = Label('')
        self['label8'] = Label(_('Number of images installed:'))                              
        self['label9'] = Label('')
        self['label10'] = Label('')
        self['label11'] = Label('')
        self['label12'] = Label('')
        self['label13'] = Label(_('Version update: '))
        self['label14'] = Label(_('NeoBoot version: '))
        self['label15'] = Label(_('Memory disc:')) 
        self['label16'] = Label(_('Kernel'))  
        self['label17'] = Label('')  
        self['label18'] = Label('')         
        self['label19'] = Label('')  
        self['label20'] = Label('')   
        self['label21'] = Label('NEO VIP')                                  
        self['actions'] = ActionMap(['WizardActions',
         'ColorActions',
         'MenuActions',
         'NumberActionMap',
         'SetupActions',
         'number'], {'ok': self.bootIMG,
         'red': self.DownloadImageOnline,                  
         'green': self.ImageInstall,
         'yellow': self.removeIMG,
         'blue': self.pomoc,
         'menu': self.mytools,        
         '1': self.neoboot_update,
         '2': self.ReinstallNeoBoot,
         '3': self.ReinstallKernel, 
         '4': self.touch4,        #hidden option           
         '5': self.touch5,        #hidden option
         '6': self.touch6,        #hidden option         
         '7': self.touch7,        #hidden option
         '8': self.touch8,        #hidden option
         '9': self.touch9,        #hidden option                                                                                              
         '0': self.touch0,        #hidden option 
         'back': self.close_exit})
        self.availablespace = 0         
        if not fileExists('/etc/name'):
            os.system('touch /etc/name')
        self.onShow.append(self.updateList)

        if not fileExists('' + LinkNeoBoot + '/files/mountpoint.sh'):
            os.system('touch ' + LinkNeoBoot + '/files/mountpoint.sh; echo "#!/bin/sh\n"  >> ' + LinkNeoBoot + '/files/mountpoint.sh; chmod 0755 ' + LinkNeoBoot + '/files/mountpoint.sh') 
            if getNeoMount() == 'hdd_install_/dev/sda1': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\nmkdir -p /media/sda1\n/bin/mount /dev/sda1 /media/hdd\n/bin/mount /dev/sda1 /media/sda1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            elif getNeoMount() == 'hdd_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\nmkdir -p /media/sdb1\n/bin/mount /dev/sdb1 /media/hdd\n/bin/mount /dev/sdb1 /media/sdb1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            elif getNeoMount() == 'hdd_install_/dev/sda2': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\nmkdir -p /media/sda2\n/bin/mount /dev/sda2 /media/hdd\n/bin/mount /dev/sda2 /media/sda2"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            elif getNeoMount() == 'hdd_install_/dev/sdb2': 
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\nmkdir -p /media/sdb2\n/bin/mount /dev/sdb2 /media/hdd\n/bin/mount /dev/sdb2 /media/sdb2"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            #---------------------------------------------
            if getNeoMount2() == 'usb_install_/dev/sdb1': 
                    os.system('echo "\numount -l /media/usb\nmkdir -p /media/usb\nmkdir -p /media/sdb1\n/bin/mount /dev/sdb1 /media/usb\n/bin/mount /dev/sdb1 /media/sdb1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')      
            elif getNeoMount2() == 'usb_install_/dev/sda1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\nmkdir -p /media/sda1\n/bin/mount /dev/sda1 /media/sda1\n/bin/mount /dev/sda1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdb2': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\nmkdir -p /media/sdb2\n/bin/mount /dev/sdb2 /media/sdb2\n/bin/mount /dev/sdb2 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdc1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\nmkdir -p /media/sdc1\n/bin/mount /dev/sdc1 /media/sdb2\n/bin/mount /dev/sdc1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdd1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\nmkdir -p /media/sdd1\n/bin/mount /dev/sdd1 /media/sdd1\n/bin/mount /dev/sdd1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sde1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\nmkdir -p /media/sde1\n/bin/mount /dev/sde1 /media/sde1\n/bin/mount /dev/sde1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdf1': 
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\nmkdir -p /media/sdf1\n/bin/mount /dev/sdf1 /media/sdf1\n/bin/mount /dev/sdf1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')  
            #---------------------------------------------                                  
            elif getNeoMount3() == 'cf_install_/dev/sda1': 
                    os.system('echo "umount -l /media/cf\nmkdir -p /media/cf\nmkdir -p /media/sdb1\n/bin/mount /dev/sda1 /media/cf\n/bin/mount /dev/sda1 /media/sda1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            elif getNeoMount3() == 'cf_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/cf\nmkdir -p /media/cf\nmkdir -p /media/sdb1\n/bin/mount /dev/sdb1 /media/cf\n/bin/mount /dev/sdb1 /media/sdb1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            #---------------------------------------------
            elif getNeoMount4() == 'card_install_/dev/sda1': 
                    os.system('echo "umount -l /media/card\nmkdir -p /media/card\nmkdir -p /media/sda1\n/bin/mount /dev/sda1 /media/card\n/bin/mount /dev/sda1 /media/sda1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            elif getNeoMount4() == 'card_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/card\nmkdir -p /media/card\nmkdir -p /media/sdb1\n/bin/mount /dev/sdb1 /media/card\n/bin/mount /dev/sdb1 /media/sdb1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            #---------------------------------------------
            elif getNeoMount5() == 'mmc_install_/dev/sda1': 
                    os.system('echo "umount -l /media/mmc\nmkdir -p /media/mmc\nmkdir -p /media/sda1\n/bin/mount /dev/sda1 /media/mmc\n/bin/mount /dev/sda1 /media/sda1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            elif getNeoMount5() == 'mmc_install_/dev/sdb1': 
                    os.system('echo "umount -l /media/mmc\nmkdir -p /media/mmc\nmkdir -p /media/sdb1\n/bin/mount /dev/sdb1 /media/mmc\n/bin/mount /dev/sdb1 /media/sdb1"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 
            os.system('echo "\n\nexit 0"  >> ' + LinkNeoBoot + '/files/mountpoint.sh') 

        if not fileExists('' + LinkNeoBoot + '/files/neo.sh'):
            system('' + LinkNeoBoot + '/files/mountpoint.sh') 
            system('echo ' + getLocationMultiboot() + ' > ' + LinkNeoBoot + '/bin/install; chmod 0755 ' + LinkNeoBoot + '/bin/install')    
            if getLocationMultiboot() == '/dev/sda1':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sda1 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()
            elif getLocationMultiboot() == '/dev/sdb1':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sdb1 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()
            elif getLocationMultiboot() == '/dev/sda2':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sda2 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()
            elif getLocationMultiboot() == '/dev/sdb2':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sdb2 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()
            elif getLocationMultiboot() == '/dev/sdc1':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sdc1 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()                    
            elif getLocationMultiboot() == '/dev/sdd1':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sdd1 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()
            elif getLocationMultiboot() == '/dev/sde1':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sde1 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()
            elif getLocationMultiboot() == '/dev/sdf1':
                    out = open('' + LinkNeoBoot + '/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n\n/bin/mount /dev/sdf1 ' + getNeoLocation() + '  \n\nexit 0')
                    out.close()
            system('chmod 755 ' + LinkNeoBoot + '/files/neo.sh')  

        if fileExists('/tmp/.init_reboot'):
            system('rm /tmp/.init_reboot')

        if fileExists('/.multinfo'):
            if not fileExists('/.control_ok'):
                if fileExists('/.control_boot_new_image'):  
                    os.system('rm -f /.control_boot_new_image; echo "Image uruchomione OK\nNie kasuj tego pliku. \n\nImage started OK\nDo not delete this file."  > /.control_ok ')          
                if not fileExists('/.control_boot_new_image'):  
                    os.system('echo "Image uruchomione OK\nNie kasuj tego pliku. \n\nImage started OK\nDo not delete this file."  > /.control_ok') 


    def DownloadImageOnline(self):				          	
            if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/ImageDownloader/download.py'):
                    message = _('Plugin ImageDownloader not installed!\nInstall plugin to download new image? \and---Continue ?---' )
                    ybox = self.session.openWithCallback(self.InstallImageDownloader, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Installation'))
            else:
                try:
                                from Plugins.Extensions.ImageDownloader.main import STBmodelsScreen
                                self.session.open(STBmodelsScreen)
                except Exception as e:
                                loggscrash = time.localtime(time.time())
                                LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                                mess = _('Sorry cannot open Image Downloader.\nAccess Fails with Error code 0x05.')
                                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    def InstallImageDownloader(self, yesno):		
        if yesno:
            if checkInternet():  
                cmd = 'mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -rf /tmp/*.ipk'
                system(cmd)
                if fileExists('/usr/bin/curl'):                    
                            os.system('cd /tmp; curl -O --ftp-ssl http://read.cba.pl/panel_extra/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk')
                if not fileExists('/tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'): 
                    if fileExists('/usr/bin/fullwget'):
                        cmd1 = 'cd /tmp; fullwget --no-check-certificate http://read.cba.pl/panel_extra/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'
                        system(cmd1)
                if not fileExists('/tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'): 
                    if fileExists('/usr/bin/wget'):            
                            os.system('cd /tmp; wget --no-check-certificate http://read.cba.pl/panel_extra/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk')
                if fileExists('/tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'): 
                    cmd2 = 'opkg install --force-overwrite --force-reinstall --force-downgrade /tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'
                    system(cmd2)
                    self.session.open(MessageBox, _('The plug-in has been successfully installed.'), MessageBox.TYPE_INFO, 5)
                    self.close()
                else:
                    self.session.open(MessageBox, _('The plugin not installed.\nAccess Fails with Error code 0x04.'), MessageBox.TYPE_INFO, 10)
                    self.close()            
            else:
                mess = _('Geen internet')
                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
        else:
                mess = _('Upload image files in zip formats to the ImagesUpload location.' )
                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)  

    def chackkernel(self):		
                            message = _('NeoBoot detected a kernel mismatch in flash, \nInstall a kernel for flash image??')
                            ybox = self.session.openWithCallback(self.updatekernel, MessageBox, message, MessageBox.TYPE_YESNO)
                            ybox.setTitle(_('Updating ... '))
    def pomoc(self):		
            try:
                    from Plugins.Extensions.NeoBoot.files.tools import Opis
                    self.session.open(Opis)
            except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    mess = _('Sorry cannot open neo menu.\nAccess Fails with Error code 0x02.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)            

    def ReinstallNeoBoot(self):		
        INSTALLbox = self.session.openWithCallback(self.reinstallboot, MessageBox, _('Select Yes to reinstall the neoboot.\n     NEOBOOT.'), MessageBox.TYPE_YESNO)
        INSTALLbox.setTitle(_('Reinstall neoboot'))
                
    def reinstallboot(self, answer):		        
        if answer is True:
            try:
                cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Please reinstall NeoBoot....\nPlease wait, done...\nrestart systemu...')
                cmd1 = 'cd ' + LinkNeoBoot + '/; rm ./bin/install; rm ./.location; rm ./files/mountpoint.sh; rm ./files/neo.sh; sleep 5; PATH=/sbin:/bin:/usr/sbin:/usr/bin; echo -n "Restarting E2... "; init 4; sleep 1; init 3 '                                                                                       
            except:                                 
                False
            self.session.open(Console, _('NeoBoot ARM....'), [cmd, cmd1])
            self.close()
        else:
            try:
                self.session.open(MessageBox, _('Resignation.'), MessageBox.TYPE_INFO, 4)
                self.close()
            except:
                False
         
    def close_exit(self):		
        system('touch /tmp/.init_reboot')
        if fileExists('/tmp/error_neo'): 
            try:
                cmd = 'cat /tmp/error_neo'
                cmd1 = ''
                self.session.openWithCallback(self.close, Console, _('NeoBoot....'), [cmd,
                         cmd1]) 
                self.close()

            except:
                False

        if not fileExists('/tmp/.finishdate') or not fileExists('/tmp/.nkod') or fileExists('/.multinfo') :
            if checkInternet():  
                pass
            else:
                mess = _('Geen internet')
                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                
        if not fileExists('/.multinfo'):            
            out = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'w' )
            out.write('Flash')
            out.close()
            self.close()
                        
        elif fileExists('/.multinfo'):            
            with open('/.multinfo', 'r'  ) as f:
                imagefile = f.readline().strip()
                f.close()
                out = open('%sImageBoot/.neonextboot'% getNeoLocation(), 'w' )
                out.write(imagefile)
                out.close()
        else:
            system('touch /tmp/.init_reboot')
            out = open('%sImageBoot/.neonextboot' % getNeoLocation() , 'w')
            out.write('Flash')
            out.close()
        self.close()
                        
    def ReinstallKernel(self):		
            try:
                    from Plugins.Extensions.NeoBoot.files.tools import ReinstallKernel
                    self.session.open(ReinstallKernel)
            except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    mess = _('Sorry cannot open neo menu Reinstall Kernel.\nAccess Fails with Error code 0x03.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)            
  
    def touch5(self):    
        if fileExists('/usr/lib/periodon/.kodn'):
            if getTestIn() == getTestOut():
                    pass
            else:
                    system('touch /tmp/guto')
        else:
                    system('touch /tmp/guto')
    def touch4(self):
        if fileExists('/usr/lib/periodon/.kodn'):
            pass
        else:
            if not fileExists('/tmp/guto'): 
                pass
            else:
                    system('touch /tmp/gutos')
    def touch7(self):
        if fileExists('/usr/lib/periodon/.kodn'):
            pass
        else:
            if not fileExists('/tmp/gutos'): 
                pass
            else:
                    system('touch /tmp/gutosi')
    def touch6(self):
        if fileExists('/usr/lib/periodon/.kodn'):
            pass
        else:
            if not fileExists('/tmp/gutosi'):
                pass 
            else:
                if not fileExists('/usr/lib/periodon'):
                    system('mkdir /usr/lib/periodon')
                else:
                    if getButtonPin() == 'pinok':
                        os.system('sleep 2; rm -f /tmp/gut*; date %s  > /usr/lib/periodon/.accessdate' % UPDATEDATE ) 
                        if fileExists('/usr/lib/periodon/.accessdate') and fileExists('/usr/lib/periodon/.kodn'):  
                                mess = _('Bravo! Neoboot vip full version activated OK!\nPlease restart your system E2.')
                                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                        elif not fileExists('/usr/lib/periodon/.accessdate'):
                                mess = _('VIP Access Activation Fails with Error code 0x10.')
                                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)                    
                        elif not fileExists('/usr/lib/periodon/.kodn'):                    
                                mess = _('VIP Access Activation Fails with Error code 0x20.')
                                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
    def touch9(self):
        if fileExists('/usr/lib/periodon/.kodn'):
            system('touch /tmp/gut1')
        else:
            if not fileExists('/tmp/gutosie'): 
                pass
            else:
                    system('touch /tmp/gutosiep')
    def touch8(self):
        if fileExists('/usr/lib/periodon/.kodn'):
            system('touch /tmp/gut2')
        else:
            if not fileExists('/tmp/gutosiep'): 
                pass
            else:
                    system('touch /tmp/gutosiepi')
    def touch0(self):                    
        if fileExists('/usr/lib/periodon/.kodn'):
            if not fileExists('/tmp/gut3'):
                system('touch /tmp/gut3')
            elif fileExists('/tmp/gut3'):
                system('rm -f /tmp/gut*; rm -f /usr/lib/periodon/.kodn')
                mess = _('Bravo - pin code removed!\nPlease re-enter your pin code.')
                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
            else:
                pass
        else:
            if not fileExists('/tmp/gutosiepi'): 
                pass
            else:
                    system('touch /tmp/gutosiepin')


#    def neoboot_update(self):		
#            mess = _('Updated unnecessary, you have the latest version. Please try again later.')
#            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    #Zablokowanie aktualizacji przez zmiane nazwy  neoboot_update na neoboot_update2 i likwidacja 3 lini hastagu wyzej  
    def neoboot_update(self):
        if checkInternet():  
        #if getTestInTime() == getTestOutTime() or getTestIn() != getTestOut():    
                #myerror = _('Sorry, this is not neoboot vip version.\nGet NEO-VIP version, more info press blue button.')
                #self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
        #else:
            if fileExists('/.multinfo'):
                    mess = _('Downloading available only from the image Flash.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
            else:
                    out = open('%sImageBoot/.neonextboot' % getNeoLocation() , 'w')
                    out.write('Flash')
                    out.close()
                    message = _('\n\n\n')
                    message += _('WARNING !: The update brings with it the risk of errors.\n')
                    message += _('Before upgrading it is recommended that you make a backup NeoBoot.\n')
                    message += _('Do you want to run the update now ?\n')
                    message += _('\n')
                    ybox = self.session.openWithCallback(self.chackupdate2, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('The download neoboot update.'))
        else:
                mess = _('Geen internet')
                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    def chackupdate2(self, yesno):		
        if yesno:
            self.chackupdate3()
        else:
            self.session.open(MessageBox, _('Canceled update.'), MessageBox.TYPE_INFO, 7)
                                           
    def chackupdate3(self):		                    
        if fileExists('/usr/bin/fullwget'):            
                            os.system('cd ' + LinkNeoBoot + ';fullwget --no-check-certificate https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt; sleep 3;cd /')           
        if not fileExists('' + LinkNeoBoot + '/ver.txt'):
                    if fileExists('/usr/bin/curl'):                    
                            os.system('cd ' + LinkNeoBoot + ';curl -O --ftp-ssl https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt;sleep 3;cd /')
        if not fileExists('' + LinkNeoBoot + '/ver.txt'):
                    if fileExists('/usr/bin/wget'):            
                            os.system('cd ' + LinkNeoBoot + ';wget --no-check-certificate https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt; sleep 3;cd /')      
        if fileExists('' + LinkNeoBoot + '/ver.txt'):
                mypath = ''
                version = open('' + LinkNeoBoot + '/ver.txt', 'r')
                mypath = float(version.read().strip())
                version.close()
                if float(UPDATEVERSION) != mypath:
                    message = _('NeoBoot has detected update.\nDo you want to update NeoBoota now ?')
                    ybox = self.session.openWithCallback(self.aktualizacjamboot, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Updating ... '))
                elif fileExists('' + LinkNeoBoot + '/ver.txt'):
                    os.system('rm ' + LinkNeoBoot + '/ver.txt')                    
                    if fileExists('' + LinkNeoBoot + '/wget-log'):
                        os.system('rm ' + LinkNeoBoot + '/wget-log') 
                    self.session.open(MessageBox, _('Updated unnecessary, you have the latest version. Please try again later.'), MessageBox.TYPE_INFO)
                else:
                    self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 10)
        else:
            if not fileExists('' + LinkNeoBoot + '/ver.txt'):
                self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 10)

    def aktualizacjamboot(self, yesno):		
        if yesno:
            if fileExists('/tmp/*.zip'):
                    os.system('rm /tmp/*.zip')
            if fileExists('/usr/bin/curl'):
                    os.system('cd /tmp; curl -O --ftp-ssl https://github.com/gutosie/neoboot/archive/main.zip; unzip -qn ./main.zip; sleep 2;cd /')
            if not fileExists('/tmp/neoboot-main/NeoBoot'):
                    if fileExists('/tmp/main.zip'):
                            os.system('rm -r /tmp/main.zip')            
                    if fileExists('/usr/bin/fullwget'):            
                            os.system('cd /tmp; fullwget --no-check-certificate https://github.com/gutosie/neoboot/archive/main.zip; unzip -qn ./main.zip; sleep 2;cd /')           
            if not fileExists('/tmp/neoboot-main/NeoBoot'):
                    if fileExists('/tmp/main.zip'):
                            os.system('rm -r /tmp/main.zip')            
                    if fileExists('/usr/bin/wget'):            
                            os.system('cd /tmp; rm ./*.zip; wget --no-check-certificate https://github.com/gutosie/neoboot/archive/main.zip; unzip -qn ./main.zip; sleep 2;cd / ')  
            if not fileExists('/tmp/neoboot-main/NeoBoot'):
                    self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 10)
            else:
                self.goUpdateNEO()
        else:
            os.system('rm -f ' + LinkNeoBoot + '/ver.txt')
            self.session.open(MessageBox, _('The update has been canceled.'), MessageBox.TYPE_INFO, 8)

    def goUpdateNEO(self):   
                if fileExists('' + LinkNeoBoot + '/wget-log'):
                        os.system('rm ' + LinkNeoBoot + '/wget-log')                                                                                                                                                                                                                                                                                                                                                    
                os.system('cd /tmp/; cp -rf ./neoboot-main/NeoBoot /usr/lib/enigma2/python/Plugins/Extensions; rm -rf /tmp/neoboot*;  rm ' + LinkNeoBoot + '/ver.txt; cd ' + LinkNeoBoot + '/; chmod 0755 ./bin/neoini*;  chmod 0755 ./ex_init.py; chmod 0755 ./tmpfiles/target/*; chmod 0755 ./files/userscript.sh; cd /; date %s  > /usr/lib/periodon/.accessdate' % UPDATEDATE)                    
                if getCPUtype() == 'MIPS':
                    os.system('cd ' + LinkNeoBoot + '/; cp -rf ./bin/neoinitmipsvu /sbin; chmod 755 /sbin/neoinitmipsvu; cp -rf ./bin/neoinitmips /sbin; chmod 755 /sbin/neoinitmips; cd')                                                                                  
                os.system('cd ' + LinkNeoBoot + '/; rm ./bin/install; rm -f ./files/testinout; rm ./files/mountpoint.sh; rm ./files/neo.sh; rm -f /usr/lib/periodon/.kodn; rm -f /tmp/.nkod; rm -rf /tmp/main.zip')
                restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('Completed update NeoBoot.\nYou need to restart the E2 and re-enter your pin code VIP!!!\nRestart now ?'), MessageBox.TYPE_YESNO)
                restartbox.setTitle(_('Restart GUI now ?'))


    def restartGUI(self, answer):		
        if answer is True: 
            os.system('rm -f ' + LinkNeoBoot + '/.location; rm -r ' + LinkNeoBoot + '/ubi_reader')     
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def MBBackup(self):		
            try:
                    from Plugins.Extensions.NeoBoot.files.tools import MBBackup
                    self.session.open(MBBackup)
            except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    mess = _('Sorry cannot open neo menu Backup.\nAccess Fails with Error code 0x60.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)            
    def MBRestore(self):		
            try:
                    from Plugins.Extensions.NeoBoot.files.tools import MBRestore
                    self.session.open(MBRestore)
            except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    mess = _('Sorry cannot open neo menu Restore.\nAccess Fails with Error code 0x61.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)            
                                                               
    def updateList(self):		
        self.list = []
        pluginpath = '' + LinkNeoBoot + ''
        f = open(pluginpath + '/.location', 'r')
        mypath = f.readline().strip()
        f.close()
        icon = 'dev_usb.png'
        if 'card' in mypath or 'sd' in mypath:
            icon = 'dev_sd.png'
        elif 'ntfs' in mypath:
            icon = 'dev_sd.png'
        elif 'hdd' in mypath:
            icon = 'dev_hdd.png'
        elif 'cf' in mypath:
            icon = 'dev_cf.png'
        elif 'ssd' in mypath:
            icon = 'dev_ssd.png'
           
        icon = pluginpath + '/images/' + icon
        png = LoadPixmap(icon)
        self['device_icon'].instance.setPixmap(png)                               
        linesdevice = open('' + LinkNeoBoot + '/.location', 'r').readlines()
        deviceneo = linesdevice[0][0:-1]
        device = deviceneo

        ustot = usfree = usperc = ''
        rc = system('df > /tmp/memoryinfo.tmp')
        if fileExists('/tmp/memoryinfo.tmp'):
            f = open('/tmp/memoryinfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == device:               
                    if totsp == 5:
                        ustot = parts[1]
                        usfree = parts[3]
                        usperc = parts[4]
                    else:
                        ustot = 'N/A   '
                        usfree = parts[2]
                        usperc = parts[3]
                    break

            f.close()
            os.remove('/tmp/memoryinfo.tmp')

        perc = int(usperc[0:-1])
#        perc = int()  # jak czasami robi error to odhaszowac i zahaszowac wyzej      
        self['progreso'].setValue(perc)
        green = '#00389416'
        red = '#00ff2525'
        yellow = '#00ffe875'
        orange = '#00ff7f50'
        if perc < 30:
                color = green
        elif perc < 60:
                color = yellow
        elif perc < 80:
                color = orange
        else:
                color = red
        try:
            from skin import parseColor
            self['label13'].instance.setForegroundColor(parseColor(color))
            self['label15'].instance.setForegroundColor(parseColor(color))
            self['progreso'].instance.setForegroundColor(parseColor(color))
        except:
            pass

        self.availablespace = usfree[0:-3]
        
        strview = _('Used: ') + usperc + _('   \n   Available: ') + usfree[0:-3] + ' MB'
        self['label3'].setText(strview)

        strview2 = _('Free Space : ') + usfree[0:-3] + ' MB'
        self['label11'].setText(strview2)

        strview1 = _('Capacity : ') + usperc +  _(' Full')                  
        self['label18'].setText(strview1)

        try:
            f2 = open('%sImageBoot/.neonextboot', 'r' % getNeoLocation())
            mypath2 = f2.readline().strip()
            f2.close()
        except:
            mypath2 = 'Flash'

        if mypath2 == 'Flash':
            image = getImageDistroN()
            writefile = open('%sImageBoot/.Flash' % getNeoLocation(), 'w')
            writefile.write(image)
            writefile.close()

        elif fileExists('%sImageBoot/.Flash' % getNeoLocation()):
            f = open('%sImageBoot/.Flash', 'r' % getNeoLocation())
            image = f.readline().strip()
            f.close()

        image = ' [' + image + ']'
        self.list.append('Flash' + image)
        self['label5'].setText(mypath)

        if fileExists('/.multinfo'):
            f2 = open('/.multinfo', 'r')
            mypath3 = f2.readline().strip()
            f2.close()
            self['label6'].setText(mypath3)
        else:
            f2 = open('%sImageBoot/.neonextboot' % getNeoLocation() , 'r' )
            mypath3 = f2.readline().strip()
            f2.close()
            self['label6'].setText(mypath3)
        mypath = ('%sImageBoot' % getNeoLocation())
        myimages = listdir(mypath)
        for fil in myimages:
            if os.path.isdir(os.path.join(mypath, fil)):
                self.list.append(fil)

        self['label7'].setText(str(len(self.list) - 1))
        self['config'].setList(self.list)

        strview = PLUGINVERSION 
        self['label9'].setText(strview)

        KERNELVERSION = getKernelImageVersion()
        strview = KERNELVERSION  
        self['label20'].setText(strview)

        self['label17'].setText(readline('/etc/hostname'))         
        self['label19'].setText(readline('%sImagesUpload/.kernel/used_flash_kernel' % getNeoLocation() ))

        strview = UPDATEVERSION
        self['label10'].setText(strview)

    def mytools(self):                     
        if not fileExists('/.multinfo'):
            if getTestIn() == getTestOut():
                if getAccessN() == '1234':
                    if (getSupportedTuners()) == (getBoxHostName()):                             	
                        try:      
                            from Plugins.Extensions.NeoBoot.files.tools import MBTools                    
                            self.session.open(MBTools)            	
                    #except:
                        except Exception as e:
                            loggscrash = time.localtime(time.time())
                            LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                            mess = _('Sorry cannot open neo menu. Access Fails with Error code 0x50.')
                            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                    else:
                                mess = _('Sorry cannot open neo menu. Access Fails with Error code 0x60.')
                                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                else:
                    myerror = _('Sorry, this is not neoboot vip version.\nGet NEO-VIP version, more info press blue button.')
                    self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)                

            else:
                myerror = _('Sorry, this is not neoboot vip version.\nGet NEO-VIP version, more info press blue button or try to update.')
                self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
        else:
                        try:
                            from Plugins.Extensions.NeoBoot.files.tools import MBTools
                            self.session.open(MBTools)
                        except Exception as e:
                            loggscrash = time.localtime(time.time())
                            LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                            mess = _('Sorry cannot open neo menu. Access Fails with Error code 0x50.')
                            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                            
    def removeIMG(self):		
        self.mysel = self['config'].getCurrent()
        if 'Flash' in self.mysel:
            self.mysel = 'Flash'
        if self.mysel:
            f = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'r')
            mypath = f.readline().strip()
            f.close()
            try:
                if fileExists('/.multinfo'):
                     self.session.open(MessageBox, _('Sorry you can delete only from the image Flash.'), MessageBox.TYPE_INFO, 5)
                elif self.mysel == 'Flash':
                    self.session.open(MessageBox, _('Sorry you cannot delete Flash image'), MessageBox.TYPE_INFO, 5)
                elif mypath == self.mysel:
                    self.session.open(MessageBox, _('Sorry you cannot delete the image currently booted from.'), MessageBox.TYPE_INFO, 5)
                else:

                    out = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'w' )
                    out.write('Flash')
                    out.close()
                    message = _('Delete the selected image - ') + self.mysel + _('\nDelete ?')
                    ybox = self.session.openWithCallback(self.RemoveIMAGE, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Delete Confirmation'))
            except:
                print ("no image to remove")

        else:
            self.mysel

    def up(self):		
        self.list = []
        self['config'].setList(self.list)
        self.updateList()

    def up2(self):		
        try:
            self.list = []
            self['config'].setList(self.list)
            self.updateList()
        except:
            print (" ")

    def RemoveIMAGE(self, yesno):		
        if yesno:
            cmd = _("echo -e 'Deleting in progress...\n'")
            cmd1 = 'chattr -i %sImageBoot/' % getNeoLocation() + self.mysel
            cmd2 = 'rm -r %sImageBoot/' % getNeoLocation() + self.mysel
            self.session.openWithCallback(self.up, Console, _('NeoBoot: Deleting Image'), [cmd, cmd1, cmd2])
        else:
            self.session.open(MessageBox, _('Removing canceled!'), MessageBox.TYPE_INFO)


    def ImageInstall(self):        
        if not fileExists('/.multinfo'):
            if getAccessN() != '1234':   #%s' % UPDATEVERSION
                count = 0
                for fn in listdir('' + getNeoLocation() + '/ImageBoot'):
                    dirfile = '' + getNeoLocation() + '/ImageBoot/' + fn
                    if os_isdir(dirfile):
                        count = count + 1

                if count > 1:
                    myerror = _('Sorry, you can install up to 2 images, this is not neoboot vip version.\nGet unlimited image installations in VIP version')
                    self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
                elif int(self.availablespace) < 500:    
                    myerror = _('Not enough free space on /media/ !!\nYou need at least 500Mb free space.\n\nExit plugin.')
                    self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
                else:
                        self.ImageInstallTestOK()
            else:
                if getTestIn() == getTestOut():
                    self.ImageInstallTestOK()
                else:
                    myerror = _('Sorry, this is not neoboot vip version.\nGet NEO-VIP version, more info press blue button or try to update.')
                    self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
        else:
                        self.ImageInstallTestOK()        

    def ImageInstallTestOK(self):
            if int(self.availablespace) < 500:
                myerror = _('Not enough free space on /media/ !!\nYou need at least 500Mb free space.\n\nExit plugin.')
                self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
            else:
                if (getSupportedTuners()) == (getBoxHostName()):
                    try:
                        self.GOImageInstall()
                    except Exception as e:
                        loggscrash = time.localtime(time.time())
                        LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                        mess = _('Sorry, cannot open neo menu image install. Access Fails with Error code 0x70.')
                        self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                else:
                    mess = _('Your receiver is not on the list of supported tuners.\nAccess error with error code 0x71.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    def GOImageInstall(self):		
        if fileExists('/.multinfo'):
                    message = _('Installing new neoboot software, only recommended from Flash!!!\n---Continue ?---')
                    ybox = self.session.openWithCallback(self.installation_image, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Installation'))
        else:
                    message = _('Installation from Flash!!!\n---Continue ?---')
                    ybox = self.session.openWithCallback(self.installation_image, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Installation new image. '))

    def installation_image(self, yesno):
        if yesno:
                self.extractImage()        
        else:
                self.messagebox = self.session.open(MessageBox, _('It is recommended to install new software only from a flash system.\n---NEOBOOT EXIT---'), MessageBox.TYPE_INFO, 10)
                self.close()
                
    def extractImage(self):
        if fileExists('%sImageBoot/.without_copying' % getNeoLocation()):
            system('rm -f %sImageBoot/.without_copying' % getNeoLocation())

        if not os.path.exists('%sImagesUpload' % getNeoLocation()):
            system('mkdir %sImagesUpload' % getNeoLocation())

        images = False
        myimages=listdir('%sImagesUpload' % getNeoLocation())
        print (myimages)
        for fil in myimages:
            if fil.endswith(".zip"):
                images=True
                break
            if os.path.exists('%sImagesUpload/*zip' % getNeoLocation()):
                images=True
                break
            if os.path.exists('%sImagesUpload/*.tar.bz2' % getNeoLocation()):
                images=True
                break
            if fil.endswith(".tar.xz"):
                images=True
                break
            if fil.endswith(".nfi"):
                images=True
                break
            else:
                images=False
        if images is True:
            self.ImageTrue()
        else:
                self.DownloaderImage()

    def ImageTrue(self):
                    try:
                        from Plugins.Extensions.NeoBoot.unpack import InstallImage
                        self.session.open(InstallImage)
                    except Exception as e:
                        loggscrash = time.localtime(time.time())
                        LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                        mess = _('Sorry, cannot open instalation menu.\nAccess error with error code 0x72.')
                        self.session.open(MessageBox, mess, MessageBox.TYPE_INFO) 
                        
    def DownloaderImage(self):
            if not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/ImageDownloader/download.py'):
                    message = (_('The %sImagesUpload directory is EMPTY!!!\nInstall the plugin to download new image online ?\n --- Continue? ---') % getNeoLocation() ) 
                    ybox = self.session.openWithCallback(self.ImageDownloader, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Installation'))
            elif fileExists('/usr/lib/python3.8') and fileExists('/.multinfo'):
                self.session.open(MessageBox, _('Sorry, cannot open neo menu install image.'), type=MessageBox.TYPE_ERROR) 
            else:
                message = (_('Catalog %sImagesUpload directory is empty\nPlease upload the image files in zip or nfi formats to install') % getNeoLocation() )
                self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
    
    def ImageDownloader(self, yesno):		
        if checkInternet():  
            if yesno:
                cmd = 'mkdir /tmp/install; touch /tmp/install/plugin.txt; rm -rf /tmp/*.ipk'
                system(cmd)
                if fileExists('/usr/bin/fullwget'):            
                            os.system('cd /tmp; wget http://read.cba.pl/panel_extra/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk')           
                if not fileExists('/tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'):
                    if fileExists('/usr/bin/curl'):                    
                            os.system('sync; cd /tmp; curl -O --ftp-ssl http://read.cba.pl/panel_extra/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk')
                if not fileExists('/tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'):
                    if fileExists('/usr/bin/wget'):            
                            os.system('cd /tmp;rm ./*.zip; wget --no-check-certificate http://read.cba.pl/panel_extra/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk')  
                if not fileExists('/tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'):
                        self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 10)
                else:
                    cmd2 = 'opkg install --force-overwrite --force-reinstall --force-downgrade /tmp/enigma2-plugin-extensions-imagedownloader_2.6_all.ipk'
                    system(cmd2)
                    self.session.open(MessageBox, _('The plug-in has been successfully installed.'), MessageBox.TYPE_INFO, 5)
                    self.close()
            else:
                mess = (_('Directory %sImagesUpload  is empty\nPlease upload the image files in zip or nfi formats to install') % getNeoLocation() )
                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)  
        else:
                mess = _('Geen internet')
                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    def bootIMG(self):
        if not fileExists('/.multinfo'):
            if getAccessN() == '1234':
                self.bootIMG2()
            else:
                    myerror = _('Sorry, this is not neoboot vip version.\nGet NEO-VIP version, more info press blue button.')
                    self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
        else:
            self.bootIMG2()       
        
    def bootIMG2(self):  		       
                self.mysel = self['config'].getCurrent()
                if 'Flash' in self.mysel:
                    self.mysel = 'Flash'
                if self.mysel:
                    out = open('' + getNeoLocation() + 'ImageBoot/.neonextboot', 'w' )
                    out.write(self.mysel)
                    out.close()
 
                    if getImageNeoBoot() != "Flash":
                        if not fileExists('%sImageBoot/%s/.control_ok' % ( getNeoLocation(),  getImageNeoBoot())):
                            message = _('After successful launch of the selected software\nyou must run the neoboot plugin\nif the software does not start or neoboot is not confirmed\nthe system will return to the internal flash memory\n\nPress OK or exit on the remote control to continue...' )
                            ybox = self.session.openWithCallback(self.StartReboot, MessageBox, message, MessageBox.TYPE_YESNO)
                            ybox.setTitle(_('First start of software'))
                        else:
                            try:
                                from Plugins.Extensions.NeoBoot.run import StartImage
                                self.session.open(StartImage)
                            except Exception as e:
                                loggscrash = time.localtime(time.time())
                                LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                                mess = _('Sorry cannot open run.py file - Access Fails with Error code 0x30.')
                                self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
                    else:
                        try:
                                from Plugins.Extensions.NeoBoot.run import StartImage
                                self.session.open(StartImage)
                        except Exception as e:
                            loggscrash = time.localtime(time.time())
                            LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                            mess = _('Sorry cannot open run file - Access Fails with Error code 0x40.')
                            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)                            
                            
    def StartReboot(self, yesno):		
        if yesno:
                try:
                        from Plugins.Extensions.NeoBoot.run import StartImage
                        self.session.open(StartImage)
                except Exception as e:
                    loggscrash = time.localtime(time.time())
                    LogCrashGS('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (loggscrash.tm_mday, loggscrash.tm_mon, loggscrash.tm_year, loggscrash.tm_hour, loggscrash.tm_min, loggscrash.tm_sec, str(e)))
                    mess = _('Sorry cannot open neo menu. Hymmm...\nAccess Fails with Error code 0x73.')
                    self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)                
        else:
            self.close()

    def myClose(self, message):		
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()


def readline(filename, iferror = ''):
    if iferror[:3] == 'or:':
      data = iferror[3:]
    else:
      data = iferror
    try:
        if os.path.exists(filename):
            with open(filename) as f:
                data = f.readline().strip()
                f.close()
    except Exception:
        PrintException()
    return data

def checkInternet():
    if fileExists('/usr/lib/python3.8'):                     
        return True
    else:
        import urllib2, urllib
        try:
            response = urllib2.urlopen("http://google.com", None, 5)
            response.close()
        except urllib2.HTTPError:
            return False
        except urllib2.URLError:
            return False
        except socket.timeout:
            return False
        else:
            return True

def checkimage():
    mycheck = False
    if not fileExists('/proc/stb/info') or not fileExists('' + LinkNeoBoot + '/neoskins/neo/neo_skin.py') or not fileExists('' + LinkNeoBoot + '/bin/utilsbh') or not fileExists('' + LinkNeoBoot + '/stbinfo.cfg'): 
        mycheck = False
    else:
        mycheck = True
    return mycheck

def main(session, **kwargs):
    vip = checkimage()
    if vip == 1:
        if not fileExists('' + LinkNeoBoot + '/.location'):
            pass
        else:
            if not fileExists('%sImageBoot/.version' % getNeoLocation()):
                if fileExists('' + LinkNeoBoot + '/files/mountpoint.sh'):
                    os.system('chmod 0755 ' + LinkNeoBoot + '/files/mountpoint.sh; ' + LinkNeoBoot + '/files/mountpoint.sh')
        if not fileExists('/.multinfo') and fileExists('' + LinkNeoBoot + '/.location'):
            if checkInternet():
                if not os.path.exists('/tmp/.finishdate'):
                                        os.system('date "+%Y%m%d"  > /tmp/.finishdate')
                if fileExists('/tmp/.nkod'):
                                        pass
                else: 
                                        if not fileExists('/tmp/ver.txt'):
                                                if fileExists('/usr/bin/curl'):                    
                                                        os.system('cd /tmp; curl -O --ftp-ssl https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt; cd /')
                                        if not fileExists('/tmp/ver.txt'):
                                                if fileExists('/usr/bin/wget'):            
                                                        os.system('cd /tmp; wget --no-check-certificate https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt; cd /')         
                                        if not fileExists('/tmp/ver.txt'):
                                                if fileExists('/usr/bin/fullwget'):            
                                                        os.system('cd /tmp; fullwget --no-check-certificate https://raw.githubusercontent.com/gutosie/neoboot/master/ver.txt; cd /')                                       
                                        if fileExists('/tmp/ver.txt'):
                                                        os.system('mv /tmp/ver.txt /tmp/.nkod ;cd /')
                                        else:
                                                        os.system(_('echo %s  > /tmp/.nkod') % PLUGINVERSION)
            from Plugins.Extensions.NeoBoot.files.stbbranding import getCheckInstal1, getCheckInstal2, getCheckInstal3
            if fileExists('/tmp/error_neo') :
                if fileExists('/tmp/error_neo'):
                    os.system('rm -f /tmp/error_neo')
                if getCheckInstal1() == '1':
                    os.system('echo "\nNeoboot installation errors 1:\nfile install is error - 1\n"  >> /tmp/error_neo')
                    session.open(MessageBox, _('Neoboot plugin installed with ERRORS! Not work properly! The error number is 1'), type=MessageBox.TYPE_ERROR)
                if getCheckInstal2() == '2':
                    os.system('echo "\nNeoboot installation errors 2:\nfile .location is error - 2\n"  >> /tmp/error_neo')
                    session.open(MessageBox, _('Neoboot plugin installed with ERRORS! Not work properly! The error number is 2'), type=MessageBox.TYPE_ERROR)
                if getCheckInstal3() == '3':
                    os.system('echo "\nNeoboot installation errors 3:\nfile neo.sh is error - 3\n"  >> /tmp/error_neo')
                    session.open(MessageBox, _('Neoboot plugin installed with ERRORS! Not work properly! The error number is 3'), type=MessageBox.TYPE_ERROR)
            if not fileExists('/usr/lib/periodon/.kodn'):
                        session.open(MessageBox, _('Get a free test to the full vip version.'), type=MessageBox.TYPE_ERROR)
            elif fileExists('/usr/lib/periodon/.kodn') and fileExists('/tmp/.nkod'):
                        if getTestToTest() != UPDATEVERSION:
                                session.open(MessageBox, _('New version update neoboot is available!\nPlease upgrade your flash plugin.'), type=MessageBox.TYPE_ERROR)
            if not fileExists('/usr/lib/periodon/.accessdate'):       #timeoff
                                session.open(MessageBox, _('VIP access error. Reinstall the plugin.'), type=MessageBox.TYPE_ERROR)
            if getAccesDate() == 'timeoff':       #timeoff
                                session.open(MessageBox, _('Neoboot vip version has expired, please re-access.'), type=MessageBox.TYPE_ERROR)
                                
        version = 0
        if fileExists('%sImageBoot/.version' % getNeoLocation()):
            f = open('%sImageBoot/.version' % getNeoLocation())
            version = float(f.read())
            f.close()

        if fileExists('' + LinkNeoBoot + '/.location') and fileExists('%sImageBoot/.neonextboot' % getNeoLocation()):
                f2 = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'r' )
                mypath2 = f2.readline().strip()
                f2.close()                 
                if mypath2 != 'Flash' or mypath2 == 'Flash' and checkimage():
                
                    if fileExists('/.multinfo'):
                                    session.open(NeoBootImageChoose)                                
                    else:                                   
                        if float(PLUGINVERSION) != version:
                                session.open(MyUpgrade)
                        else:
                                session.open(NeoBootImageChoose)
                else:
                    session.open(MessageBox, _('Sorry, Unable to install, bad satellite receiver or you do not have the full plug-in version\n The full version of the NEO VIP plugin is on address:\nkrzysztofgutosie@.gmail.com'), type=MessageBox.TYPE_ERROR)
        else:
            if (getSupportedTuners()) == (getBoxHostName()):
                            session.open(NeoBootInstallation)
            else:
                    session.open(MessageBox, _('Sorry cannot open neo menu. Not supported tuners. '), type=MessageBox.TYPE_ERROR)
    else:
            session.open(MessageBox, (_('Sorry, Unable to install, bad satellite receiver or you do not have the full plug-in version\n\nThe full version of the NEO VIP plugin is on address:\nkrzysztofgutosie@.gmail.com')), type=MessageBox.TYPE_ERROR)
            
def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('NeoBOOT'),
          main,
          'neo_boot',
          1)]
    return []

from Plugins.Plugin import PluginDescriptor

def Plugins(**kwargs):
    if isFHD():
        list = [PluginDescriptor(name='NeoBoot', description='NeoBoot', where=PluginDescriptor.WHERE_MENU, fnc=menu), PluginDescriptor(name='NeoBoot', description=_('Installing multiple images'), icon='neo_fhd.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
        list.append(PluginDescriptor(name=_('NEOBOOT'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main))
    else:
        list = [PluginDescriptor(name='NeoBoot', description='NeoBoot', where=PluginDescriptor.WHERE_MENU, fnc=menu), PluginDescriptor(name='NeoBoot', description=_('Installing multiple images'), icon='neo_hd.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
        list.append(PluginDescriptor(name=_('NEOBOOT'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main))
    return list

####################### _q(-_-)p_ gutosie _q(-_-)p_ #######################

# -*- coding: utf-8 -*-

#from Plugins.Extensions.NeoBoot.__init__ import _
import sys
import os
import time
from Tools.Directories import fileExists, SCOPE_PLUGINS
LinkNeoBoot = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'

LogFileObj = None

def Log(param=''):
    global LogFileObj
    #first close object if exists
    if param.lower() in ['open', 'write', 'append', 'close']:
        if LogFileObj is not None:
            LogFileObj.close()
            if LogFileObj.closed:
                LogFileObj = None
                try:
                    with open('/tmp/NeoBoot.log', 'a') as f:
                        f.write('LogFile closed properly\n')
                        f.close()
                except Exception:
                    print("ERROR closing LogFile!!!")
            else:
                print("ERROR closing LogFile!!!")
    #second create object if does not exist
    if LogFileObj is None:
        if param.lower() in ['open', 'write']:
            LogFileObj = open(LogFile, "w")
        elif param.lower() in ['append']:
            LogFileObj = open(LogFile, "a")
        elif param.lower() in ['close']:
            pass
    elif param.lower() in ['flush']:
        LogFileObj.flush()
    return LogFileObj


def clearMemory():
    with open("/proc/sys/vm/drop_caches", "w") as f:
        f.write("1\n")
        f.close()


def LogCrashGS(line):
	log_file = open('%sImageBoot/neoboot.log' % getNeoLocation(), 'a')
	log_file.write(line)
	log_file.close()


def fileCheck(f, mode='r'):
    return fileExists(f, mode) and f

#		if not IsImageName():
#			from Components.PluginComponent import plugins
#			plugins.reloadPlugins()


def IsImageName():
	if fileExists("/etc/issue"):
		for line in open("/etc/issue"):
			if "BlackHole" in line or "vuplus" in line:
				return True
	return False


def mountp():
	pathmp = []
	if os.path.isfile('/proc/mounts'):
		for line in open('/proc/mounts'):
			if '/dev/sd' in line or '/dev/disk/by-uuid/' in line or '/dev/mmc' in line or '/dev/mtdblock' in line:
				pathmp.append(line.split()[1].replace('\\040', ' ') + '/')
	pathmp.append('/usr/share/enigma2/')
	pathmp.append('/etc/enigma2/')
	pathmp.append('/tmp/')
	return pathmp


def getSupportedTuners():
    supportedT = ''
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/stbinfo.cfg'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/stbinfo.cfg', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find("%s" % getBoxHostName()) != -1:
            supportedT = '%s' % getBoxHostName()
    return supportedT


def getFreespace(dev):
    statdev = os.statvfs(dev)
    space = statdev.f_bavail * statdev.f_frsize / 1024
    print("[NeoBoot] Free space on %s = %i kilobytes") % (dev, space)
    return space

#check install


def getCheckInstal1():
    neocheckinstal = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install', 'r') as f:
            lines1 = f.read()
            f.close()
        if not lines1.find('/dev/') != -1:
            neocheckinstal = '1'
    return neocheckinstal


def getCheckInstal2():
    neocheckinstal = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'r') as f:
            lines2 = f.read()
            f.close()
        if not lines2.find('/media/') != -1:
            neocheckinstal = '2'
    return neocheckinstal


def getCheckInstal3():
    neocheckinstal = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'r') as f:
            lines3 = f.read()
            f.close()
        if not lines3.find('/bin/mount') != -1:
            neocheckinstal = '3'

    return neocheckinstal

#check imageATV


def getImageATv():
    atvimage = 'UNKNOWN'
    if os.path.exists('/etc/issue.net'):
        with open('/etc/issue.net', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('openatv') != -1:
            atvimage = 'okfeedCAMatv'
    return atvimage

#check install


def getNeoLocation():
    locatinoneo = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'r') as f:
            locatino = f.readline().strip()
            f.close()
        if os.path.exists('/media/hdd/ImageBoot'):
            locatinoneo = '/media/hdd/'
        elif os.path.exists('/media/usb/ImageBoot'):
            locatinoneo = '/media/usb/'
        else:
            locatinoneo = locatino    		
    return locatinoneo


#check ext
def getFormat():
    neoformat = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('ext2') != -1:
            neoformat = 'ext2'
        elif lines.find('ext3') != -1:
            neoformat = 'ext3'
        elif lines.find('ext4') != -1:
            neoformat = 'ext4'
        elif lines.find('nfs') != -1:
            neoformat = 'nfs'

    return neoformat


def getNEO_filesystems():
    neo_filesystems = 'UNKNOWN'
    if os.path.exists('/tmp/.neo_format'):
        with open('/tmp/.neo_format', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('ext2') != -1:
            neo_filesystems = '1'
        elif lines.find('ext3') != -1:
            neo_filesystems = '1'
        elif lines.find('ext4') != -1:
            neo_filesystems = '1'
        elif lines.find('nfs') != -1:
            neo_filesystems = '1'

    return neo_filesystems

#typ procesora arm lub mips


def getCPUtype():
    cpu = 'UNKNOWN'
    if os.path.exists('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('ARMv7') != -1:
            cpu = 'ARMv7'
        elif lines.find('mips') != -1:
            cpu = 'MIPS'
    return cpu

#check install


def getFSTAB():
    install = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/reading_blkid'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/reading_blkid', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('UUID') != -1:
            install = 'UUID'
        elif not lines.find('UUID') != -1:
            install = 'NOUUID'
    return install


def getFSTAB2():
    install = 'UNKNOWN'
    if os.path.exists('/etc/fstab'):
        with open('/etc/fstab', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('UUID') != -1:
            install = 'OKinstall'
        elif not lines.find('UUID') != -1:
            install = 'NOUUID'
    return install


def getINSTALLNeo():
    neoinstall = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/installNeo'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/installNeo', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/dev/sda1') != -1:
            neoinstall = '/dev/sda1'
        elif lines.find('/dev/sda2') != -1:
            neoinstall = '/dev/sda2'
        elif lines.find('/dev/sdb1') != -1:
            neoinstall = '/dev/sdb1'
        elif lines.find('/dev/sdb2') != -1:
            neoinstall = '/dev/sdb2'
        elif lines.find('/dev/sdc1') != -1:
            neoinstall = '/dev/sdc1'
        elif lines.find('/dev/sdd1') != -1:
            neoinstall = '/dev/sdd1'
        elif lines.find('/dev/sde1') != -1:
            neoinstall = '/dev/sde1'
        elif lines.find('/dev/sdf1') != -1:
            neoinstall = '/dev/sdf1'

    return neoinstall


def getLocationMultiboot():
    LocationMultiboot = 'UNKNOWN'
    if os.path.exists('/media/sda1/ImageBoot'):
            LocationMultiboot = '/dev/sda1'
    if os.path.exists('/media/sda2/ImageBoot'):
            LocationMultiboot = '/dev/sda2'
    if os.path.exists('/media/sdb1/ImageBoot'):
            LocationMultiboot = '/dev/sdb1'
    if os.path.exists('/media/sdb2/ImageBoot'):
            LocationMultiboot = '/dev/sdb2'
    if os.path.exists('/media/sdc1/ImageBoot'):
            LocationMultiboot = '/dev/sdc1'
    if os.path.exists('/media/sdd1/ImageBoot'):
            LocationMultiboot = '/dev/sdd1'
    if os.path.exists('/media/sde1/ImageBoot'):
            LocationMultiboot = '/dev/sde1'
    if os.path.exists('/media/sdf1/ImageBoot'):
            LocationMultiboot = '/dev/sdf1'

    return LocationMultiboot


def getLabelDisck():
    label = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/reading_blkid'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/reading_blkid', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('LABEL=') != -1:
            label = 'LABEL='
    return label

#checking device  neo


def getNeoMountDisc():
    lines_mount = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines_mount = f.read()
            f.close()

    return lines_mount
    

def getNeoMount():
    neo = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/dev/sda1 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sda1'
        elif lines.find('/dev/sdb1 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sdb1'
        elif lines.find('/dev/sda2 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sda2'
        elif lines.find('/dev/sdb2 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sdb2'
        elif lines.find('/dev/sdc1 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sdc1'
        elif lines.find('/dev/sdd1 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sdd1'
        elif lines.find('/dev/sde1 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sde1'
        elif lines.find('/dev/sdf1 /media/hdd') != -1:
            neo = 'hdd_install_/dev/sdf1'

    return neo
    
    
def getNeoMount2():
    neo = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/dev/sda1 /media/usb') != -1:
            neo = 'usb_install_/dev/sda1'
        elif lines.find('/dev/sdb1 /media/usb') != -1:
            neo = 'usb_install_/dev/sdb1'
        elif lines.find('/dev/sdb2 /media/usb') != -1:
            neo = 'usb_install_/dev/sdb2'
        elif lines.find('/dev/sdc1 /media/usb') != -1:
            neo = 'usb_install_/dev/sdc1'
        elif lines.find('/dev/sdd1 /media/usb') != -1:
            neo = 'usb_install_/dev/sdd1'
        elif lines.find('/dev/sde1 /media/usb') != -1:
            neo = 'usb_install_/dev/sde1'
        elif lines.find('/dev/sdf1 /media/usb') != -1:
            neo = 'usb_install_/dev/sdf1'
        elif lines.find('/dev/sda1 /media/usb2') != -1:
            neo = 'usb_install_/dev/sda1'
        elif lines.find('/dev/sdb1 /media/usb2') != -1:
            neo = 'usb_install_/dev/sdb1'
        elif lines.find('/dev/sdb2 /media/usb2') != -1:
            neo = 'usb_install_/dev/sdb2'
        elif lines.find('/dev/sdc1 /media/usb2') != -1:
            neo = 'usb_install_/dev/sdc1'
        elif lines.find('/dev/sdd1 /media/usb2') != -1:
            neo = 'usb_install_/dev/sdd1'
        elif lines.find('/dev/sde1 /media/usb2') != -1:
            neo = 'usb_install_/dev/sde1'
        elif lines.find('/dev/sdf1 /media/usb2') != -1:
            neo = 'usb_install_/dev/sdf1'

    return neo


def getNeoMount3():
    neo = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/dev/sda1 /media/cf') != -1:
            neo = 'cf_install_/dev/sda1'
        elif lines.find('/dev/sdb1 /media/cf') != -1:
            neo = 'cf_install_/dev/sdb1'
    return neo


def getNeoMount4():
    neo = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/dev/sda1 /media/card') != -1:
            neo = 'card_install_/dev/sda1'
        elif lines.find('/dev/sdb1 /media/card') != -1:
            neo = 'card_install_/dev/sdb1'
    return neo


def getNeoMount5():
    neo = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/dev/sda1 /media/mmc') != -1:
            neo = 'mmc_install_/dev/sda1'
        elif lines.find('/dev/sdb1 /media/mmc') != -1:
            neo = 'mmc_install_/dev/sdb1'
    return neo


#zwraca typ chipa prcesora
def getCPUSoC():
    chipset = 'UNKNOWN'
    if os.path.exists('/proc/stb/info/chipset'):
        with open('/proc/stb/info/chipset', 'r') as f:
            chipset = f.readline().strip()
            f.close()
        if chipset == '7405(with 3D)':
                chipset = '7405'
    return chipset


def getCPUSoCModel():
    devicetree = 'UNKNOWN'
    if os.path.exists('/proc/device-tree/model'):
        with open('/proc/device-tree/model', 'r') as f:
            devicetree = f.readline().strip()
            f.close()
    return devicetree

#zwraca wybrane image w neoboot do uruchomienia


def getImageNeoBoot():
    imagefile = 'UNKNOWN'
    if os.path.exists('%sImageBoot/.neonextboot' % getNeoLocation()):
        with open('%sImageBoot/.neonextboot' % getNeoLocation(), 'r') as f:
            imagefile = f.readline().strip()
            f.close()
    return imagefile

#zwraca model vuplus


def getBoxVuModel():
    vumodel = 'UNKNOWN'
    if fileExists("/proc/stb/info/vumodel") and not fileExists("/proc/stb/info/boxtype"):
        with open('/proc/stb/info/vumodel', 'r') as f:
            vumodel = f.readline().strip()
            f.close()
    elif fileExists("/proc/stb/info/boxtype") and not fileExists("/proc/stb/info/vumodel"):
        with open('/proc/stb/info/boxtype', 'r') as f:
            vumodel = f.readline().strip()
            f.close()
    return vumodel


def getVuModel():
    if fileExists("/proc/stb/info/vumodel") and not fileExists("/proc/stb/info/boxtype"):
        brand = "Vu+"
        f = open("/proc/stb/info/vumodel", 'r')
        procmodel = f.readline().strip()
        f.close()
        model = procmodel.title().replace("olose", "olo SE").replace("olo2se", "olo2 SE").replace("2", "²")
    return model

#zwraca nazwe stb z pliku hostname


def getBoxHostName():
    if os.path.exists('/etc/hostname'):
        with open('/etc/hostname', 'r') as f:
            myboxname = f.readline().strip()
            f.close()
    return myboxname

#zwraca vuplus/vumodel


def getTunerModel(): #< neoboot.py
    BOX_NAME = ''
    if os.path.isfile('/proc/stb/info/vumodel') and not os.path.isfile("/proc/stb/info/boxtype"):
        BOX_NAME = open('/proc/stb/info/vumodel').read().strip()
        ImageFolder = 'vuplus/%s' % BOX_NAME
    elif os.path.isfile('proc/stb/info/boxtype'):
        BOX_NAME = open('/proc/stb/info/boxtype').read().strip()
    elif os.path.isfile('proc/stb/info/model') and not os.path.isfile("/proc/stb/info/mid"):
        BOX_NAME = open('/proc/stb/info/model').read().strip()
    return BOX_NAME

#zwraca strukture folderu zip - vuplus/vumodel


def getImageFolder():
    if os.path.isfile('/proc/stb/info/vumodel'):
        BOX_NAME = getBoxModelVU()
        ImageFolder = 'vuplus/' + BOX_NAME
    return ImageFolder

#zwraca nazwe kernela z /lib/modules


def getKernelVersion():
    try:
        return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
    except:
        return _('unknown')

# czysci pamiec


def runCMDS(cmdsList):
    clearMemory()
    if isinstance(cmdsList, (list, tuple)):
        myCMD = '\n'.join(cmdsList)# + '\n'
    ret = os.system(myCMD)
    return rett


def getImageDistroN():
    image = 'Internal storage'

    if fileExists('/.multinfo') and fileExists('%sImageBoot/.imagedistro' % getNeoLocation()):
                    with open('%sImageBoot/.imagedistro' % getNeoLocation(), 'r') as f:
                        image = f.readline().strip()
                        f.close()

    elif not fileExists('/.multinfo') and fileExists('/etc/vtiversion.info'):
                    f = open("/etc/vtiversion.info", 'r')
                    imagever = f.readline().strip().replace("Release ", " ")
                    f.close()
                    image = imagever

    elif not fileExists('/.multinfo') and fileExists('/etc/bhversion'):
                    f = open("/etc/bhversion", 'r')
                    imagever = f.readline().strip()
                    f.close()
                    image = imagever

#    elif not fileExists('/.multinfo') and fileExists('/etc/vtiversion.info'):
#                    image = 'VTI Team Image '

    elif fileExists('/.multinfo') and fileExists('/etc/bhversion'):
                    image = 'Flash ' + ' ' + getBoxHostName()

    elif fileExists('/.multinfo') and fileExists('/etc/vtiversion.info'):
                    image = 'Flash ' + ' ' + getBoxHostName()

    elif fileExists('/usr/lib/enigma2/python/boxbranding.so') and not fileExists('/.multinfo'):
                    from boxbranding import getImageDistro
                    image = getImageDistro()

    elif fileExists('/media/InternalFlash/etc/issue.net') and fileExists('/.multinfo') and not fileExists('%sImageBoot/.imagedistro' % getNeoLocation()):
                    obraz = open('/media/InternalFlash/etc/issue.net', 'r').readlines()
                    imagetype = obraz[0][:-3]
                    image = imagetype

    elif fileExists('/etc/issue.net') and not fileExists('/.multinfo'):
                    obraz = open('/etc/issue.net', 'r').readlines()
                    imagetype = obraz[0][:-3]
                    image = imagetype

    else:
                    image = 'Inernal Flash ' + ' ' + getBoxHostName()

    return image


def getKernelVersionString():
    try:
        result = popen('uname -r', 'r').read().strip('\n').split('-')
        kernel_version = result[0]
        return kernel_version
    except:
        pass

    return 'unknown'


def getKernelImageVersion():
    try:
        from glob import glob
        lines = open(glob('/var/lib/opkg/info/kernel-*.control')[0], 'r').readlines()
        kernelimage = lines[1][:-1]
    except:
        kernelimage = getKernelVersionString

    return kernelimage


def getTypBoxa():
    if not fileExists('/etc/typboxa'):
        os.system('touch /etc/typboxa')
        f2 = open('/etc/hostname', 'r')
        mypath2 = f2.readline().strip()
        f2.close()
        if mypath2 == 'vuuno':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Uno ')
            out.close()
        elif mypath2 == 'vuultimo':
            out = open('/etc/typboxa', 'w')
            out.write('Vu+Ultimo ')
            out.close()
        elif mypath2 == 'vuduo':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Duo ')
            out.close()
        elif mypath2 == 'vuduo2':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Duo2 ')
            out.close()
        elif mypath2 == 'vusolo':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Solo ')
            out.close()
        elif mypath2 == 'vusolo2':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Solo2 ')
            out.close()
        elif mypath2 == 'vusolose':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Solo-SE ')
            out.close()
        elif mypath2 == 'vuvzero':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Zero ')
            out.close()
        elif mypath2 == 'vuuno4k':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Uno4k ')
            out.close()
        elif mypath2 == 'vuultimo4k':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Ultimo4k ')
            out.close()
        elif mypath2 == 'vusolo4k':
            out = open('/etc/typboxa ', 'w')
            out.write('Vu+Solo4k ')
            out.close()
        elif mypath2 == 'mbmini':
            out = open('/etc/typboxa', 'w')
            out.write('Miraclebox-Mini ')
            out.close()
        elif mypath2 == 'mutant51':
            out = open('/etc/typboxa', 'w')
            out.write('Mutant 51 ')
            out.close()
        elif mypath2 == 'sf4008':
            out = open('/etc/typboxa', 'w')
            out.write('Ocatgon sf4008 ')
            out.close()
        elif mypath2 == 'ax51':
            out = open('/etc/typboxa', 'w')
            out.write('ax51 ')
            out.close()

    try:
        lines = open('/etc/typboxa', 'r').readlines()
        typboxa = lines[0][:-1]
    except:
        typboxa = 'not detected'

    return typboxa


def getImageVersionString():
    try:
        if os.path.isfile('/var/lib/opkg/status'):
            st = os.stat('/var/lib/opkg/status')
        else:
            st = os.stat('/usr/lib/ipkg/status')
        tm = time.localtime(st.st_mtime)
        if tm.tm_year >= 2015:
            return time.strftime('%Y-%m-%d %H:%M:%S', tm)
    except:
        pass

    return _('unavailable')


def getModelString():
    try:
        file = open('/proc/stb/info/boxtype', 'r')
        model = file.readline().strip()
        file.close()
        return model
    except IOError:
        return 'unknown'


def getChipSetString():
    try:
        f = open('/proc/stb/info/chipset', 'r')
        chipset = f.read()
        f.close()
        return str(chipset.lower().replace('\n', '').replace('bcm', ''))
    except IOError:
        return 'unavailable'


def getCPUString():
    try:
        file = open('/proc/cpuinfo', 'r')
        lines = file.readlines()
        for x in lines:
            splitted = x.split(': ')
            if len(splitted) > 1:
                splitted[1] = splitted[1].replace('\n', '')
                if splitted[0].startswith('system type'):
                    system = splitted[1].split(' ')[0]
                elif splitted[0].startswith('Processor'):
                    system = splitted[1].split(' ')[0]

        file.close()
        return system
    except IOError:
        return 'unavailable'


def getCpuCoresString():
    try:
        file = open('/proc/cpuinfo', 'r')
        lines = file.readlines()
        for x in lines:
            splitted = x.split(': ')
            if len(splitted) > 1:
                splitted[1] = splitted[1].replace('\n', '')
                if splitted[0].startswith('processor'):
                    if int(splitted[1]) > 0:
                        cores = 2
                    else:
                        cores = 1

        file.close()
        return cores
    except IOError:
        return 'unavailable'


def getEnigmaVersionString():
    import enigma
    enigma_version = enigma.getEnigmaVersionString()
    if '-(no branch)' in enigma_version:
        enigma_version = enigma_version[:-12]
    return enigma_version


def getKernelVersionString():
    try:
        f = open('/proc/version', 'r')
        kernelversion = f.read().split(' ', 4)[2].split('-', 2)[0]
        f.close()
        return kernelversion
    except:
        return _('unknown')


def getHardwareTypeString():
    try:
        if os.path.isfile('/proc/stb/info/boxtype'):
            return open('/proc/stb/info/boxtype').read().strip().upper() + ' (' + open('/proc/stb/info/board_revision').read().strip() + '-' + open('/proc/stb/info/version').read().strip() + ')'
        if os.path.isfile('/proc/stb/info/vumodel'):
            return 'VU+' + open('/proc/stb/info/vumodel').read().strip().upper() + '(' + open('/proc/stb/info/version').read().strip().upper() + ')'
        if os.path.isfile('/proc/stb/info/model'):
            return open('/proc/stb/info/model').read().strip().upper()
    except:
        pass

    return _('unavailable')


def getImageTypeString():
    try:
        return open('/etc/issue').readlines()[-2].capitalize().strip()[:-6]
    except:
        pass

    return _('undefined')


def getMachineBuild():
    try:
        return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
    except:
        return 'unknown'


def getVuBoxModel():
    if fileExists('/proc/stb/info/vumodel'):
        try:
            l = open('/proc/stb/info/vumodel')
            model = l.read()
            l.close()
            BOX_NAME = str(model.lower().strip())
            l.close()
            BOX_MODEL = 'vuplus'
        except:
            BOX_MODEL = 'not detected'

    return BOX_MODEL


def getBoxModelVU():
    try:
        if os.path.isfile('/proc/stb/info/vumodel'):
            return open('/proc/stb/info/vumodel').read().strip().upper()
    except:
        pass

    return _('unavailable')


def getMachineProcModel():
    if os.path.isfile('/proc/stb/info/vumodel'):
        BOX_NAME = getBoxModelVU()
        BOX_MODEL = getVuBoxModel()
        if BOX_MODEL == 'vuplus':
            if BOX_NAME == 'duo':
                GETMACHINEPROCMODEL = 'bcm7335'
            elif BOX_NAME == 'solo':
                GETMACHINEPROCMODEL = 'bcm7325'
            elif BOX_NAME == 'solo2':
                GETMACHINEPROCMODEL = 'bcm7346'
            elif BOX_NAME == 'solose':
                GETMACHINEPROCMODEL = 'bcm7241'
            elif BOX_NAME == 'ultimo' or BOX_NAME == 'uno':
                GETMACHINEPROCMODEL = 'bcm7413'
            elif BOX_NAME == 'zero':
                GETMACHINEPROCMODEL = 'bcm7362'
            elif BOX_NAME == 'duo2':
                GETMACHINEPROCMODEL = 'bcm7425'
            elif BOX_NAME == 'ultimo4k':
                GETMACHINEPROCMODEL = 'bcm7444S'
            elif BOX_NAME == 'uno4k':
                GETMACHINEPROCMODEL = 'bcm7252S'
            elif BOX_NAME == 'solo4k':
                GETMACHINEPROCMODEL = 'bcm7376'
            elif BOX_NAME == 'zero4K':
                GETMACHINEPROCMODEL = 'bcm72604'
            elif BOX_NAME == 'uno4kse':
                GETMACHINEPROCMODEL = ''
            procmodel = getMachineProcModel()
    return procmodel


def getMountPointAll():
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


def getMountPointNeo():
            os.system('' + LinkNeoBoot + '/files/mountpoint.sh')
            os.system('echo ' + getLocationMultiboot() + ' > ' + LinkNeoBoot + '/bin/install; chmod 0755 ' + LinkNeoBoot + '/bin/install')
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
            os.system('chmod 755 ' + LinkNeoBoot + '/files/neo.sh')


def getMountPointNeo2():
        #---------------------------------------------
        os.system('touch ' + LinkNeoBoot + '/files/mountpoint.sh; echo "#!/bin/sh"  > ' + LinkNeoBoot + '/files/mountpoint.sh; chmod 0755 ' + LinkNeoBoot + '/files/mountpoint.sh')
        if getNeoMount() == 'hdd_install_/dev/sda1':
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda1 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount() == 'hdd_install_/dev/sdb1':
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sdb1 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount() == 'hdd_install_/dev/sda2':
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda2 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount() == 'hdd_install_/dev/sdb2':
                    os.system('echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda2 /media/hdd"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        #---------------------------------------------
        if getNeoMount2() == 'usb_install_/dev/sdb1':
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdb1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount2() == 'usb_install_/dev/sda1':
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sda1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount2() == 'usb_install_/dev/sdb2':
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdb2 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount2() == 'usb_install_/dev/sdc1':
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdc1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount2() == 'usb_install_/dev/sdd1':
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdd1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount2() == 'usb_install_/dev/sde1':
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sde1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount2() == 'usb_install_/dev/sdf1':
                    os.system('echo "umount -l /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdf1 /media/usb"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        #---------------------------------------------
        elif getNeoMount3() == 'cf_install_/dev/sda1':
                    os.system('echo "umount -l /media/cf\nmkdir -p /media/cf\n/bin/mount /dev/sda1 /media/cf"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount3() == 'cf_install_/dev/sdb1':
                    os.system('echo "umount -l /media/cf\nmkdir -p /media/cf\n/bin/mount /dev/sdb1 /media/cf"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        #---------------------------------------------
        elif getNeoMount4() == 'card_install_/dev/sda1':
                    os.system('echo "umount -l /media/card\nmkdir -p /media/card\n/bin/mount /dev/sda1 /media/card"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount4() == 'card_install_/dev/sdb1':
                    os.system('echo "umount -l /media/card\nmkdir -p /media/card\n/bin/mount /dev/sdb1 /media/card"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        #---------------------------------------------
        elif getNeoMount5() == 'mmc_install_/dev/sda1':
                    os.system('echo "umount -l /media/mmc\nmkdir -p /media/mmc\n/bin/mount /dev/sda1 /media/mmc"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        elif getNeoMount5() == 'mmc_install_/dev/sdb1':
                    os.system('echo "umount -l /media/mmc\nmkdir -p /media/mmc\n/bin/mount /dev/sdb1 /media/mmc"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
        os.system('echo "\n\nexit 0"  >> ' + LinkNeoBoot + '/files/mountpoint.sh')
	
def getBoxMacAddres():
    os.system('%s > /tmp/.mymac' % ("ifconfig -a"))
    if fileExists('/etc/.nameneo'):
        os.system('cp -r /etc/.nameneo /tmp/.mymac; sleep 1')        
        with open('/tmp/.mymac', 'r') as f:
            myboxmac = f.read()
            f.close()
        EthernetMac = myboxmac
    elif fileExists('/tmp/.mymac'):
                    f = open("/tmp/.mymac", 'r')
                    myboxmac = f.readline().strip().replace("eth0      Link encap:Ethernet  HWaddr ", "")
                    f.close()
                    EthernetMac = myboxmac                       
                    writefile = open('/tmp/.mymac' , 'w')
                    writefile.write(myboxmac)
                    writefile.close()
    elif not fileExists('/tmp/.mymac'):
            EthernetMac = '12:34:56:78:91:02'
                        
    return EthernetMac    

def getCheckActivateVip():
    supportedvip = ''
    if os.path.exists('/usr/lib/periodon/.activatedmac'):
        with open('/usr/lib/periodon/.activatedmac', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find("%s" % getBoxMacAddres()) != -1:
            supportedvip = '%s' % getBoxMacAddres()
    return supportedvip
    
def getMountDiskSTB():
    neo_disk = ' '
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()   
        if lines.find('/dev/sda1 /media/hdd') != -1:
            os.system('touch /tmp/disk/sda1; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sdb1 /media/hdd') != -1:
            os.system('touch /tmp/disk/sdb1; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sda2 /media/hdd') != -1:
            os.system('touch /tmp/disk/sda2; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sdb2 /media/hdd') != -1:
            os.system('touch /tmp/disk/sdb2; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sdc1 /media/hdd') != -1:
            os.system('touch /tmp/disk/sdc1; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sdd1 /media/hdd') != -1:
            os.system('touch /tmp/disk/sdd1; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sde1 /media/hdd') != -1:
            os.system('touch /tmp/disk/sde1; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sdf1 /media/hdd') != -1:
            os.system('touch /tmp/disk/sdf1; touch /tmp/disk/#---Select_the_disk_HDD:')            
        if lines.find('/dev/sda1 /media/usb') != -1:
            os.system('touch /tmp/disk/sda1; touch /tmp/disk/#---Select_the_disk_USB:')            
        if lines.find('/dev/sdb1 /media/usb') != -1:
            os.system('touch /tmp/disk/sdb1; touch /tmp/disk/#---Select_the_disk_USB:')            
        if lines.find('/dev/sda2 /media/usb') != -1:
            os.system('touch /tmp/disk/sda2; touch /tmp/disk/#---Select_the_disk_USB:')            
        if lines.find('/dev/sdb2 /media/usb') != -1:
            os.system('touch /tmp/disk/sdb2; touch /tmp/disk/#---Select_the_disk_USB:')            
        if lines.find('/dev/sdc1 /media/usb') != -1:
            os.system('touch /tmp/disk/sdc1; touch /tmp/disk/#---Select_the_disk_USB:')            
        if lines.find('/dev/sdd1 /media/usb') != -1:
            os.system('touch /tmp/disk/sdd1; touch /tmp/disk/#---Select_the_disk_USB:')            
        if lines.find('/dev/sde1 /media/usb') != -1:
            os.system('touch /tmp/disk/sde1; touch /tmp/disk/#---Select_the_disk_USB:')            
        if lines.find('/dev/sdf1 /media/usb') != -1:
            os.system('touch /tmp/disk/sdf1; touch /tmp/disk/#---Select_the_disk_USB:')            

    return neo_disk    

def getCheckExtDisk():
    os.system("cat /proc/mounts | egrep -o '.ext.' | sort | uniq > /tmp/.myext")
    if os.path.exists('/tmp/.myext'):
        with open('/tmp/.myext', 'r') as f:
            myboxEXT = f.readline().strip()
            f.close()
    return myboxEXT 
        
def getCheckExt():
    neoExt = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/media/usb vfat') != -1:
            neoExt = 'vfat'
        elif lines.find('/media/hdd vfat') != -1:
            neoExt = 'vfat'
        elif lines.find('/media/hdd ext3') != -1:
            neoExt = 'ext3'
        elif lines.find('/media/hdd ext4') != -1:
            neoExt = 'ext4'
        elif lines.find('/media/usb ext3') != -1:
            neoExt = 'ext3'
        elif lines.find('/media/usb ext4') != -1:
            neoExt = 'ext4'                         
    return neoExt

def getExtCheckHddUsb():
    neoExt = 'UNKNOWN'
    if os.path.exists('/proc/mounts'):
        with open('/proc/mounts', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('/media/hdd ext4') != -1 or lines.find('/media/hdd type ext4') != -1 and os.path.exists('/media/hdd/ImageBoot'):
            neoExt = 'ext4'
        if lines.find('/media/usb ext4') != -1 or lines.find('/media/usb type ext4') != -1 and os.path.exists('/media/usb/ImageBoot'):
            neoExt = 'ext4'                        
    return neoExt

def getNandWrite():
    NandWrite = 'NandWrite'
    if fileExists('/usr/lib/python2.7'):    
        if os.path.exists('/usr/sbin/nandwrite'):
            with open('/usr/sbin/nandwrite', 'r') as f:
                lines = f.read()
                f.close()
            if lines.find('nandwrite') != -1:
                NandWrite = 'nandwrite'
    else:
        NandWrite = 'no_nandwrite'
	
    return NandWrite

def getMyUUID():
    #os.system("tune2fs -l /dev/sd?? | awk '/UUID/ {print $NF}' > /tmp/.myuuid")
    os.system("tune2fs -l %s | awk '/UUID/ {print $NF}' > /tmp/.myuuid" % (getLocationMultiboot()))
    try:
        if os.path.isfile('/tmp/.myuuid'):
            return open('/tmp/.myuuid').read().strip().upper()
    except:
        pass

    return _('unavailable')

def getImageBootNow():
    imagefile = 'UNKNOWN'
    if os.path.exists('/.multinfo'):
        with open('/.multinfo' , 'r') as f:
            imagefile = f.readline().strip()
            f.close()
    return imagefile

def getNeoActivatedtest():
        neoactivated = 'NEOBOOT MULTIBOOT'
        if not fileExists('/.multinfo'):        
            if getCheckActivateVip() != getBoxMacAddres():       
                neoactivated = 'Ethernet MAC not found.'
            elif not fileExists('/usr/lib/periodon/.kodn'):                   
                neoactivated = 'VIP Pin code missing.'
            elif getTestToTest() != UPDATEVERSION :
                neoactivated = _('Update %s is available.') % getTestToTest()
            else:    
                if getCheckActivateVip() == getBoxMacAddres() and fileExists('/usr/lib/periodon/.kodn') and getTestToTest() == UPDATEVERSION :
                    neoactivated = 'NEOBOOT VIP ACTIVATED'                

        return neoactivated

boxbrand = sys.modules[__name__]

#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import struct
import shutil

# ver. gutosie
#--------------------------------------------- 2022 ---------------------------------------------#

def NEOBootMainEx(source, target, CopyFiles, CopyKernel, TvList, LanWlan, Sterowniki, Montowanie, InstallSettings, ZipDelete, RepairFTP, SoftCam, MediaPortal, PiconR, Kodi, BlackHole, Nandsim):
    NEOBootR(source, target, CopyFiles, CopyKernel, TvList, LanWlan, Sterowniki, Montowanie, InstallSettings, ZipDelete, RepairFTP, SoftCam, MediaPortal, PiconR, Kodi, BlackHole, Nandsim)


def LanguageUsed():
    language = ''
    lang = open('/etc/enigma2/settings', 'r')
    usedlang = 'config.osd.language=pl_PL'
    bak = lang.read().find(usedlang)
    if bak != -1:
        language = 'Yes'
    else:
        language = 'No'
    return language


def getBoxHostName():
    if os.path.exists('/etc/hostname'):
        with open('/etc/hostname', 'r') as f:
            myboxname = f.readline().strip()
            f.close()
    return myboxname


def getCPUSoC():
    chipset = 'UNKNOWN'
    if os.path.exists('/proc/stb/info/chipset'):
        with open('/proc/stb/info/chipset', 'r') as f:
            chipset = f.readline().strip()
            f.close()
        if chipset == '7405(with 3D)':
            chipset == '7405'

    return chipset


def getBoxVuModel():
    vumodel = 'UNKNOWN'
    if os.path.exists("/proc/stb/info/vumodel") and not os.path.exists("/proc/stb/info/boxtype"):
        with open('/proc/stb/info/vumodel', 'r') as f:
            vumodel = f.readline().strip()
            f.close()
    return vumodel


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


def getKernelVersion():
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm520') or os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm525') :
            result = popen('uname -r', 'r').read().strip('\n').split('-')
            kernel_version = result[0]
            return kernel_version
    else:                        
        try:
            return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
        except:
            os.system('uname -r > /tmp/.uname_r') 
            return open('/tmp/.uname_r').read().strip().upper()


def getNeoLocation():
    locatino = 'UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'r') as f:
            locatino = f.readline().strip()
            f.close()
    return locatino


media = getNeoLocation()
mediahome = media + '/ImageBoot/'
extensions_path = '/usr/lib/enigma2/python/Plugins/Extensions/'
dev_null = ' > /dev/null 2>&1'
supportedTuners = 'vuplus'


def NEOBootMainEx(source, target, CopyFiles, CopyKernel, TvList, LanWlan, Sterowniki, Montowanie, InstallSettings, ZipDelete, RepairFTP, SoftCam, MediaPortal, PiconR, Kodi, BlackHole, Nandsim):
    media_target = mediahome + target
    list_one = ['rm -r ' + media_target + dev_null, 'mkdir ' + media_target + dev_null, 'chmod -R 0777 ' + media_target]
    for command in list_one:
        os.system(command)

    rc = NEOBootExtract(source, target, ZipDelete, Nandsim)

    os.system('sync; echo 1 > /proc/sys/vm/drop_caches')

    if not os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions' % (media, target)):
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions' % (media, target))

    if os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot' % (media, target)):
        os.system('rm -r %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot' % (media, target))
        
    list_two = ['mkdir -p ' + media_target + '/media' + dev_null,
     'rm ' + media_target + media + dev_null,
     'rmdir ' + media_target + media + dev_null,
     'mkdir -p ' + media_target + media + dev_null,
     #'cp /etc/passwd ' + media_target + '/etc/passwd' + dev_null,
#     'cp ' + extensions_path + 'NeoBoot/bin/hdd' + media_target+'/etc/init.d/hddusb' + dev_null,
     'cp /etc/hostname ' + media_target + '/etc/hostname' + dev_null,
     'cp -a /usr/share/enigma2/rc_models/* ' + media_target + '/usr/share/enigma2/rc_models/' + dev_null,
     'cp -r -p /usr/share/enigma2/rc_models ' + media_target + '/usr/share/enigma2' + dev_null,
     'cp -af ' + extensions_path + 'NeoBoot ' + media_target + extensions_path + 'NeoBoot' + dev_null,
     'mkdir -p ' + media_target + extensions_path + 'NeoReboot' + dev_null,
     'touch ' + media_target + extensions_path + 'NeoReboot/__init__.py' + dev_null,
     'chmod 644 ' + media_target + extensions_path + 'NeoReboot/__init__.py' + dev_null,
     'cp -af ' + extensions_path + 'NeoBoot/files/backflash ' + media_target + extensions_path + 'NeoReboot/backflash.sh' + dev_null,
     'cp -af ' + extensions_path + 'NeoBoot/files/neoreboot ' + media_target + extensions_path + 'NeoReboot/plugin.py' + dev_null]
    for command in list_two:
        os.system(command)

    if CopyFiles == 'False':
        os.system('echo "No copying of files..."')
        os.system('touch  ' + getNeoLocation() + 'ImageBoot/.without_copying; sleep 5')

    if CopyKernel == 'True':
           #mips vuplus
            if getBoxHostName() == 'vuultimo' or getCPUSoC() == '7405' and os.path.exists('%s/ImageBoot/%s/etc/vtiversion.info' % (media, target)):
                if os.path.exists('%s/ImageBoot/%s/lib/modules' % (media, target)):
                    cmd = 'rm -r %s/ImageBoot/%s/lib/modules' % (media, target)
                    rc = os.system(cmd)
                cmd = 'mkdir -p %s/ImageBoot/%s/lib/modules > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /lib/modules  %s/ImageBoot/%s/lib  > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                if os.path.exists('%s/ImageBoot/%s/lib/firmware' % (media, target)):
                    cmd = 'rm -r %s/ImageBoot/%s/lib/firmware' % (media, target)
                    rc = os.system(cmd)
                cmd = 'mkdir -p %s/ImageBoot/%s/lib/firmware > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /lib/firmware %s/ImageBoot/%s/lib > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                os.system('echo "Copied system drivers. Not recommended copied kernel.bin for Ultimo HD."')
            elif getCPUtype() == "MIPS" and getBoxHostName() == 'vuultimo' or getBoxHostName() == 'bm750' or getBoxHostName() == 'vuduo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuduo' or getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vusolose' or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vuzero' or getBoxHostName() == 'mbultra':
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/vuplus/' + getBoxVuModel() + '/kernel_cfe_auto.bin ' + media_target + '/boot/' + getBoxHostName() + '.vmlinux.gz' + dev_null)
                os.system('echo "Copied kernel.bin STB-MIPS"')
            elif getCPUtype() == "MIPS" and getBoxHostName() == 'et5x00' :
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/' + getBoxHostName() + '/kernel.bin ' + media_target + '/boot/' + getBoxHostName() + '.vmlinux.gz' + dev_null)
                os.system('echo "Copied kernel.bin STB-MIPS Clarke-Tech & Xtrend"')
            #arm vuplus arms
            elif getCPUtype() == "ARMv7" and getBoxHostName() == "vuultimo4k" or getBoxHostName() == "vusolo4k" or getBoxHostName() == "vuuno4k" or getBoxHostName() == "vuuno4kse" or getBoxHostName() == "vuduo4k" or getBoxHostName() == "vuduo4kse" or getBoxHostName() == "vuzero4k":
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/vuplus/' + getBoxVuModel() + '/kernel_auto.bin ' + media_target + '/boot/zImage.' + getBoxHostName() + '' + dev_null)
                os.system('echo "Copied kernel.bin STB-ARM"')

    if not os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying'):
        if os.path.exists('/usr/sbin/nandwrite'):
            cmd = 'cp -af /usr/sbin/nandwrite %s/ImageBoot/%s/usr/sbin/nandwrite > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/bin/fullwget'):
            cmd = 'cp -af /usr/bin/fullwget %s/ImageBoot/%s/usr/bin/fullwget > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/etc/init.d/inadyn-mt'):
            cmd = 'cp -af /etc/init.d/inadyn-mt %s/ImageBoot/%s/etc/init.d/inadyn-mt > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/bin/inadyn-mt'):
            cmd = 'cp -af /usr/bin/inadyn-mt %s/ImageBoot/%s/usr/bin/inadyn-mt > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/etc/inadyn.conf'):
            cmd = 'cp -af /etc/inadyn.conf %s/ImageBoot/%s/etc/inadyn.conf > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/FanControl'):
            cmd = 'cp -af /usr/lib/enigma2/python/Plugins/SystemPlugins/FanControl %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/SystemPlugins > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('' + extensions_path + 'EmuManager'):
            cmd = 'cp -af ' + extensions_path + 'EmuManager %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('' + extensions_path + 'CamdMenager'):
            cmd = 'cp -af ' + extensions_path + 'CamdMenager %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('' + extensions_path + 'IPTVPlayer'):
            cmd = 'cp -af ' + extensions_path + 'IPTVPlayer %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /usr/lib/python*.*/htmlentitydefs.pyo %s/ImageBoot/%s/usr/lib/python*.* > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('' + extensions_path + 'FeedExtra'):
            cmd = 'cp -af ' + extensions_path + 'FeedExtra %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('' + extensions_path + 'MyUpdater'):
            cmd = 'cp -af ' + extensions_path + 'MyUpdater %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('' + extensions_path + 'AlternativeSoftCamManager'):
            cmd = 'cp -af ' + extensions_path + 'AlternativeSoftCamManager %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('' + extensions_path + 'TempFanControl'):
            cmd = 'cp -af ' + extensions_path + 'TempFanControl %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/TempFanControl > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)            
        if not os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so' % (media, target)):
            cmd = 'cp -af /usr/lib/enigma2/python/boxbranding.so %s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions/HbbTV' % (media, target)):
            os.system('rm -rf %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions/HbbTV' % (media, target))

        if TvList == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.radio %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/lamedb %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Copied TV list..."')

        if LanWlan == 'True':
            if os.path.exists('%s/ImageBoot/%s/etc/vtiversion.info' % (media, target)):
                os.system('echo "Not copied LAN-WLAN, not recommended for this image."')
            elif os.path.exists('/etc/vtiversion.info') and os.path.exists('%s/usr/lib/enigma2/python/Plugins/PLi' % (media, target)):
                os.system('echo "Not copied LAN-WLAN, not recommended for this image."')
            elif os.path.exists('/etc/bhversion') and os.path.exists('%s/usr/lib/enigma2/python/Plugins/PLi' % (media, target)):
                os.system('echo "Not copied LAN-WLAN, not recommended for this image."')
            else:
                if os.path.exists('/etc/wpa_supplicant.wlan0.conf'):
                    cmd = 'cp -af /etc/wpa_supplicant.wlan0.conf %s/ImageBoot/%s/etc/wpa_supplicant.wlan0.conf > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/network/interfaces'):
                    cmd = 'cp -af /etc/network/interfaces %s/ImageBoot/%s/etc/network/interfaces > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/wpa_supplicant.conf'):
                    cmd = 'cp -af /etc/wpa_supplicant.conf %s/ImageBoot/%s/etc/wpa_supplicant.conf > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/resolv.conf'):
                    cmd = 'cp -af /etc/resolv.conf %s/ImageBoot/%s/etc/resolv.conf > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/wl.conf.wlan3'):
                    cmd = 'cp -af /etc/wl.conf.wlan3 %s/ImageBoot/%s/etc/wl.conf.wlan3 > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
            os.system('echo "Copied LAN-WLAN..."')

        if Sterowniki == 'True':
            if os.path.exists('%s/ImageBoot/%s/lib/modules' % (media, target)):
                cmd = 'rm -r %s/ImageBoot/%s/lib/modules' % (media, target)
                rc = os.system(cmd)
            cmd = 'mkdir -p %s/ImageBoot/%s/lib/modules > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp -af /lib/modules  %s/ImageBoot/%s/lib  > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            if os.path.exists('%s/ImageBoot/%s/lib/firmware' % (media, target)):
                cmd = 'rm -r %s/ImageBoot/%s/lib/firmware' % (media, target)
                rc = os.system(cmd)
            cmd = 'mkdir -p %s/ImageBoot/%s/lib/firmware > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp -af /lib/firmware %s/ImageBoot/%s/lib > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            os.system('echo "System drivers copied..."')
            
        if Montowanie == 'True':
            if getCPUtype() == "MIPS":
                if os.path.exists('%s/ImageBoot/%s/etc/fstab' % (media, target)):
                    cmd = 'mv %s/ImageBoot/%s/etc/fstab %s/ImageBoot/%s/etc/fstab.org' % (media,
                     target,
                     media,
                     target)
                    rc = os.system(cmd)
                if os.path.exists('%s/ImageBoot/%s/etc/init.d/volatile-media.sh' % (media, target)):
                    cmd = 'mv %s/ImageBoot/%s/etc/init.d/volatile-media.sh %s/ImageBoot/%s/etc/init.d/volatile-media.sh.org' % (media,
                     target,
                     media,
                     target)
                    rc = os.system(cmd)
                cmd = 'cp -r /etc/fstab %s/ImageBoot/%s/etc/fstab' % (media, target)
                rc = os.system(cmd)
                os.system('echo "The fstab mount file was copied..."')
            elif getCPUtype() == "ARMv7":
                os.system('echo "No copied mount ARM..."')
                

        if InstallSettings == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/settings %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            if not os.path.exists('%s/ImageBoot/%s/etc/tuxbox/config' % (media, target)):
                cmd = 'mkdir -p /etc/tuxbox/config %s/ImageBoot/%s/etc/tuxbox/config' % (media, target)
                rc = os.system(cmd)
                cmd = 'mkdir -p /etc/tuxbox/scce %s/ImageBoot/%s/etc/tuxbox/scce' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp -af /etc/tuxbox/* %s/ImageBoot/%s/etc/tuxbox' % (media, target)
            rc = os.system(cmd)
            os.system('touch /tmp/settings_copied; echo "System settings copied..."')

        if RepairFTP == 'True':
            if os.path.exists('%s/ImageBoot/%s/etc/vsftpd.conf' % (media, target)):
                filename = media + '/ImageBoot/' + target + '/etc/vsftpd.conf'
                if os.path.exists(filename):
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('listen=NO') != -1:
                            line = 'listen=YES\n'
                        elif line.find('listen_ipv6=YES') != -1:
                            line = 'listen_ipv6=NO\n'
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
            os.system('echo "Repair ftp."')

        if SoftCam == 'True':
            if os.path.exists('/etc/CCcam.cfg'):
                cmd = 'cp -af /etc/CCcam.cfg %s/ImageBoot/%s/etc > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
            if os.path.exists('/etc/tuxbox/config'):
                cmd = 'cp -af /etc/tuxbox/config %s/ImageBoot/%s/etc/tuxbox > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)                
            os.system('echo "Copied softcam files to the installed image..."')

        if MediaPortal == 'True':
            if os.path.exists('' + extensions_path + 'MediaPortal'):
                cmd = 'cp -af ' + extensions_path + 'MediaPortal %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af ' + extensions_path + 'mpgz %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /usr/lib/python2.7/argparse.pyo %s/ImageBoot/%s/usr/lib/python2.7 > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /usr/lib/python2.7/robotparser.pyo %s/ImageBoot/%s/usr/lib/python2.7 > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /usr/lib/python2.7/site-packages/Crypto %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /usr/lib/python2.7/site-packages/mechanize %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /usr/lib/python2.7/site-packages/requests %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -af /usr/lib/python2.7/site-packages/requests-2.11.1-py2.7.egg-info %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)

                if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                    cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/enigma2/mp_2s4p'):
                    cmd = 'cp /etc/enigma2/mp_2s4p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/enigma2/mp_config'):
                    cmd = 'cp /etc/enigma2/mp_config %s/ImageBoot/%s/etc/enigma2' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/enigma2/mp_pluginliste'):
                    cmd = 'cp /etc/enigma2/mp_pluginliste %s/ImageBoot/%s/etc/enigma2' % (media, target)
                    rc = os.system(cmd)
                os.system('echo "Copied MediaPortal..."')
            elif not os.path.exists('' + extensions_path + 'MediaPortal'):
                os.system('echo "MediaPortal not found."')

        if PiconR == 'True':
            if os.path.exists('/usr/share/enigma2/picon'):
                cmd = 'cp -af /usr/share/enigma2/picon %s/ImageBoot/%s/usr/share/enigma2' % (media, target)
                rc = os.system(cmd)
                os.system('echo "Copied picon..."')
            elif not os.path.exists('/usr/share/enigma2/picon'):
                os.system('echo "Picon flash not found."')

        if Kodi == 'True':
            cmd = 'mkdir -p %s/ImageBoot/%s/home/root/.kodi > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            if os.path.exists('/home/root/.kodi'):
                os.system('echo "Kodi set ok."')
            else:
                if not os.path.exists('/home/root/.kodi'):
                    if not os.path.exists('/.multinfo'):
                        if os.path.exists('/media/hdd/.kodi'):
                            cmd = 'mv /media/hdd/.kodi /media/hdd/.kodi_flash; ln -sf "/media/hdd/.kodi_flash" "/home/root/.kodi"; ln -sf "/home/root/.kodi" "/media/hdd/.kodi" '
                            rc = os.system(cmd)
                            os.system('echo "Kodi fix ok."')
                        else:
                            os.system('echo "Kodi not found.."')
                    else:
                        os.system('echo "Kodi path possible only from flash."')
                else:
                    os.system('echo "Kodi not found."')

        if BlackHole == 'True':
            if 'BlackHole' in source or os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Blackhole' % (media, target)):
                cmd = 'mkdir -p ' + getNeoLocation() + 'ImageBoot/%s/boot/blackhole' % target
                rc = os.system(cmd)
                cmd = 'mv ' + getNeoLocation() + 'ImageBoot/' + target + '/usr/lib/enigma2/python/Blackhole/BhUtils.pyo ' + getNeoLocation() + 'ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo.org' % target
                rc = os.system(cmd)
                cmd = 'cp -af ' + extensions_path + 'NeoBoot/bin/utilsbh ' + getNeoLocation() + 'ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.py' % target
                rc = os.system(cmd)
                ver = source.replace('BlackHole-', '')
                try:
                    text = ver.split('-')[0]
                except:
                    text = ''
                localfile = '' + getNeoLocation() + 'ImageBoot/%s/boot/blackhole/version' % target
                temp_file = open(localfile, 'w')
                temp_file.write(text)
                temp_file.close()
                cmd = 'mv ' + getNeoLocation() + 'ImageBoot/' + target + '/usr/bin/enigma2 ' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2-or' % target
                rc = os.system(cmd)
                fail = '' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2-or' % target
                f = open(fail, 'r')
                content = f.read()
                f.close()
                localfile2 = '' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2' % target
                temp_file2 = open(localfile2, 'w')
                temp_file2.write(content.replace('/proc/blackhole/version', '/boot/blackhole/version'))
                temp_file2.close()
                cmd = 'chmod -R 0755 %s' % localfile2
                rc = os.system(cmd)
                cmd = 'rm -r ' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2-or' % target
                rc = os.system(cmd) 
                #cmd = 'cp -af' + getNeoLocation() + 'ImageBoot/' + target + '/etc/bhversion ' + getNeoLocation() + 'ImageBoot/%s/boot/blackhole/version' % target
                #rc = os.system(cmd)
                #cmd = 'cp -f ' + extensions_path + 'NeoBoot/bin/version ' + getNeoLocation() + 'ImageBoot/%s/boot/blackhole/version' % target
                #rc = os.system(cmd)

# for all image:
        if os.path.exists('%s/ImageBoot/%s/etc/rc.local' % (media, target)):
                filename = '%s/ImageBoot/%s/etc/rc.local' % (media, target)
                if os.path.exists(filename):
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('exit 0') != -1:
                            line = '\n'
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                cmd = 'echo -n "\n\n/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/userscript.sh \n\nexit 0" >> %s/ImageBoot/%s/etc/rc.local' % (media, target)
                rc = os.system(cmd)
                cmd = 'chmod 0755 %s/ImageBoot/%s/etc/rc.local' % (media, target)
                rc = os.system(cmd)

        if os.path.exists('%s/ImageBoot/%s/etc/init.d/rc.local' % (media, target)):
                filename = '%s/ImageBoot/%s/etc/init.d/rc.local' % (media, target)
                if os.path.exists(filename):
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('exit 0') != -1:
                            line = '\n'
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)

                cmd = 'echo -n "\n\n/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/userscript.sh \n\nexit 0" >> %s/ImageBoot/%s/etc/init.d/rc.local' % (media, target)
                rc = os.system(cmd)
                cmd = 'chmod 0755 %s/ImageBoot/%s/etc/init.d/rc.local' % (media, target)
                rc = os.system(cmd)

        if not os.path.exists('%s/ImageBoot/%s/etc/init.d/rc.local' % (media, target)) and not os.path.exists('%s/ImageBoot/%s/etc/rc.local' % (media, target)):
            if os.path.exists('%s/ImageBoot/%s/etc/init.d' % (media, target)):
#                cmd = 'ln -s %sImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/userscript.sh %sImageBoot/%s/etc/rcS.d/S99neo.local' % (media,
#                 target,
#                 media,
#                 target)
                cmd = 'cp -af /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/userscript.sh %sImageBoot/%s/etc/rcS.d/S99neo.local' % (media, target)
                rc = os.system(cmd)
                cmd1 = 'chmod 0755 %s/ImageBoot/%s/etc/rcS.d/S99neo.local' % (media, target)
                rc = os.system(cmd1)
            elif not os.path.exists('%s/ImageBoot/%s/etc/init.d' % (media, target)):
                os.system('echo "/etc/init.d not found."')
            os.system('echo "Copied file neo_userscript.sh"')
            
    if not os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying') and not os.path.exists(' /tmp/settings_copied'):        
        for line in open("/etc/hostname"):                                
            if getCPUtype() == 'MIPS' and "dm500hd" in line or "dm800se" in line or "dm800" in line or "dm800se" in line or "dm8000" in line:
                if os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                    cmd = 'rm -r %s/ImageBoot/%s/etc/enigma2' % (media, target)
                    rc = os.system(cmd)
            else:                
                if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                    cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                    rc = os.system(cmd)
                    cmd = 'touch %s/ImageBoot/%s/etc/enigma2/settings' % (media, target)
                    rc = os.system(cmd)
                cmd = 'grep "config.Nims" /etc/enigma2/settings >> %s/ImageBoot/%s/etc/enigma2/settings' % (media, target)
                rc = os.system(cmd)
                cmd1 = 'grep "av.videomode.DVI" /etc/enigma2/settings >> %s/ImageBoot/%s/etc/enigma2/settings' % (media, target)
                rc = os.system(cmd1)
                cmd2 = 'grep "config.OpenWebif" /etc/enigma2/settings >> %s/ImageBoot/%s/etc/enigma2/settings' % (media, target)
                rc = os.system(cmd2)
                cmd3 = 'grep "config.osd" /etc/enigma2/settings >> %s/ImageBoot/%s/etc/enigma2/settings' % (media, target)
                rc = os.system(cmd3)
                cmd4 = 'grep "config.timezone.val" /etc/enigma2/settings >> %s/ImageBoot/%s/etc/enigma2/settings' % (media, target)
                rc = os.system(cmd4)
                cmd5 = 'grep "config.servicelist.startuproot" /etc/enigma2/settings >> %s/ImageBoot/%s/etc/enigma2/settings' % (media, target)
                rc = os.system(cmd5)
                cmd6 = 'grep "UUID=" /etc/fstab >> %s/ImageBoot/%s/etc/fstab' % (media, target)
                rc = os.system(cmd6)

#####################################
        if not os.path.exists('' + media_target + '/boot/zImage.' + getBoxHostName() + '') and getCPUtype() == 'MIPS':
            namefile = media + '/ImageBoot/' + target + '/etc/fstab'
            namefile2 = namefile + '.tmp'
            if os.path.exists(namefile2):
                out = open(namefile2, 'w')
                f = open(namefile, 'r')
                for line in f.readlines():
                    if line.find('/dev/mmcblk0p2') != -1:
                        line = '#' + line
                    elif line.find('/dev/root') != -1:
                        line = '#' + line
                    out.write(line)

                f.close()
                out.close()
                os.rename(namefile2, namefile)

            tpmd = media + '/ImageBoot/' + target + '/etc/init.d/tpmd'
            if os.path.exists(tpmd):
                os.system('rm ' + tpmd)

            fname = media + '/ImageBoot/' + target + '/usr/lib/enigma2/python/Components/config.py'
            if os.path.exists(fname):
                fname2 = fname + '.tmp'
                out = open(fname2, 'w')
                f = open(fname, 'r')
                for line in f.readlines():
                    if line.find('if file(""/proc/stb/info/vumodel")') != -1:
                        line = '#' + line
                    out.write(line)

                f.close()
                out.close()
                os.rename(fname2, fname)

            targetfile = media + '/ImageBoot/' + target + '/etc/vsftpd.conf'
            if os.path.exists(targetfile):
                targetfile2 = targetfile + '.tmp'
                out = open(targetfile2, 'w')
                f = open(targetfile, 'r')
                for line in f.readlines():
                    if not line.startswith('nopriv_user'):
                        out.write(line)

                f.close()
                out.close()
                os.rename(targetfile2, targetfile)

            mypath = media + '/ImageBoot/' + target + '/usr/lib/opkg/info/'
            cmd = 'mkdir -p %s/ImageBoot/%s/var/lib/opkg/info > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            if not os.path.exists(mypath):
                mypath = media + '/ImageBoot/' + target + '/var/lib/opkg/info/'
            for fn in os.listdir(mypath):
                if fn.find('kernel-image') != -1 and fn.find('postinst') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    if f.close():
                        out.close()
                        os.rename(filename2, filename)
                        cmd = 'chmod -R 0755 %s' % filename
                        rc = os.system(cmd)
                if fn.find('-bootlogo.postinst') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
                if fn.find('-bootlogo.postrm') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
                if fn.find('-bootlogo.preinst') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
                if fn.find('-bootlogo.prerm') != -1:
                    filename = mypath + fn
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('/boot') != -1:
                            line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
                    
            #_______________________________________________status1 zmienione        
            if os.path.exists('%s/ImageBoot/%s/var/lib/opkg/status1' % (media, target)):                
                cmd = 'mv ' + getNeoLocation() + 'ImageBoot/' + target + '/var/lib/opkg/status ' + getNeoLocation() + 'ImageBoot/%s/var/lib/opkg/status-or' % target
                rc = os.system(cmd)
                fail = '' + getNeoLocation() + 'ImageBoot/%s/var/lib/opkg/status-or' % target
                f = open(fail, 'r')
                content = f.read()
                f.close()
                localfile2 = '' + getNeoLocation() + 'ImageBoot/%s/var/lib/opkg/status' % target
                temp_file2 = open(localfile2, 'w')
                temp_file2.write(content.replace('kernel-image', '#kernel-image'))
                temp_file2.close()
                
                cmd = 'chmod -R 0755 %s' % localfile2
                rc = os.system(cmd)
                cmd = 'rm -r ' + getNeoLocation() + 'ImageBoot/%s/var/lib/opkg/status-or' % target
                rc = os.system(cmd)                    

#    cmd = 'cp -f ' + extensions_path + 'NeoBoot/bin/hdd ' + getNeoLocation() + 'ImageBoot/%s/etc/init.d/hddusb' % target
#    rc = os.system(cmd)
    if os.path.exists('%s/ImageBoot/%s/usr/lib' % (media, target)):
        cmd = 'cp -af /usr/lib/periodon ' + getNeoLocation() + 'ImageBoot/%s/usr/lib/' % target
        rc = os.system(cmd)
        cmd = 'cp -af /usr/lib/enigma2/python/Tools/Testinout.py ' + getNeoLocation() + 'ImageBoot/%s/usr/lib/enigma2/python/Tools/' % target
        rc = os.system(cmd)
    os.system('mkdir -p ' + media_target + '/media/hdd' + dev_null)
    os.system('mkdir -p ' + media_target + '/media/usb' + dev_null)
    os.system('mkdir -p ' + media_target + '/var/lib/opkg/info/' + dev_null)
    os.system('touch ' + getNeoLocation() + 'ImageBoot/.data; echo "Data instalacji image" > ' + getNeoLocation() + 'ImageBoot/.data; echo " "; date  > ' + getNeoLocation() + 'ImageBoot/.data')
    os.system('mv -f ' + getNeoLocation() + 'ImageBoot/.data ' + getNeoLocation() + 'ImageBoot/%s/.data' % target)
    cmd = 'touch /tmp/.init_reboot'
    rc = os.system(cmd)
    out = open(mediahome + '.neonextboot', 'w')
    out.write(target)
    out.close()
    os.system('cp ' + getNeoLocation() + 'ImageBoot/.neonextboot ' + getNeoLocation() + 'ImageBoot/%s/.multinfo' % target)
    out = open(mediahome + '.neonextboot', 'w')
    out.write('Flash')
    out.close()
    if '.tar.xz' not in source and not os.path.exists('' + getNeoLocation() + '/ImageBoot/%s/etc/issue' % target):
            os.system('echo ""; echo "No system installed! The reason for the installation error may be badly packed image files or it is not a system for your model."')
            os.system('echo "The installed system may not start. Check the correctness of the installed image directory!!!"')
            os.system('rm -r ' + getNeoLocation() + '/ImageBoot/%s' % target)

    if os.path.exists('' + getNeoLocation() + 'ubi'):
        os.system('rm -r ' + getNeoLocation() + 'ubi')
    if os.path.exists('' + getNeoLocation() + 'image_cache/'):
        os.system('rm -r ' + getNeoLocation() + 'image_cache')
    if os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying'):
        os.system('rm -f ' + getNeoLocation() + 'ImageBoot/.without_copying')

    rc = RemoveUnpackDirs()

    os.system('echo "End of installation:"; date +%T')
    os.system('echo "If you want to save the installation process from the console press green."')


def RemoveUnpackDirs():
    os.chdir(media + '/ImagesUpload')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/unpackedzip'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/unpackedzip')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/*.bin'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/*.bin')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/*.txt'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/*.txt')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/vuplus')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf4008'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/sf4008')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmio4k'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osmio4k')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmio4kplus'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osmio4kplus')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm900'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/dm900')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd60'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/hd60')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd61'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/hd61')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd51'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/hd51')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/bre2ze4k'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/bre2ze4k')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/multibox'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/multibox')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/multiboxse'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/multiboxse')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/unforce_multibox.txt'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/unforce_multibox.txt')       
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/axas'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/axas')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/miraclebox')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e4hd'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/e4hd')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/update')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/*.nfi'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/*.nfi')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/zgemma')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler1'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/formuler1')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler3'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/formuler3')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler4turbo'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/formuler4turbo')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et*'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/et*')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedl*'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/xpeedl*')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osmini')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osminiplus'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osminiplus')        
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osnino'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osnino')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osninoplus'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osninoplus')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osninopro'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osninopro')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini4k'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osmini4k')        
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/xp1000 '):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/xp1000 ')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et5x00'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/et5x00 ')        
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dinobot '):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/dinobot ')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e2/update'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/e2')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et1x000'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/et1x000')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/protek4k'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/protek4k')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm920 '):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/dm920 ')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dreamtwo '):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/dreamtwo ')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/multibox') or os.path.exists('' + getNeoLocation() + 'ImagesUpload/multiboxse'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/multibox ' + getNeoLocation() + 'ImagesUpload/multibox; rm -r ' + getNeoLocation() + 'ImagesUpload/multibox')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/usb_update.bin ' + getNeoLocation() + 'ImagesUpload/octagon; rm -r ' + getNeoLocation() + 'ImagesUpload/octagon')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008m'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/octagon')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h7'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/h7; mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/h7')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h7')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/h9; mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/h9')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h9')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9se'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/h9se; mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/h9se')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h9se')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/i55plus'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/i55plus; mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/i55plus')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/i55plus')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9combo'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/force_h9combo_READ.ME ' + getNeoLocation() + 'ImagesUpload/h9combo; mv ' + getNeoLocation() + 'ImagesUpload/unforce_h9combo.txt ' + getNeoLocation() + 'ImagesUpload/h9combo')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h9combo')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9combose'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/force_h9combose_READ.ME ' + getNeoLocation() + 'ImagesUpload/h9combo; mv ' + getNeoLocation() + 'ImagesUpload/unforce_h9combose.txt ' + getNeoLocation() + 'ImagesUpload/h9combose')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h9combose')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h10'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/force_h10_READ.ME ' + getNeoLocation() + 'ImagesUpload/h10; mv ' + getNeoLocation() + 'ImagesUpload/unforce_h10.txt ' + getNeoLocation() + 'ImagesUpload/h10')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h10')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/uclan'):
        if os.path.exists('' + getNeoLocation() + 'ImagesUpload/usb_update.bin'):
            rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/usb_update.bin ' + getNeoLocation() + 'ImagesUpload/uclan')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/uclan')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/ustym4kpro'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/ustym4kpro')        
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/apploader.bin ' + getNeoLocation() + 'ImagesUpload/beyonwiz')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/beyonwiz')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/beyonwiz')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/beyonwiz')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/amiko'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/usb_update.bin ' + getNeoLocation() + 'ImagesUpload/amiko')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/apploader.bin ' + getNeoLocation() + 'ImagesUpload/amiko')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/amiko')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/amiko')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/amiko')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/x1') or os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/x34k'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/gigablue')   
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue') and os.path.exists('' + getNeoLocation() + 'ImagesUpload/usb_update.bin'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/usb_update.bin ' + getNeoLocation() + 'ImagesUpload/gigablue')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/apploader.bin ' + getNeoLocation() + 'ImagesUpload/gigablue')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/gigablue')
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/gigablue')
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/gigablue')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.tar.bz2'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.bz2')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et10000'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/et10000')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vs1000'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/vs1000')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vs1500'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/vs1500')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/pulse4k'):
        if os.path.exists('' + getNeoLocation() + 'ImagesUpload/pulse4k/force_pulse4k_READ.ME'):
            rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/pulse4k/force_pulse4k_READ.ME; rm -r ' + getNeoLocation() + 'ImagesUpload/pulse4k/unforce_pulse4k.txt')    
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/pulse4k')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/pulse4kmin'):
        if os.path.exists('' + getNeoLocation() + 'ImagesUpload/pulse4kmin/force_pulse4kmini_READ.ME'):
            rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/pulse4kmini/force_pulse4kmini_READ.ME; rm -r ' + getNeoLocation() + 'ImagesUpload/pulse4kmini/unforce_pulse4kmini.txt')    
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/pulse4kmin')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/xpeedlx')        
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm520'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/dm520')        
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/unforce_h9combo.txt'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/unforce_h9combo.txt')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/imageversion'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/imageversion')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/kernel.bin'):
        rc = os.system('rm -rf ' + getNeoLocation() + 'ImagesUpload/kernel.bin') 
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/force_multibox_READ.ME'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/force_multibox_READ.ME')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/force'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/force')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.bin'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/rootfs.bin')  
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/splash.bin'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/splash.bin')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/gigablue')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/update_bootargs_h8'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/update_bootargs_h8')        
        
def NEOBootExtract(source, target, ZipDelete, Nandsim):
    RemoveUnpackDirs()
    os.system('echo "Press green to hide Console or red to abort the installation\nInstallation started:"; date +%T;echo "Extracting the installation file..."')

    if os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying'):
        os.system('rm -f ' + getNeoLocation() + 'ImageBoot/.without_copying')
    if os.path.exists('' + getNeoLocation() + 'image_cache'):
        os.system('rm -rf ' + getNeoLocation() + 'image_cache')

    sourcefile = media + '/ImagesUpload/%s.zip' % source
    sourcefile2 = media + '/ImagesUpload/%s.nfi' % source
    sourcefile3 = media + '/ImagesUpload/%s.rar' % source
    sourcefile4 = media + '/ImagesUpload/%s.gz' % source

    #Instalacja *.nfi
    if os.path.exists(sourcefile2) is True:
        if sourcefile2.endswith('.nfi'):
            os.system('echo "Instalacja systemu skapowanego w plik nfi..."')
            to = '' + getNeoLocation() + 'ImageBoot/' + target
            cmd = 'mkdir %s > /dev/null 2<&1' % to
            rc = os.system(cmd)
            to = '' + getNeoLocation() + 'ImageBoot/' + target
            cmd = 'chmod -R 0777 %s' % to
            rc = os.system(cmd)
            cmd = 'touch /tmp/root_jffs2; ' + extensions_path + 'NeoBoot/bin/nfidump ' + sourcefile2 + ' ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            if os.path.exists('%sImageBoot/%s/media/squashfs-images' % (media, target)) and os.path.exists('%s/squashfs-images' % (media)) :
                os.system('cp -af %s/squashfs-images/* "%sImageBoot/%s/media/squashfs-images' % (media, media, target))            
            if ZipDelete == 'True':
                rc = os.system('rm -rf ' + sourcefile2)
            else:
                os.system('echo "NeoBoot keep the file:  %s  for reinstallation."' % sourcefile2)
    #Instalacja *.rar
    if os.path.exists(sourcefile3) is True:
        if sourcefile3.endswith('.rar'):
            os.system('echo "Installing iamge  x.rar..."')
            cmd = 'unrar e ' + sourcefile3 + ' ' + getNeoLocation() + 'ImagesUpload/ > /dev/null 2>&1'
            rc = os.system(cmd)
            if ZipDelete == 'True':
                rc = os.system('rm -rf ' + sourcefile3)
            else:
                os.system('echo "NeoBoot keep the file:  %s  for reinstallation."' % sourcefile3)

    #Instalacja *.zip
    elif os.path.exists(sourcefile) is True:
        os.system('unzip ' + sourcefile)
        if ZipDelete == 'True':
            os.system('rm -rf ' + sourcefile)

    #Instalacja MIPS
    if getCPUtype() == 'MIPS' and not os.path.exists('/tmp/root_jffs2'):
        if os.path.exists('' + getNeoLocation() + 'ubi') is False:
            rc = os.system('mkdir ' + getNeoLocation() + 'ubi')
        to = '' + getNeoLocation() + 'ImageBoot/' + target
        cmd = 'mkdir %s > /dev/null 2<&1' % to
        rc = os.system(cmd)
        to = '' + getNeoLocation() + 'ImageBoot/' + target
        cmd = 'chmod -R 0777 %s' % to
        rc = os.system(cmd)
        rootfname = 'rootfs.bin'
        brand = ''
        #NANDSIM
        if Nandsim == 'True' and os.path.exists('/lib/modules/%s/kernel/drivers/mtd/nand/nandsim.ko' % getKernelVersion()):
            for i in range(0, 20):
                    mtdfile = '/dev/mtd' + str(i)
                    if os.path.exists(mtdfile) is False:
                        break

            mtd = str(i)
            os.chdir(media + '/ImagesUpload')
            #zgemma
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma'):
                os.chdir('zgemma')
                brand = 'zgemma'
                rootfname = 'rootfs.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/sh1'):
                    os.chdir('sh1')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/sh2'):
                    os.chdir('sh2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h2'):
                    os.chdir('h2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h3'):
                    os.chdir('h3')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h5'):
                    os.chdir('h5')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h7'):
                    os.chdir('h7')

            #miraclebox
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox'):
                os.chdir('miraclebox')
                brand = 'miraclebox'
                rootfname = 'rootfs.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini'):
                    os.chdir('mini')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/miniplus'):
                    os.chdir('miniplus')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/minihybrid'):
                    os.chdir('minihybrid')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twin'):
                    os.chdir('twin')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra'):
                    os.chdir('ultra')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/micro'):
                    os.chdir('micro')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twinplus'):
                    os.chdir('twinplus')
            #atemio
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio'):
                    os.chdir('atemio')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/5x00'):
                        os.chdir('5x00')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6000'):
                        os.chdir('6000')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6100'):
                        os.chdir('6100')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6200'):
                        os.chdir('6200')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
            #Xtrend
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et10000'):
                os.chdir('et10000')
                brand = 'et10000'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et9x00'):
                os.chdir('et9x00')
                brand = 'et9x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8500'):
                os.chdir('et8500')
                brand = 'et8500'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8000'):
                os.chdir('et8000')
                brand = 'et8000'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et7x00'):
                os.chdir('et7x00')
                brand = 'et7x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et6x00'):
                os.chdir('et6x00')
                brand = 'et6x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et5x00'):
                os.chdir('et5x00')
                brand = 'et5x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et4x00'):
                os.chdir('et4x00')
                brand = 'et4x00'
            #formuler
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler1'):
                os.chdir('formuler1')
                brand = 'formuler1'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler2'):
                os.chdir('formuler2')
                brand = 'formuler2'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler3'):
                os.chdir('formuler3')
                brand = 'formuler3'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler4turbo'):
                os.chdir('formuler4turbo')
                brand = 'formuler4turbo'
            #   Golden Interstar 
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx'):
                os.chdir('xpeedlx')
                brand = 'xpeedlx'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx3'):
                os.chdir('xpeedlx3')
                brand = 'xpeedlx3'
            #GigaBlue    
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue'):
                os.chdir('gigablue')
                brand = 'gigablue'
                rootfname = 'rootfs.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/x1'):
                    os.chdir('x1')
            #VuPlus
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus'):
                os.chdir('vuplus')
                brand = 'vuplus'
                rootfname = 'root_cfe_auto.jffs2'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno'):
                    os.chdir('uno')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo'):
                    os.chdir('duo')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo'):
                    os.chdir('ultimo')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo'):
                    os.chdir('solo')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo2'):
                    os.chdir('duo2')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo2'):
                    os.chdir('solo2')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solose'):
                    os.chdir('solose')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero'):
                    os.chdir('zero')
                    rootfname = 'root_cfe_auto.bin'

            #os_Edision
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini'):
                os.chdir('osmini')
                brand = 'osmini'
                rootfname = 'rootfs.bin'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osminiplus'):
                os.chdir('osminiplus')
                brand = 'osmini'
                rootfname = 'rootfs.bin' 
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmega'):
                os.chdir('osmega')
                brand = 'osmini'
                rootfname = 'rootfs.bin'                
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osnino'):
                os.chdir('osnino')
                brand = 'osnino'
                rootfname = 'rootfs.bin'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osninoplus'):
                os.chdir('osninoplus')
                brand = 'osnino'
                rootfname = 'rootfs.bin'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osninopro'):
                os.chdir('osninopro')
                brand = 'osnino'
                rootfname = 'rootfs.bin'
            #Vimastec
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vs1000'):
                os.chdir('vs1000')
                brand = 'vs1000'
                rootfname = 'rootfs.bin'
            #Dreambox
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm520'):
                os.chdir('dm520')
                brand = 'dm520'
                rootfname = 'rootfs.bin'
            #
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf3038'):
                os.chdir('sf3038')                
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xp1000'):
                os.chdir('xp1000')
                brand = 'xp1000'  

            #Instalacja image nandsim
            os.system('echo "Instalacja - nandsim w toku..."')
            rc = os.system('insmod /lib/modules/' + getKernelVersion() + '/kernel/drivers/mtd/nand/nandsim.ko cache_file=' + getNeoLocation() + 'image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5')#% getKernelVersion())
            cmd = 'dd if=%s of=/dev/mtdblock%s bs=2048' % (rootfname, mtd)
            rc = os.system(cmd)
            cmd = 'ubiattach /dev/ubi_ctrl -m %s -O 2048' % mtd
            rc = os.system(cmd)
            rc = os.system('mount -t ubifs ubi1_0 ' + getNeoLocation() + 'ubi')
            os.chdir('/home/root')
            cmd = 'cp -af ' + getNeoLocation() + 'ubi/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            rc = os.system('umount ' + getNeoLocation() + 'ubi')
            cmd = 'ubidetach -m %s' % mtd
            rc = os.system(cmd)
            rc = os.system('rmmod nandsim')
            rc = os.system('rm ' + getNeoLocation() + 'image_cache')

            if '.tar.xz' not in source and not os.path.exists('%s/ImageBoot/%s/etc/issue' % (media, target)):
                os.system("echo 3 > /proc/sys/vm/drop_caches")
                os.system('echo ""; echo "Nie zainstalowano systemu ! Powodem b\xc5\x82\xc4\x99du instalacji mo\xc5\xbce by\xc4\x87 kernel-module-nandsim."')
                os.system('echo "By uzyc innego narzedzia do rozpakowania image, ponow instalacje image jeszcze raz po restarcie tunera."')
                os.system('echo "RESTART ZA 15 sekund..."')
                os.system('rm -r %s/ImageBoot/%s' % (media, target))
                os.system('sleep 5; init 4; sleep 5; init 3 ')

        #UBI_READER
        elif os.path.exists('' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py') and not os.path.exists('/tmp/root_jffs2'):
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/venton-hdx'):
                    os.chdir('venton-hdx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hde'):
                    os.chdir('hde')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hdx'):
                    os.chdir('hdx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hdp'):
                    os.chdir('hdp')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox'):
                    os.chdir('miraclebox')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini'):
                        os.chdir('mini')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/miniplus'):
                        os.chdir('miniplus')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/minihybrid'):
                        os.chdir('minihybrid')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twin'):
                        os.chdir('twin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra'):
                        os.chdir('ultra')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/micro'):
                        os.chdir('micro')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/microv2'):
                        os.chdir('microv2')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twinplus'):
                        os.chdir('twinplus')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k'):
                        os.chdir('mini4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k'):
                        os.chdir('ultra4k')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio'):
                    os.chdir('atemio')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/5x00'):
                        os.chdir('5x00')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6000'):
                        os.chdir('6000')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6100'):
                        os.chdir('6100')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6200'):
                        os.chdir('6200')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx'):
                    os.chdir('xpeedlx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx3'):
                    os.chdir('xpeedlx3')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/bwidowx'):
                    os.chdir('bwidowx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/bwidowx2'):
                    os.chdir('bwidowx2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz'):
                    os.chdir('beyonwiz')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz/hdx'):
                        os.chdir('hdx')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz/hdp'):
                        os.chdir('hdp')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz/hde2'):
                        os.chdir('hde2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus'):
                    os.chdir('vuplus')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo'):
                        os.chdir('duo')
                        os.system('mv root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo'):
                        os.chdir('solo')
                        os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solose'):
                        if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solose/root_cfe_auto.bin'):
                            os.chdir('solose')
                            os.system('mv -f root_cfe_auto.bin rootfs.bin')
                        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solose/root_cfe_auto.jffs2'):
                            os.chdir('solose')
                            os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo'):
                        os.chdir('ultimo')
                        os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno'):
                        os.chdir('uno')
                        os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo2'):
                        os.chdir('solo2')
                        os.system('mv -f root_cfe_auto.bin rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo2'):
                        os.chdir('duo2')
                        os.system('mv -f root_cfe_auto.bin rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero'):
                        os.chdir('zero')
                        os.system('mv -f root_cfe_auto.bin rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k'):
                        os.chdir('solo4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k'):
                        os.chdir('uno4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k'):
                        os.chdir('ultimo4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k'):
                        os.chdir('duo4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo4kse'):
                        os.chdir('duo4kse')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k'):
                        os.chdir('zero4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse'):
                        os.chdir('uno4kse')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et10000'):
                    os.chdir('et10000')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et9x00'):
                    os.chdir('et9x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8500'):
                    os.chdir('et8500')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8000'):
                    os.chdir('et8000')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et7x00'):
                    os.chdir('et7x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et6x00'):
                    os.chdir('et6x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et5x00'):
                    os.chdir('et5x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et4x00'):
                    os.chdir('et4x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf8'):
                    os.chdir('sf')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf98'):
                    os.chdir('sf98')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf108'):
                    os.chdir('sf108')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf128'):
                    os.chdir('sf128')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf138'):
                    os.chdir('sf138')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf208'):
                    os.chdir('sf208')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf228'):
                    os.chdir('sf228')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf3038'):
                    os.chdir('sf3038')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf4008'):
                    os.chdir('sf4008')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008'):
                    os.chdir('sf8008')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue'):
                    os.chdir('gigablue')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/quad'):
                        os.chdir('quad')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/x1'):
                        os.chdir('x1')                        
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd2400'):
                    os.chdir('hd2400')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd51'):
                    os.chdir('hd51')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma'):
                    os.chdir('zgemma')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h3'):
                        os.chdir('h3')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h5'):
                        os.chdir('h5')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h7'):
                        os.chdir('h7')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm900'):
                    os.chdir('dm900')
                #os_Edision
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini'):
                    os.chdir('osmini')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osminiplus'):
                    os.chdir('osminiplus')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmega'):
                    os.chdir('osmega')                     
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osnino'):
                    os.chdir('osnino')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osninoplus'):
                    os.chdir('osninoplus')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osninopro'):
                    os.chdir('osninopro')                     
                #xp1000
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xp1000'):
                    os.chdir('xp1000')

                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler1'):
                    os.chdir('formuler1')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler2'):
                    os.chdir('formuler2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler3'):
                    os.chdir('formuler3')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler4turbo'):
                    os.chdir('formuler4turbo')
                #AZBOX - Install image VUULTIMO MIPS It works 
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/patch.e2'):
                    os.system('rm -f ' + getNeoLocation() + 'ImagesUpload/patch.e2 ')
                    os.system('echo "____NEOBOOT will not unpack this image.____"')
                    os.system('echo "____Try to install the image vuultimo mips____"')
                #Vimastec                    
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vs1000'):
                    os.chdir('vs1000')
                #Dreambox                   
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/odm520'):
                    os.chdir('odm520')                    

                #Instalacja image ubi_reader
                os.system('echo "Instalacja - ubi_reader w toku..."')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/root_cfe_auto.*'):
                    os.system('mv -f root_cfe_auto.* rootfs.bin')
                cmd = 'chmod 777 ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py'
                rc = os.system(cmd)
                cmd = 'python ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o' + getNeoLocation() + 'ubi'
                rc = os.system(cmd)
                os.chdir('/home/root')
                os.system('mv ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/%s/' % target)
                cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
                rc = os.system(cmd)

        else:
                os.system('echo "NeoBoot wykrył błąd !!! Prawdopodobnie brak ubi_reader lub nandsim."')

#ARM
    elif getCPUtype() == 'ARMv7':
        os.chdir('' + getNeoLocation() + 'ImagesUpload')
        if os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9/rootfs.ubi') or os.path.exists('' + getNeoLocation() + 'ImagesUpload/h8/rootfs.ubi'):
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9/rootfs.ubi'):
                os.chdir('h9')
            elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h8/rootfs.ubi'):
                os.chdir('h8')
            os.system('mv -f rootfs.ubi rootfs.bin')
            os.system('echo "Instalacja - ubi_reader w toku..."')
            print("[NeoBoot] Extracting UBIFS image and moving extracted image to our target")
            cmd = 'chmod 777 ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py'
            rc = os.system(cmd)
            cmd = 'python ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)
            os.chdir('/home/root')
            cmd = 'cp -af -p ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'rm -rf ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)

        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/axas'):
            os.chdir('axas')
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/axas/axashistwin'):
                os.chdir('axashistwin')
                os.system('echo "Instalacja - ubi_reader w toku..."')
                print("[NeoBoot] Extracting UBIFS image and moving extracted image to our target")
                cmd = 'chmod 777 ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py'
                rc = os.system(cmd)
                cmd = 'python ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o ' + getNeoLocation() + 'ubi'
                rc = os.system(cmd)
                os.chdir('/home/root')
                cmd = 'cp -af -p ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/' + target
                rc = os.system(cmd)
                cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
                rc = os.system(cmd)
                cmd = 'rm -rf ' + getNeoLocation() + 'ubi'
                rc = os.system(cmd)

        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et10000/rootfs.bin'):
            os.chdir('et10000')
            os.system('mv -f rootfs.bin rootfs.bin')
            os.system('echo "Instalacja - ubi_reader w toku..."')
            print("[NeoBoot] Extracting UBIFS image and moving extracted image to our target")
            cmd = 'chmod 777 ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py'
            rc = os.system(cmd)
            cmd = 'python ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)
            os.chdir('/home/root')
            cmd = 'cp -af ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'rm -rf ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)
            
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/lunix/cfe/oe_rootfs.bin'):
            os.chdir('update')      
            os.system('mv -f ' + getNeoLocation() + 'ImagesUpload/update/lunix/cfe/oe_rootfs.bin ' + getNeoLocation() + 'ImagesUpload/update/rootfs.bin')
            os.system('echo "Instalacja - ubi_reader w toku..."')
            print("[NeoBoot] Extracting UBIFS image and moving extracted image to our target")
            cmd = 'chmod 777 ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py'
            rc = os.system(cmd)
            cmd = 'python ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)
            os.chdir('/home/root')
            cmd = 'cp -af -p ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'rm -rf ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd) 
            
        #vuplus________________________
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k'):
            os.system('echo "Please wait. System installation VuPlus Solo4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k'):
            os.system('echo "Please wait. System installation dla modelu VuPlus Uno4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse'):
            os.system('echo "Please wait. System installation VuPlus Uno4kse."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k'):
            os.system('echo "Please wait. System installation VuPlus zero4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k'):
            os.system('echo "Please wait. System installation VuPlus Ultimo4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k'):
            os.system('echo "Please wait. System installation VuPlus Duo4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo4kse'):
            os.system('echo "Please wait. System installation VuPlus Duo4kse."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/duo4kse/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vuplus/duo4kse/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        #________________________________
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf4008'):
            os.system('echo "Please wait. System installation Octagon SF4008."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/sf4008/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/sf4008/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)     
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008m'):
            os.system('echo "Please wait. System installation Octagon SF8008m."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/octagon/sf8008m/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/octagon/sf8008m/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008'):
            os.system('echo "Please wait. System installation Octagon SF8008."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/octagon/sf8008/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/octagon/sf8008/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmio4k'):
            os.system('echo "Please wait. System installation EDISION osmio4k"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/osmio4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/osmio4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmio4kplus'):
            os.system('echo "Please wait. System installation EDISION osmio4kplus"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/osmio4kplus/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/osmio4kplus/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini4k'):
            os.system('echo "Please wait. System installation Edision OS mini 4K"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/osmini4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/osmini4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)            
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm900'):
            os.system('echo "Please wait. System installation Dreambox DM900."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dm900/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/dm900/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm920'):
            os.system('echo "Please wait. System installation Dreambox DM920."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dm920; tar -jxf ' + getNeoLocation() + 'ImagesUpload/dm920/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dreamtwo'):
            os.system('echo "Please wait. System installation Dreambox dreamtwo."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dreamtwo; tar -jxf ' + getNeoLocation() + 'ImagesUpload/dreamtwo/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd51/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation AX 4K Box HD51 "')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/hd51/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/hd51/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd60'):
            os.system('echo "Please wait. System installation AX HD60 4K"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/hd60/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/hd60/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd61'):
            os.system('echo "Please wait. System installation AX HD60 4K"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/hd61/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/hd61/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
#        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/unpackedzip/hd61'):
#            os.system('echo "Please wait. System installation AX 4K HD61"')
#            cmd = 'chmod -R 777 ' + getNeoLocation() + 'ImagesUpload/unpackedzip; tar -jxf ' + getNeoLocation() + 'ImagesUpload/unpackedzip/hd61/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
#            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/multibox'):
            os.system('echo "Please wait. System installation AX multi twin or combo"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/multibox/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/multibox/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/multiboxse'):
            os.system('echo "Please wait. System installation maxytec"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/multiboxse/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/multiboxse/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/axas/axasc4k'):
            os.system('echo "Please wait. System installation Axas his c4k"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/axas/axasc4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/axas/axasc4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e4hd'):
            os.system('echo "Please wait. System installation Axas E4HD 4K Ultra w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/e4hd/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/e4hd/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/quad4k'):
            os.system('echo "Please wait. System installation GigaBlue quad4k"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/gigablue/quad4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/gigablue/quad4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/ue4k'):
            os.system('echo "Please wait. System installation GigaBlue ue4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/gigablue/ue4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/gigablue/ue4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/revo4k'):
            os.system('echo "Please wait. System installation Revo4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/revo4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/update/revo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/force3uhd'):
            os.system('echo "Please wait. System installation force3uhd."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/force3uhd/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/update/force3uhd/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/galaxy4k'):
            os.system('echo "Please wait. System installation Galaxy4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/galaxy4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/update/galaxy4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h7/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma H7."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/zgemma/h7/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/zgemma/h7/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9/rootfs.ubi') or os.path.exists('' + getNeoLocation() + 'ImagesUpload/h8/rootfs.ubi'):
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9/rootfs.ubi'):
                os.chdir('h9')
            elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h8/rootfs.ubi'):
                os.chdir('h8')
            os.system('mv -f rootfs.ubi rootfs.bin')
            os.system('echo "Instalacja - ubi_reader w toku..."')
            print("[NeoBoot] Extracting UBIFS image and moving extracted image to our target")
            cmd = 'chmod 777 ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py'
            rc = os.system(cmd)
            cmd = 'python ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)
            os.chdir('/home/root')
            cmd = 'cp -af -p ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'rm -rf ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)            
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h9/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma H9S ."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/zgemma/h9/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/zgemma/h9/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h9se/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma H9SE ."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/zgemma/h9se/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/zgemma/h9se/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)    
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/i55plus/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma i55plus ."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/zgemma/i55plus/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/zgemma/i55plus/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9combo/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma h9combo ."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/h9combo/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/h9combo/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9combose/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma h9combose ."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/h9combose/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/h9combose/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h10/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma h10 ."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/h10/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/h10/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k'):
            os.system('echo "Please wait. System installation Miraclebox mini4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k'):
            os.system('echo "Please wait. System installation Miraclebox ultra4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/lunix3-4k'):
            os.system('echo "Please wait. System installation Qviart lunix3-4k w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/lunix3-4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/update/lunix3-4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/lunix4k'):
            os.system('echo "Please wait. System installation Qviart Lunix 4K w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/lunix4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/update/lunix4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)            
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dinobot/u5'):
            os.system('echo "Please wait. System installation dinobot w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dinobot/u5; tar -jxf ' + getNeoLocation() + 'ImagesUpload/dinobot/u5/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dinobot/u53'):
            os.system('echo "Please wait. System installation dinobot w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dinobot/u53; tar -jxf ' + getNeoLocation() + 'ImagesUpload/dinobot/u53/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dinobot/u5pvr'):
            os.system('echo "Please wait. System installation dinobot w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dinobot/u5pvr; tar -jxf ' + getNeoLocation() + 'ImagesUpload/dinobot/u5pvr/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dinobot/u57'):
            os.system('echo "Please wait. System installation dinobot w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dinobot/u57; tar -jxf ' + getNeoLocation() + 'ImagesUpload/dinobot/u57/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/uclan/ustym4kpro'):
            os.system('echo "Please wait. System installation ustym4kpro w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/uclan/ustym4kpro; tar -jxf ' + getNeoLocation() + 'ImagesUpload/uclan/ustym4kpro/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/ustym4kpro'):
            os.system('echo "Please wait. System installation ustym4kpro w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/ustym4kpro; tar -jxf ' + getNeoLocation() + 'ImagesUpload/ustym4kpro/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)            
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et1x000'):
            os.system('echo "Please wait. System installation GI ET-11000 4K w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/et1x000; tar -jxf ' + getNeoLocation() + 'ImagesUpload/et1x000/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e2/update'):
            os.system('echo "Please wait. System installation Ferguson Ariva 4K Combo w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/e2/update; tar -jxf ' + getNeoLocation() + 'ImagesUpload/e2/update/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz/v2'):
            os.system('echo "Please wait. System installation beyonwiz v2 4K w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/beyonwiz/v2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/beyonwiz/v2/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/amiko/viper4k'):
            os.system('echo "Please wait. System installation Amiko viper4k 4K w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/amiko/viper4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/amiko/viper4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/tmtwin4k'):
            os.system('echo "Please wait. System installation tmtwin4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/tmtwin4k/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/update/tmtwin4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/trio4k'):
            os.system('echo "Please wait. System installation trio4k 4K Combo..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/gigablue/trio4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/gigablue/trio4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/ip4k'):
            os.system('echo "Please wait. System installation gbip4k 4K..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/gigablue/ip4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/gigablue/ip4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/x34k'):
            os.system('echo "Please wait. System installation Gigablue X3 4k..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/gigablue/x34k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/gigablue/x34k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)            
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/protek4k'):
            os.system('echo "Please wait. System installation protek4k..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/protek4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/protek4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/pulse4k'):
            os.system('echo "Please wait. System installation AB-COM PULSe 4K..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/pulse4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/pulse4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/pulse4kmini'):
            os.system('echo "Please wait. System installation AB-COM PULSe 4K..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/pulse4kmini; tar -jxf ' + getNeoLocation() + 'ImagesUpload/pulse4kmini/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/bre2ze4k'):
            os.system('echo "Please wait. System installation WWIO BRE2ZE 4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/bre2ze4k; tar -jxf ' + getNeoLocation() + 'ImagesUpload/bre2ze4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        #Vimastec    
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vs1500'):
            os.system('echo "Please wait. System installation VIMASTEC VS1500 4K"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vs1500; tar -jxf ' + getNeoLocation() + 'ImagesUpload/vs1500/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/' + source + '.tar.xz'):
            os.system('echo "Please wait. System installation spakowanego w plik tar.xz w toku..."')
            os.system('cp -af ' + getNeoLocation() + 'ImagesUpload/' + source + '.tar.xz  ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz; tar -jjxf ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/' + source + '.tar.gz'):
            os.system('echo "Please wait. System installation spakowanego w plik tar.gz w toku..."')
            os.system('cp -af ' + getNeoLocation() + 'ImagesUpload/' + source + '.tar.gz  ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz; /bin/tar -xzvf ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/' + source + '.tar.bz2'):
            os.system('echo "Please wait. System installation spakowanego w plik tar.bz2 w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation spakowanego w plik tar.bz2 w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
            
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/' + source + '.mb'):
            os.system('echo "Please wait. System installation spakowanego w plik .mb w toku..."')
            os.system('cp -af ' + getNeoLocation() + 'ImagesUpload/' + source + '.mb  ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/*.tar.gz; tar -xzvf ' + getNeoLocation() + 'ImagesUpload/*.tar.gz -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif '.gz' in sourcefile4:
            os.system('cp -af ' + getNeoLocation() + 'ImagesUpload/*.tar.gz  ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz')
            cmd = '/bin/tar -xzvf ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.gz -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
            if '.gz' in sourcefile4:
                cmd = 'rm -rf ' + getNeoLocation() + 'ImagesUpload/*.gz '  ' > /dev/null 2>&1'
                rc = os.system(cmd)
                cmd = 'rm -f ' + getNeoLocation() + 'ImagesUpload/*.jpg '  ' > /dev/null 2>&1'
                rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.bin'):
            os.chdir('ImagesUpload')
            os.system('mv -f rootfs.bin rootfs.bin')
            os.system('echo "Instalacja - ubi_reader w toku..."')
            print("[NeoBoot] Extracting UBIFS image and moving extracted image to our target")
            cmd = 'chmod 777 ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py'
            rc = os.system(cmd)
            cmd = 'python ' + extensions_path + 'NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)
            os.chdir('/home/root')
            cmd = 'cp -af ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'rm -rf ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)

        else:
            os.system('echo "NeoBoot wykrył dłąd!!! Prawdopodobnie brak pliku instalacyjnego."')

    return
   
# ver. gutosie
#--------------------------------------------- 2022 ---------------------------------------------#   
#END

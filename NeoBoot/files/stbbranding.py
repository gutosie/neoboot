import sys
import os
import time
import subprocess
from glob import glob

try:
    from Tools.Directories import fileExists, SCOPE_PLUGINS
except Exception:

    def fileExists(path, mode="r"):
        return os.path.exists(path)


LinkNeoBoot = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot"

LogFile = "/tmp/NeoBoot.log"
LogFileObj = None

try:
    _  # noqa: F401
except NameError:

    def _(s):
        return s


def Log(param=""):
    """
    Basic file-backed logger handler. Modes: 'open', 'write', 'append', 'close', 'flush'.
    Returns the file object or None.
    """
    global LogFileObj
    p = str(param).lower()
    if p in ("open", "write", "append", "close"):
        if LogFileObj is not None:
            try:
                LogFileObj.close()
            except Exception:
                pass
            try:
                if LogFileObj.closed:
                    LogFileObj = None
                    try:
                        with open(LogFile, "a", encoding="utf-8", errors="ignore") as f:
                            f.write("LogFile closed properly\n")
                    except Exception:
                        print("ERROR closing LogFile!!!")
                else:
                    print("ERROR closing LogFile!!!")
            except Exception:
                LogFileObj = None

    if LogFileObj is None:
        if p in ("open", "write"):
            LogFileObj = open(LogFile, "w", encoding="utf-8", errors="ignore")
        elif p == "append":
            LogFileObj = open(LogFile, "a", encoding="utf-8", errors="ignore")
        elif p == "close":
            pass
    elif p == "flush":
        try:
            LogFileObj.flush()
        except Exception:
            pass

    return LogFileObj


def clearMemory():
    try:
        with open(
            "/proc/sys/vm/drop_caches", "w", encoding="utf-8", errors="ignore"
        ) as f:
            f.write("1\n")
    except Exception:
        pass


def LogCrashGS(line):
    try:
        location = getNeoLocation()
        target = os.path.join(location, "ImageBoot", "neoboot.log")
        if os.path.isfile(target):
            try:
                os.remove(target)
            except Exception:
                pass
        with open(target, "a", encoding="utf-8", errors="ignore") as log_file:
            log_file.write(str(line))
    except Exception:
        pass


def fileCheck(f, mode="r"):
    return fileExists(f, mode) and f


def IsImageName():
    try:
        if fileExists("/etc/issue"):
            with open("/etc/issue", "r", encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    if "BlackHole" in line or "vuplus" in line:
                        return True
    except Exception:
        pass
    return False


def mountp():
    pathmp = []
    try:
        if os.path.isfile("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    if (
                        "/dev/sd" in line
                        or "/dev/disk/by-uuid/" in line
                        or "/dev/mmc" in line
                        or "/dev/mtdblock" in line
                    ):
                        pathmp.append(
                            line.split()[1].replace(
                                "\\040", " ") + "/")
    except Exception:
        pass

    pathmp.append("/usr/share/enigma2/")
    pathmp.append("/etc/enigma2/")
    pathmp.append("/tmp/")
    return pathmp


def getSupportedTuners():
    supportedT = ""
    cfg = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/stbinfo.cfg"
    try:
        if os.path.exists(cfg):
            with open(cfg, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if getBoxHostName() and ("%s" % getBoxHostName()) in lines:
                supportedT = "%s" % getBoxHostName()
    except Exception:
        pass
    return supportedT


def getFreespace(dev):
    try:
        statdev = os.statvfs(dev)
        space = statdev.f_bavail * statdev.f_frsize // 1024
        print(("[NeoBoot] Free space on %s = %i kilobytes") % (dev, space))
        return space
    except Exception:
        return 0


def getCheckInstal1():
    neocheckinstal = "UNKNOWN"
    path = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install"
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines1 = f.read()
            if "/dev/" not in lines1:
                neocheckinstal = "1"
    except Exception:
        pass
    return neocheckinstal


def getCheckInstal2():
    neocheckinstal = "UNKNOWN"
    path = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location"
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines2 = f.read()
            if "/media/" not in lines2:
                neocheckinstal = "2"
    except Exception:
        pass
    return neocheckinstal


def getCheckInstal3():
    neocheckinstal = "UNKNOWN"
    path = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh"
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines3 = f.read()
            if "/bin/mount" not in lines3:
                neocheckinstal = "3"
    except Exception:
        pass
    return neocheckinstal


def getImageATv():
    atvimage = "UNKNOWN"
    try:
        if os.path.exists("/etc/issue.net"):
            with open("/etc/issue.net", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "openatv" in lines:
                atvimage = "okfeedCAMatv"
    except Exception:
        pass
    return atvimage


def getNeoLocation():
    locatinoneo = "UNKNOWN"
    path = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location"
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                locatino = f.readline().strip()
            if os.path.exists("/media/hdd/ImageBoot"):
                locatinoneo = "/media/hdd/"
            elif os.path.exists("/media/usb/ImageBoot"):
                locatinoneo = "/media/usb/"
            else:
                locatinoneo = locatino
    except Exception:
        pass
    return locatinoneo


def getFormat():
    neoformat = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "ext2" in lines:
                neoformat = "ext2"
            elif "ext3" in lines:
                neoformat = "ext3"
            elif "ext4" in lines:
                neoformat = "ext4"
            elif "nfs" in lines:
                neoformat = "nfs"
    except Exception:
        pass
    return neoformat


def getNEO_filesystems():
    neo_filesystems = "UNKNOWN"
    try:
        if os.path.exists("/tmp/.neo_format"):
            with open("/tmp/.neo_format", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if any(x in lines for x in ("ext2", "ext3", "ext4", "nfs")):
                neo_filesystems = "1"
    except Exception:
        pass
    return neo_filesystems


def getCPUtype():
    cpu = "UNKNOWN"
    try:
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "ARMv7" in lines:
                cpu = "ARMv7"
            elif "mips" in lines:
                cpu = "MIPS"
    except Exception:
        pass
    return cpu


def getFSTAB():
    install = "UNKNOWN"
    path = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/reading_blkid"
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "UUID" in lines:
                install = "UUID"
            else:
                install = "NOUUID"
    except Exception:
        pass
    return install


def getFSTAB2():
    install = "UNKNOWN"
    try:
        if os.path.exists("/etc/fstab"):
            with open("/etc/fstab", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "UUID" in lines:
                install = "OKinstall"
            else:
                install = "NOUUID"
    except Exception:
        pass
    return install


def getINSTALLNeo():
    neoinstall = "UNKNOWN"
    path = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/installNeo"
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            for candidate in (
                "/dev/sda1",
                "/dev/sda2",
                "/dev/sdb1",
                "/dev/sdb2",
                "/dev/sdc1",
                "/dev/sdc2",
                "/dev/sdd1",
                "/dev/sdd2",
                "/dev/sde1",
                "/dev/sde2",
                "/dev/sdf1",
                "/dev/sdg1",
                "/dev/sdg2",
                "/dev/sdh1",
                "/dev/sdh2",
            ):
                if candidate in lines:
                    neoinstall = candidate
                    break
    except Exception:
        pass
    return neoinstall


def getLocationMultiboot():
    LocationMultiboot = "UNKNOWN"
    try:
        for dev in (
            "/media/sda1",
            "/media/sda2",
            "/media/sdb1",
            "/media/sdb2",
            "/media/sdc1",
            "/media/sdc2",
            "/media/sdd1",
            "/media/sdd2",
            "/media/sde1",
            "/media/sde2",
            "/media/sdf1",
            "/media/sdf2",
            "/media/sdg1",
            "/media/sdg2",
            "/media/sdh1",
            "/media/sdh2",
        ):
            if os.path.exists(os.path.join(dev, "ImageBoot")):
                LocationMultiboot = dev.replace("/media/", "/dev/")
                break
    except Exception:
        pass
    return LocationMultiboot


def getLabelDisck():
    label = "UNKNOWN"
    path = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/reading_blkid"
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "LABEL=" in lines:
                label = "LABEL="
    except Exception:
        pass
    return label


def getNeoMountDisc():
    lines_mount = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines_mount = f.read()
    except Exception:
        pass
    return lines_mount


def getNeoMount():
    neo = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            mapping = {
                "/dev/sda1 /media/hdd": "hdd_install_/dev/sda1",
                "/dev/sdb1 /media/hdd": "hdd_install_/dev/sdb1",
                "/dev/sda2 /media/hdd": "hdd_install_/dev/sda2",
                "/dev/sdb2 /media/hdd": "hdd_install_/dev/sdb2",
                "/dev/sdc1 /media/hdd": "hdd_install_/dev/sdc1",
                "/dev/sdc2 /media/hdd": "hdd_install_/dev/sdc2",
                "/dev/sdd1 /media/hdd": "hdd_install_/dev/sdd1",
                "/dev/sdd2 /media/hdd": "hdd_install_/dev/sdd2",
                "/dev/sde1 /media/hdd": "hdd_install_/dev/sde1",
                "/dev/sde2 /media/hdd": "hdd_install_/dev/sde2",
                "/dev/sdf1 /media/hdd": "hdd_install_/dev/sdf1",
                "/dev/sdg1 /media/hdd": "hdd_install_/dev/sdg1",
                "/dev/sdg2 /media/hdd": "hdd_install_/dev/sdg2",
                "/dev/sdh1 /media/hdd": "hdd_install_/dev/sdh1",
                "/dev/sdh2 /media/hdd": "hdd_install_/dev/sdh2",
            }
            for k, v in mapping.items():
                if k in lines:
                    neo = v
                    break
    except Exception:
        pass
    return neo


def getNeoMount2():
    neo = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            mapping = {
                "/dev/sda1 /media/usb": "usb_install_/dev/sda1",
                "/dev/sdb1 /media/usb": "usb_install_/dev/sdb1",
                "/dev/sdb2 /media/usb": "usb_install_/dev/sdb2",
                "/dev/sdc1 /media/usb": "usb_install_/dev/sdc1",
                "/dev/sdd1 /media/usb": "usb_install_/dev/sdd1",
                "/dev/sde1 /media/usb": "usb_install_/dev/sde1",
                "/dev/sdf1 /media/usb": "usb_install_/dev/sdf1",
                "/dev/sdg1 /media/usb": "usb_install_/dev/sdg1",
                "/dev/sdh1 /media/usb": "usb_install_/dev/sdh1",
                "/dev/sda1 /media/usb2": "usb_install_/dev/sda1",
                "/dev/sdb1 /media/usb2": "usb_install_/dev/sdb1",
                "/dev/sdb2 /media/usb2": "usb_install_/dev/sdb2",
                "/dev/sdc1 /media/usb2": "usb_install_/dev/sdc1",
                "/dev/sdd1 /media/usb2": "usb_install_/dev/sdd1",
                "/dev/sde1 /media/usb2": "usb_install_/dev/sde1",
                "/dev/sdf1 /media/usb2": "usb_install_/dev/sdf1",
                "/dev/sdg1 /media/usb2": "usb_install_/dev/sdg1",
                "/dev/sdh1 /media/usb2": "usb_install_/dev/sdh1",
            }
            for k, v in mapping.items():
                if k in lines:
                    neo = v
                    break
    except Exception:
        pass
    return neo


def getNeoMount3():
    neo = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "/dev/sda1 /media/cf" in lines:
                neo = "cf_install_/dev/sda1"
            elif "/dev/sdb1 /media/cf" in lines:
                neo = "cf_install_/dev/sdb1"
    except Exception:
        pass
    return neo


def getNeoMount4():
    neo = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "/dev/sda1 /media/card" in lines:
                neo = "card_install_/dev/sda1"
            elif "/dev/sdb1 /media/card" in lines:
                neo = "card_install_/dev/sdb1"
    except Exception:
        pass
    return neo


def getNeoMount5():
    neo = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "/dev/sda1 /media/mmc" in lines:
                neo = "mmc_install_/dev/sda1"
            elif "/dev/sdb1 /media/mmc" in lines:
                neo = "mmc_install_/dev/sdb1"
    except Exception:
        pass
    return neo


def getCPUSoC():
    chipset = "UNKNOWN"
    try:
        if os.path.exists("/proc/stb/info/chipset"):
            with open(
                "/proc/stb/info/chipset", "r", encoding="utf-8", errors="ignore"
            ) as f:
                chipset = f.readline().strip()
            if chipset == "7405(with 3D)":
                chipset = "7405"
    except Exception:
        pass
    return chipset


def getCPUSoCModel():
    devicetree = "UNKNOWN"
    try:
        if os.path.exists("/proc/device-tree/model"):
            with open(
                "/proc/device-tree/model", "r", encoding="utf-8", errors="ignore"
            ) as f:
                devicetree = f.readline().strip()
    except Exception:
        pass
    return devicetree


def getImageNeoBoot():
    imagefile = "UNKNOWN"
    try:
        location = getNeoLocation()
        path = os.path.join(location, "ImageBoot", ".neonextboot")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                imagefile = f.readline().strip()
    except Exception:
        pass
    return imagefile


def getBoxVuModel():
    vumodel = "UNKNOWN"
    try:
        if fileExists("/proc/stb/info/vumodel") and not fileExists(
            "/proc/stb/info/boxtype"
        ):
            with open(
                "/proc/stb/info/vumodel", "r", encoding="utf-8", errors="ignore"
            ) as f:
                vumodel = f.readline().strip()
        elif fileExists("/proc/stb/info/boxtype") and not fileExists(
            "/proc/stb/info/vumodel"
        ):
            with open(
                "/proc/stb/info/boxtype", "r", encoding="utf-8", errors="ignore"
            ) as f:
                vumodel = f.readline().strip()
    except Exception:
        pass
    return vumodel


def getVuModel():
    try:
        if fileExists("/proc/stb/info/vumodel") and not fileExists("/proc/stb/info/boxtype"):
            brand = "Vu+"
            f = open("/proc/stb/info/vumodel", 'r')
            procmodel = f.readline().strip()
            f.close()
            model = procmodel.title().replace("olose", "olo SE").replace(
                "olo2se", "olo2 SE").replace("2", "²")
        return model
        
    except Exception:
        pass
    return "unknown"

def getBoxHostName():
    try:
        if os.path.exists("/etc/hostname"):
            with open("/etc/hostname", "r", encoding="utf-8", errors="ignore") as f:
                myboxname = f.readline().strip()
            return myboxname
    except Exception:
        pass
    return "unknown"


def getTunerModel():
    BOX_NAME = ""
    try:
        if os.path.isfile("/proc/stb/info/vumodel") and not os.path.isfile(
            "/proc/stb/info/boxtype"
        ):
            BOX_NAME = (
                open(
                    "/proc/stb/info/vumodel",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip())
        elif os.path.isfile("/proc/stb/info/boxtype"):
            BOX_NAME = (
                open(
                    "/proc/stb/info/boxtype",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip())
        elif os.path.isfile("/proc/stb/info/model") and not os.path.isfile(
            "/proc/stb/info/mid"
        ):
            BOX_NAME = (
                open(
                    "/proc/stb/info/model",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip())
    except Exception:
        pass
    return BOX_NAME


def getImageFolder():
    ImageFolder = None
    try:
        if os.path.isfile("/proc/stb/info/vumodel"):
            BOX_NAME = getBoxModelVU()
            ImageFolder = "vuplus/" + BOX_NAME
    except Exception:
        pass
    return ImageFolder


def getKernelVersion():
    try:
        with open("/proc/version", "r", encoding="utf-8", errors="ignore") as f:
            return f.read().split(" ", 4)[2].split("-", 2)[0]
    except Exception:
        return _("unknown")


def runCMDS(cmdsList):
    """
    Run commands. Accepts a string or list/tuple of strings.
    Returns the return code (int).
    """
    clearMemory()
    if isinstance(cmdsList, (list, tuple)):
        myCMD = "\n".join(str(x) for x in cmdsList)
    else:
        myCMD = str(cmdsList)
    try:
        result = subprocess.run(myCMD, shell=True)
        return result.returncode
    except Exception:
        return -1


def getImageDistroN():
    image = "Internal storage"
    try:
        if fileExists("/.multinfo") and fileExists(
            "%sImageBoot/.imagedistro" % getNeoLocation()
        ):
            with open(
                "%sImageBoot/.imagedistro" % getNeoLocation(),
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                image = f.readline().strip()
        elif not fileExists("/.multinfo") and fileExists("/etc/vtiversion.info"):
            with open(
                "/etc/vtiversion.info", "r", encoding="utf-8", errors="ignore"
            ) as f:
                imagever = f.readline().strip().replace("Release ", " ")
            image = imagever
        elif not fileExists("/.multinfo") and fileExists("/etc/bhversion"):
            with open("/etc/bhversion", "r", encoding="utf-8", errors="ignore") as f:
                imagever = f.readline().strip()
            image = imagever
        elif fileExists("/.multinfo") and fileExists("/etc/bhversion"):
            image = "Flash " + " " + getBoxHostName()
        elif fileExists("/.multinfo") and fileExists("/etc/vtiversion.info"):
            image = "Flash " + " " + getBoxHostName()
        elif fileExists("/usr/lib/enigma2/python/boxbranding.so") and not fileExists(
            "/.multinfo"
        ):
            try:
                from boxbranding import getImageDistro

                image = getImageDistro()
            except Exception:
                pass
        elif (
            fileExists("/media/InternalFlash/etc/issue.net")
            and fileExists("/.multinfo")
            and not fileExists("%sImageBoot/.imagedistro" % getNeoLocation())
        ):
            with open(
                "/media/InternalFlash/etc/issue.net",
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                obraz = f.readlines()
            imagetype = obraz[0][:-3] if obraz else ""
            image = imagetype
        elif fileExists("/etc/issue.net") and not fileExists("/.multinfo"):
            with open("/etc/issue.net", "r", encoding="utf-8", errors="ignore") as f:
                obraz = f.readlines()
            imagetype = obraz[0][:-3] if obraz else ""
            image = imagetype
        else:
            image = "Inernal Flash " + " " + getBoxHostName()
    except Exception:
        pass
    return image


def getKernelVersionString():
    """
    Preferred: use uname -r. Fallback to /proc/version parsing.
    """
    try:
        out = subprocess.check_output(["uname", "-r"])
        kernel_version = out.decode(
            "utf-8", errors="ignore").strip().split("-")[0]
        return kernel_version
    except Exception:
        try:
            with open("/proc/version", "r", encoding="utf-8", errors="ignore") as f:
                return f.read().split(" ", 4)[2].split("-", 2)[0]
        except Exception:
            return "unknown"


def getKernelImageVersion():
    try:
        ctrl_files = glob("/var/lib/opkg/info/kernel-*.control")
        if ctrl_files:
            lines = open(
                ctrl_files[0], "r", encoding="utf-8", errors="ignore"
            ).readlines()
            if len(lines) > 1:
                kernelimage = lines[1].rstrip("\n")
                return kernelimage
    except Exception:
        pass
    return getKernelVersionString()


def getTypBoxa():
    try:
        if not fileExists("/etc/typboxa"):
            with open("/etc/hostname", "r", encoding="utf-8", errors="ignore") as f2:
                mypath2 = f2.readline().strip()
            mapping = {
                "vuuno": "Vu+Uno ",
                "vuultimo": "Vu+Ultimo ",
                "vuduo": "Vu+Duo ",
                "vuduo2": "Vu+Duo2 ",
                "vusolo": "Vu+Solo ",
                "vusolo2": "Vu+Solo2 ",
                "vusolose": "Vu+Solo-SE ",
                "vuvzero": "Vu+Zero ",
                "vuuno4k": "Vu+Uno4k ",
                "vuultimo4k": "Vu+Ultimo4k ",
                "vusolo4k": "Vu+Solo4k ",
                "mbmini": "Miraclebox-Mini ",
                "mutant51": "Mutant 51 ",
                "sf4008": "Ocatgon sf4008 ",
                "novaler4kpro": "Novaler Multibox Pro ",
                "ax51": "ax51 ",
            }
            val = mapping.get(mypath2, None)
            with open("/etc/typboxa", "w", encoding="utf-8", errors="ignore") as out:
                if val:
                    out.write(val)
                else:
                    out.write("unknown")
        with open("/etc/typboxa", "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
            typboxa = lines[0].rstrip("\n") if lines else "not detected"
        return typboxa
    except Exception:
        return "not detected"


def getImageVersionString():
    try:
        st = None
        if os.path.isfile("/var/lib/opkg/status"):
            st = os.stat("/var/lib/opkg/status")
        elif os.path.isfile("/usr/lib/ipkg/status"):
            st = os.stat("/usr/lib/ipkg/status")
        if st:
            tm = time.localtime(st.st_mtime)
            if tm.tm_year >= 2015:
                return time.strftime("%Y-%m-%d %H:%M:%S", tm)
    except Exception:
        pass
    return _("unavailable")


def getModelString():
    try:
        with open(
            "/proc/stb/info/boxtype", "r", encoding="utf-8", errors="ignore"
        ) as file:
            model = file.readline().strip()
        return model
    except Exception:
        return "unknown"


def getChipSetString():
    try:
        with open(
            "/proc/stb/info/chipset", "r", encoding="utf-8", errors="ignore"
        ) as f:
            chipset = f.read()
        return str(chipset.lower().replace("\n", "").replace("bcm", ""))
    except Exception:
        return "unavailable"


def getCPUString():
    try:
        system = "unavailable"
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
            for x in lines:
                splitted = x.split(": ")
                if len(splitted) > 1:
                    splitted[1] = splitted[1].replace("\n", "")
                    if splitted[0].startswith("system type"):
                        system = splitted[1].split(" ")[0]
                    elif splitted[0].startswith("Processor"):
                        system = splitted[1].split(" ")[0]
        return system
    except Exception:
        return "unavailable"


def getCpuCoresString():
    try:
        cores = 1
        with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as file:
            lines = file.readlines()
            for x in lines:
                splitted = x.split(": ")
                if len(splitted) > 1:
                    splitted[1] = splitted[1].replace("\n", "")
                    if splitted[0].startswith("processor"):
                        if int(splitted[1]) > 0:
                            cores = 2
                        else:
                            cores = 1
        return cores
    except Exception:
        return "unavailable"


def getEnigmaVersionString():
    try:
        import enigma

        enigma_version = enigma.getEnigmaVersionString()
        if "-(no branch)" in enigma_version:
            enigma_version = enigma_version[:-12]
        return enigma_version
    except Exception:
        return _("unavailable")


def getHardwareTypeString():
    try:
        if os.path.isfile("/proc/stb/info/boxtype"):
            boxtype = (
                open(
                    "/proc/stb/info/boxtype",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip())
            board_rev = (
                open(
                    "/proc/stb/info/board_revision",
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                )
                .read()
                .strip()
            )
            version = (
                open(
                    "/proc/stb/info/version",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip())
            return boxtype.upper() + " (" + board_rev + "-" + version + ")"
        if os.path.isfile("/proc/stb/info/vumodel"):
            return (
                "VU+" +
                open(
                    "/proc/stb/info/vumodel",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip() .upper() +
                "(" +
                open(
                    "/proc/stb/info/version",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip() .upper() +
                ")")
        if os.path.isfile("/proc/stb/info/model"):
            return (
                open(
                    "/proc/stb/info/model",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip() .upper())
    except Exception:
        pass
    return _("unavailable")


def getImageTypeString():
    try:
        lines = open(
            "/etc/issue",
            "r",
            encoding="utf-8",
            errors="ignore").readlines()
        if len(lines) >= 2:
            return lines[-2].capitalize().strip()[:-6]
    except Exception:
        pass
    return _("undefined")


def getMachineBuild():
    try:
        with open("/proc/version", "r", encoding="utf-8", errors="ignore") as f:
            return f.read().split(" ", 4)[2].split("-", 2)[0]
    except Exception:
        return "unknown"


def getVuBoxModel():
    BOX_MODEL = "not detected"
    try:
        if fileExists("/proc/stb/info/vumodel"):
            with open(
                "/proc/stb/info/vumodel", "r", encoding="utf-8", errors="ignore"
            ) as l:
                model = l.read()
            BOX_NAME = str(model.lower().strip())
            BOX_MODEL = "vuplus"
    except Exception:
        BOX_MODEL = "not detected"
    return BOX_MODEL


def getBoxModelVU():
    try:
        if os.path.isfile("/proc/stb/info/vumodel"):
            return (
                open(
                    "/proc/stb/info/vumodel",
                    "r",
                    encoding="utf-8",
                    errors="ignore") .read() .strip() .upper())
    except Exception:
        pass
    return _("unavailable")


def getMachineProcModel():
    procmodel = "unknown"
    try:
        if os.path.isfile("/proc/stb/info/vumodel"):
            BOX_NAME = getBoxModelVU().lower()
            BOX_MODEL = getVuBoxModel()
            if BOX_MODEL == "vuplus":
                mapping = {
                    "duo": "bcm7335",
                    "solo": "bcm7325",
                    "solo2": "bcm7346",
                    "solose": "bcm7241",
                    "ultimo": "bcm7413",
                    "uno": "bcm7413",
                    "zero": "bcm7362",
                    "duo2": "bcm7425",
                    "ultimo4k": "bcm7444S",
                    "uno4k": "bcm7252S",
                    "solo4k": "bcm7376",
                    "zero4k": "bcm72604",
                    "uno4kse": "",
                }
                procmodel = mapping.get(BOX_NAME, "unknown")
    except Exception:
        pass
    return procmodel


def getMountPointAll():
    try:
        script = os.path.join(LinkNeoBoot, "files", "mountpoint.sh")
        os.makedirs(os.path.dirname(script), exist_ok=True)
        with open(script, "w", encoding="utf-8", errors="ignore") as f:
            f.write("#!/bin/sh\n")
        os.chmod(script, 0o755)

        nm = getNeoMount()
        if nm.startswith("hdd_install_"):
            dev = nm.split("_")[-1]
            os.system(
                'echo "umount -l /media/hdd\nmkdir -p /media/hdd\nmkdir -p %s\n/bin/mount %s /media/hdd\n/bin/mount %s %s"  >> %s' %
                (dev.replace(
                    "/dev/",
                    "/media/"),
                    dev,
                    dev,
                    dev.replace(
                    "/dev/",
                    "/"),
                    script,
                 ))
        with open(script, "a", encoding="utf-8", errors="ignore") as f:
            f.write("\n\nexit 0\n")
    except Exception:
        pass


def getMountPointNeo():
    try:
        script = os.path.join(LinkNeoBoot, "files", "mountpoint.sh")
        os.system(script)
        os.system(
            "echo "
            + getLocationMultiboot()
            + " > "
            + os.path.join(LinkNeoBoot, "bin", "install")
            + "; chmod 0755 "
            + os.path.join(LinkNeoBoot, "bin", "install")
        )
        lm = getLocationMultiboot()
        if lm and lm != "UNKNOWN":
            outpath = os.path.join(LinkNeoBoot, "files", "neo.sh")
            dev = lm
            with open(outpath, "w", encoding="utf-8", errors="ignore") as out:
                out.write(
                    "#!/bin/sh\n\n/bin/mount %s %s  \n\nexit 0"
                    % (dev, getNeoLocation())
                )
            os.chmod(outpath, 0o755)
    except Exception:
        pass


def getMountPointNeo2():
    try:
        script = os.path.join(LinkNeoBoot, "files", "mountpoint.sh")
        with open(script, "w", encoding="utf-8", errors="ignore") as f:
            f.write("#!/bin/sh\n")
        os.chmod(script, 0o755)
        nm = getNeoMount()
        if nm != "UNKNOWN":
            dev = nm.split("_")[-1]
            os.system(
                'echo "umount -l /media/hdd\nmkdir -p /media/hdd\n/bin/mount %s /media/hdd"  >> %s' %
                (dev, script))
        with open(script, "a", encoding="utf-8", errors="ignore") as f:
            f.write("\n\nexit 0\n")
    except Exception:
        pass


def getBoxMacAddres():
    ethernetmac = "UNKNOWN"
    try:
        if not fileExists("/etc/.nameneo"):
            try:
                with open("/tmp/.mymac", "w", encoding="utf-8", errors="ignore") as fh:
                    out = subprocess.check_output(
                        ["ifconfig", "-a"], stderr=subprocess.DEVNULL
                    )
                    fh.write(out.decode("utf-8", errors="ignore"))
            except Exception:
                pass
        if os.path.exists("/etc/.nameneo"):
            with open("/etc/.nameneo", "r", encoding="utf-8", errors="ignore") as f:
                ethernetmac = f.readline().strip()
            try:
                subprocess.run(
                    ["cp", "-r", "/etc/.nameneo", "/tmp/.mymac"], check=False
                )
            except Exception:
                pass
        elif fileExists("/tmp/.mymac"):
            with open("/tmp/.mymac", "r", encoding="utf-8", errors="ignore") as f:
                myboxmac = (
                    f.readline()
                    .strip()
                    .replace("eth0      Link encap:Ethernet  HWaddr ", "")
                )
            ethernetmac = myboxmac
            try:
                with open(
                    "/tmp/.mymac", "w", encoding="utf-8", errors="ignore"
                ) as writefile:
                    writefile.write(myboxmac)
            except Exception:
                pass
        else:
            ethernetmac = "12:34:56:78:91:02"
    except Exception:
        pass
    return ethernetmac


def getCheckActivateVip():
    supportedvip = ""
    try:
        path = "/usr/lib/periodon/.activatedmac"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "%s" % getBoxMacAddres() in lines:
                supportedvip = "%s" % getBoxMacAddres()
    except Exception:
        pass
    return supportedvip


def getMountDiskSTB():
    neo_disk = " "
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            for dev in (
                "sda1",
                "sdb1",
                "sda2",
                "sdb2",
                "sdc1",
                "sdd1",
                "sde1",
                "sdf1",
                "sdg1",
                "sdh1",
            ):
                if f"/dev/{dev} /media/hdd" in lines:
                    os.system(
                        f"touch /tmp/disk/{dev}; touch /tmp/disk/#---Select_the_disk_HDD:")
                if f"/dev/{dev} /media/usb" in lines:
                    os.system(
                        f"touch /tmp/disk/{dev}; touch /tmp/disk/#---Select_the_disk_USB:")
    except Exception:
        pass
    return neo_disk


def getCheckExtDisk():
    try:
        subprocess.run(
            "cat /proc/mounts | egrep -o '.ext.' | sort | uniq > /tmp/.myext",
            shell=True,
        )
        if os.path.exists("/tmp/.myext"):
            with open("/tmp/.myext", "r", encoding="utf-8", errors="ignore") as f:
                myboxEXT = f.readline().strip()
            return myboxEXT
    except Exception:
        pass
    return "UNKNOWN"


def getCheckExt():
    neoExt = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if "/media/usb vfat" in lines or "/media/hdd vfat" in lines:
                neoExt = "vfat"
            elif "/media/hdd ext3" in lines or "/media/usb ext3" in lines:
                neoExt = "ext3"
            elif "/media/hdd ext4" in lines or "/media/usb ext4" in lines:
                neoExt = "ext4"
    except Exception:
        pass
    return neoExt


def getExtCheckHddUsb():
    neoExt = "UNKNOWN"
    try:
        if os.path.exists("/proc/mounts"):
            with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as f:
                lines = f.read()
            if (
                ("/media/hdd ext4" in lines) or ("/media/hdd type ext4" in lines)
            ) and os.path.exists("/media/hdd/ImageBoot"):
                neoExt = "ext4"
            if (
                ("/media/usb ext4" in lines) or ("/media/usb type ext4" in lines)
            ) and os.path.exists("/media/usb/ImageBoot"):
                neoExt = "ext4"
    except Exception:
        pass
    return neoExt


def getNandWrite():
    NandWrite = "NandWrite"
    try:
        if os.path.exists("/usr/sbin/nandwrite"):
            try:
                with open(
                    "/usr/sbin/nandwrite", "r", encoding="utf-8", errors="ignore"
                ) as f:
                    lines = f.read()
                if "nandwrite" in lines:
                    NandWrite = "nandwrite"
            except Exception:
                NandWrite = "nandwrite"
        else:
            NandWrite = "no_nandwrite"
    except Exception:
        pass
    return NandWrite


def getMyUUID():
    try:
        lm = getLocationMultiboot()
        if lm and lm != "UNKNOWN":
            subprocess.run(
                "tune2fs -l %s | awk '/UUID/ {print $NF}' > /tmp/.myuuid" %
                (lm,), shell=True, )
            if os.path.isfile("/tmp/.myuuid"):
                return (
                    open(
                        "/tmp/.myuuid",
                        "r",
                        encoding="utf-8",
                        errors="ignore") .read() .strip() .upper())
    except Exception:
        pass
    return _("unavailable")


def getImageBootNow():
    imagefile = "UNKNOWN"
    try:
        if os.path.exists("/.multinfo"):
            with open("/.multinfo", "r", encoding="utf-8", errors="ignore") as f:
                imagefile = f.readline().strip()
    except Exception:
        pass
    return imagefile


def getNeoActivatedtest():
    neoactivated = "NEOBOOT MULTIBOOT"
    try:
        if not fileExists("/.multinfo"):
            if getCheckActivateVip() != getBoxMacAddres():
                neoactivated = "Ethernet MAC not found."
            elif not fileExists("/usr/lib/periodon/.kodn"):
                neoactivated = "VIP Pin code missing."
            else:
                try:
                    if getCheckActivateVip() == getBoxMacAddres(
                    ) and fileExists("/usr/lib/periodon/.kodn"):
                        neoactivated = "NEOBOOT VIP ACTIVATED"
                except Exception:
                    neoactivated = "NEOBOOT MULTIBOOT"
    except Exception:
        pass
    return neoactivated


boxbrand = sys.modules[__name__]

from Plugins.Extensions.NeoBoot.__init__ import _
import os
import time
import subprocess
from Tools.Directories import fileExists, pathExists
from Tools.CList import CList
from Components.SystemInfo import SystemInfo
from Components.Console import Console

if fileExists("/usr/lib/python2.7"):
    from Plugins.Extensions.NeoBoot.files import Task
else:
    from Components import Task
try:
    from Plugins.Extensions.NeoBoot.files.Task import LoggingTask
except Exception:
    from Components.Task import LoggingTask
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.MessageBox import MessageBox


def readFile(filename):
    try:
        with open(filename, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read().strip()
    except Exception:
        return ""


def getProcMounts():
    """
    Returns a list of mount entries where each entry is a list of fields from /proc/mounts.
    Replaces '\040' with space in mount points as /proc/mounts encodes spaces as '\040'.
    """
    try:
        with open("/proc/mounts", "r", encoding="utf-8", errors="ignore") as mounts:
            result = [line.strip().split(" ") for line in mounts]
    except IOError as ex:
        print("[Harddisk] Failed to open /proc/mounts:", ex)
        return []

    for item in result:
        if len(item) > 1:
            item[1] = item[1].replace("\\040", " ")
    return result


def getNonNetworkMediaMounts():
    return [
        x[1]
        for x in getProcMounts()
        if x and len(x) > 1 and x[1].startswith("/media/") and not x[0].startswith("//")
    ]


def isFileSystemSupported(filesystem):
    try:
        with open("/proc/filesystems", "r", encoding="utf-8", errors="ignore") as fh:
            for fs in fh:
                if fs.strip().endswith(filesystem):
                    return True
        return False
    except Exception as ex:
        print("[Harddisk] Failed to read /proc/filesystems:", ex)
        return False


def findMountPoint(path):
    path = os.path.abspath(path)
    while not os.path.ismount(path):
        path = os.path.dirname(path)
    return path


DEVTYPE_UDEV = 0
DEVTYPE_DEVFS = 1


class Harddisk:

    def __init__(self, device, removable=False):
        self.device = device
        if os.path.exists("/dev/.udev"):
            self.type = DEVTYPE_UDEV
        elif os.path.exists("/dev/.devfsd"):
            self.type = DEVTYPE_DEVFS
        else:
            print("[Harddisk] Unable to determine structure of /dev")
            self.type = -1
            self.card = False

        self.max_idle_time = 0
        self.idle_running = False
        self.last_access = time.time()
        self.last_stat = 0
        self.timer = None
        self.is_sleeping = False
        self.dev_path = ""
        self.disk_path = ""
        self.mount_path = None
        self.mount_device = None
        try:
            self.phys_path = os.path.realpath(self.sysfsPath("device"))
        except Exception:
            self.phys_path = ""
        self.removable = removable
        self.internal = (
            "pci" in self.phys_path
            or "ahci" in self.phys_path
            or "sata" in self.phys_path
        )
        try:
            with open(
                "/sys/block/%s/queue/rotational" % device,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                data = f.read().strip()
            self.rotational = int(data)
        except Exception:
            self.rotational = True

        if self.type == DEVTYPE_UDEV:
            self.dev_path = "/dev/" + self.device
            self.disk_path = self.dev_path
            self.card = "sdhci" in self.phys_path
        elif self.type == DEVTYPE_DEVFS:
            tmp = (
                readFile(self.sysfsPath("dev")).split(":")
                if readFile(self.sysfsPath("dev"))
                else ["0", "0"]
            )
            try:
                s_major = int(tmp[0])
                s_minor = int(tmp[1])
            except Exception:
                s_major = s_minor = 0
            for disc in (os.listdir("/dev/discs")
                         if os.path.exists("/dev/discs") else []):
                dev_path = os.path.realpath("/dev/discs/" + disc)
                disk_path = dev_path + "/disc"
                try:
                    rdev = os.stat(disk_path).st_rdev
                except OSError:
                    continue

                if s_major == os.major(rdev) and s_minor == os.minor(rdev):
                    self.dev_path = dev_path
                    self.disk_path = disk_path
                    break

            self.card = self.device[:2] == "hd" and "host0" not in self.dev_path
        print(
            "[Harddisk] new device",
            self.device,
            "->",
            self.dev_path,
            "->",
            self.disk_path,
        )
        if not removable and not getattr(self, "card", False):
            try:
                self.startIdle()
            except Exception:
                pass
        return

    def __lt__(self, ob):
        return self.device < ob.device

    def partitionPath(self, n):
        n_str = str(n)
        if self.type == DEVTYPE_UDEV:
            if self.dev_path.startswith("/dev/mmcblk0"):
                return self.dev_path + "p" + n_str
            else:
                return self.dev_path + n_str
        elif self.type == DEVTYPE_DEVFS:
            return self.dev_path + "/part" + n_str

    def sysfsPath(self, filename):
        return os.path.join("/sys/block/", self.device, filename)

    def stop(self):
        if self.timer:
            try:
                self.timer.stop()
                try:
                    self.timer.callback.remove(self.runIdle)
                except Exception:
                    pass
            except Exception:
                pass

    def bus(self):
        ret = _("External")
        type_name = ""
        if self.type == DEVTYPE_UDEV:
            type_name = " (SD/MMC)"
        elif self.type == DEVTYPE_DEVFS:
            type_name = " (CF)"
        if getattr(self, "card", False):
            ret += type_name
        else:
            if self.internal:
                ret = _("Internal")
            if not self.rotational:
                ret += " (SSD)"
        return ret

    def diskSize(self):
        cap = 0
        try:
            line = readFile(self.sysfsPath("size"))
            cap = int(line) if line else 0
            return (cap * 512) // 1000000
        except Exception:
            dev = self.findMount()
            if dev:
                try:
                    stat = os.statvfs(dev)
                    cap_bytes = int(stat.f_blocks * stat.f_bsize)
                    return cap_bytes // 1000000
                except Exception:
                    pass

        return cap

    def capacity(self):
        cap = self.diskSize()
        if cap == 0:
            return ""
        if cap < 1000:
            return _("%03d MB") % cap
        return _("%d.%03d GB") % (cap // 1000, cap % 1000)

    def model(self):
        try:
            if self.device[:2] == "hd":
                return readFile("/proc/ide/" + self.device + "/model")
            if self.device[:2] == "sd":
                vendor = readFile(self.sysfsPath("device/vendor"))
                model = readFile(self.sysfsPath("device/model"))
                return vendor + "(" + model + ")"
            if self.device.startswith("mmcblk0"):
                return readFile(self.sysfsPath("device/name"))
            raise Exception("unknown device type")
        except Exception as e:
            print("[Harddisk] Failed to get model:", e)
            return "-?-"

    def free(self):
        dev = self.findMount()
        if dev:
            try:
                stat = os.statvfs(dev)
                return stat.f_bavail * stat.f_bsize
            except Exception:
                pass
        return -1

    def numPartitions(self):
        numPart = -1
        if self.type == DEVTYPE_UDEV:
            try:
                devdir = os.listdir("/dev")
            except OSError:
                return -1

            for filename in devdir:
                if filename.startswith(self.device):
                    numPart += 1

        elif self.type == DEVTYPE_DEVFS:
            try:
                idedir = os.listdir(self.dev_path)
            except OSError:
                return -1

            for filename in idedir:
                if filename.startswith("disc"):
                    numPart += 1
                if filename.startswith("part"):
                    numPart += 1

        return numPart

    def mountDevice(self):
        for parts in getProcMounts():
            if not parts:
                continue
            try:
                if os.path.realpath(parts[0]).startswith(self.dev_path):
                    self.mount_device = parts[0]
                    self.mount_path = parts[1]
                    return parts[1]
            except Exception:
                continue
        return None

    def enumMountDevices(self):
        for parts in getProcMounts():
            if parts and len(parts) > 0:
                try:
                    if os.path.realpath(parts[0]).startswith(self.dev_path):
                        yield parts[1]
                except Exception:
                    continue

    def findMount(self):
        if self.mount_path is None:
            return self.mountDevice()
        else:
            return self.mount_path

    def unmount(self):
        dev = self.mountDevice()
        if dev is None:
            return 0
        else:
            cmd = ["umount", dev]
            print("[Harddisk]", " ".join(cmd))
            try:
                res = subprocess.run(cmd)
                return res.returncode
            except Exception:
                return -1

    def createPartition(self):
        cmd = 'printf "8,\n;0,0\n;0,0\n;0,0\ny\n" | sfdisk -f -uS ' + self.disk_path
        try:
            res = subprocess.run(cmd, shell=True)
            return res.returncode
        except Exception:
            return -1

    def mkfs(self):
        return 1

    def mount(self):
        if self.mount_device is None:
            dev = self.partitionPath("1")
        else:
            dev = self.mount_device
        try:
            with open("/etc/fstab", "r", encoding="utf-8", errors="ignore") as fstab:
                lines = fstab.readlines()
        except IOError:
            return -1

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            fspath = os.path.realpath(parts[0])
            if fspath == dev:
                print("[Harddisk] mounting:", fspath)
                try:
                    res = subprocess.run(["mount", "-t", "auto", fspath])
                    return res.returncode
                except Exception:
                    return -1

        res = -1
        if self.type == DEVTYPE_UDEV:
            try:
                subprocess.run(["hdparm", "-z", self.disk_path])
                from time import sleep

                sleep(3)
            except Exception:
                pass
        return res

    def fsck(self):
        return 1

    def killPartitionTable(self):
        zero = 512 * b"\x00"
        try:
            with open(self.dev_path, "wb") as h:
                for i in range(9):
                    h.write(zero)
        except Exception as ex:
            print("[Harddisk] killPartitionTable failed:", ex)

    def killPartition(self, n):
        zero = 512 * b"\x00"
        part = self.partitionPath(n)
        try:
            with open(part, "wb") as h:
                for i in range(3):
                    h.write(zero)
        except Exception as ex:
            print("[Harddisk] killPartition failed:", ex)

    def createInitializeJob(self):
        job = Task.Job(_("Initializing storage device..."))
        size = self.diskSize()
        print("[HD] size: %s MB" % size)
        task = UnmountTask(job, self)
        task = Task.PythonTask(job, _("Removing partition table"))
        task.work = self.killPartitionTable
        task.weighting = 1
        task = Task.LoggingTask(job, _("Rereading partition table"))
        task.weighting = 1
        task.setTool("hdparm")
        task.args.append("-z")
        task.args.append(self.disk_path)
        task = Task.ConditionTask(
            job, _("Waiting for partition"), timeoutCount=20)
        task.check = lambda: not os.path.exists(self.partitionPath("1"))
        task.weighting = 1
        if os.path.exists("/usr/sbin/parted"):
            use_parted = True
        elif size > 2097151:
            addInstallTask(job, "parted")
            use_parted = True
        else:
            use_parted = False
        task = Task.LoggingTask(job, _("Creating partition"))
        task.weighting = 5
        if use_parted:
            task.setTool("parted")
            if size < 1024:
                alignment = "min"
            else:
                alignment = "opt"
            if size > 2097151:
                parttype = "gpt"
            else:
                parttype = "msdos"
            task.args += [
                "-a",
                alignment,
                "-s",
                self.disk_path,
                "mklabel",
                parttype,
                "mkpart",
                "primary",
                "0%",
                "100%",
            ]
        else:
            task.setTool("sfdisk")
            task.args.append("-f")
            task.args.append("-uS")
            task.args.append(self.disk_path)
            if size > 128000:
                print("[HD] Detected >128GB disk, using 4k alignment")
                task.initial_input = "8,,L\n;0,0\n;0,0\n;0,0\ny\n"
            else:
                task.initial_input = ",,L\n;\n;\n;\ny\n"
        task = Task.ConditionTask(job, _("Waiting for partition"))
        task.check = lambda: os.path.exists(self.partitionPath("1"))
        task.weighting = 1
        task = MkfsTask(job, _("Creating filesystem"))
        big_o_options = ["dir_index"]

        task.setTool("mkfs.ext3")
        if size > 250000:
            task.args += ["-T", "largefile", "-N", "262144"]
            big_o_options.append("sparse_super")
        elif size > 16384:
            task.args += ["-T", "largefile"]
            big_o_options.append("sparse_super")
        elif size > 2048:
            task.args += ["-T", "largefile", "-N", str(size * 32)]
        task.args += ["-m0",
                      "-O",
                      ",".join(big_o_options),
                      self.partitionPath("1")]
        task = MountTask(job, self)
        task.weighting = 3
        task = Task.ConditionTask(job, _("Waiting for mount"), timeoutCount=20)
        task.check = self.mountDevice
        task.weighting = 1
        return job

    def initialize(self):
        return -5

    def check(self):
        return -5

    def createCheckJob(self):
        job = Task.Job(_("Checking filesystem..."))
        if self.findMount():
            UnmountTask(job, self)
            dev = self.mount_device
        else:
            dev = self.partitionPath("1")
        task = Task.LoggingTask(job, "fsck")
        task.setTool("fsck.ext3")
        task.args.append("-f")
        task.args.append("-p")
        task.args.append(dev)
        MountTask(job, self)
        task = Task.ConditionTask(job, _("Waiting for mount"))
        task.check = self.mountDevice
        return job

    def getDeviceDir(self):
        return self.dev_path

    def getDeviceName(self):
        return self.disk_path

    def readStats(self):
        try:
            with open(
                "/sys/block/%s/stat" % self.device,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                l = f.read()
        except IOError:
            return (-1, -1)

        data = l.split(None, 5)
        try:
            return (int(data[0]), int(data[4]))
        except Exception:
            return (-1, -1)

    def startIdle(self):
        try:
            from enigma import eTimer
        except Exception:
            eTimer = None

        if self.bus() == _("External"):
            Console().ePopen(("sdparm", "sdparm", "--set=SCT=0", self.disk_path))
        else:
            Console().ePopen(("hdparm", "hdparm", "-S0", self.disk_path))
        if eTimer is None:
            return
        self.timer = eTimer()
        self.timer.callback.append(self.runIdle)
        self.idle_running = True
        self.setIdleTime(self.max_idle_time)

    def runIdle(self):
        if not self.max_idle_time:
            return
        t = time.time()
        idle_time = t - self.last_access
        stats = self.readStats()
        l = sum(stats) if isinstance(stats, (list, tuple)) else 0
        if l != self.last_stat and l >= 0:
            self.last_stat = l
            self.last_access = t
            idle_time = 0
            self.is_sleeping = False
        if idle_time >= self.max_idle_time and not self.is_sleeping:
            self.setSleep()
            self.is_sleeping = True

    def setSleep(self):
        if self.bus() == _("External"):
            Console().ePopen(
                (
                    "sdparm",
                    "sdparm",
                    "--flexible",
                    "--readonly",
                    "--command=stop",
                    self.disk_path,
                )
            )
        else:
            Console().ePopen(("hdparm", "hdparm", "-y", self.disk_path))

    def setIdleTime(self, idle):
        self.max_idle_time = idle
        if self.idle_running and self.timer:
            if not idle:
                try:
                    self.timer.stop()
                except Exception:
                    pass
            else:
                try:
                    self.timer.start(int(idle * 100), False)
                except Exception:
                    pass

    def isSleeping(self):
        return self.is_sleeping


class Partition:

    def __init__(
            self,
            mountpoint,
            device=None,
            description="",
            force_mounted=False):
        self.mountpoint = mountpoint
        self.description = description
        self.force_mounted = bool(mountpoint) and force_mounted
        self.is_hotplug = force_mounted
        self.device = device

    def __str__(self):
        return "Partition(mountpoint=%s,description=%s,device=%s)" % (
            self.mountpoint,
            self.description,
            self.device,
        )

    def stat(self):
        if self.mountpoint:
            return os.statvfs(self.mountpoint)
        raise OSError("Device %s is not mounted" % self.device)

    def free(self):
        try:
            s = self.stat()
            return s.f_bavail * s.f_bsize
        except OSError:
            return None

    def total(self):
        try:
            s = self.stat()
            return s.f_blocks * s.f_bsize
        except OSError:
            return None

    def tabbedDescription(self):
        if self.mountpoint.startswith(
                "/media/net") or self.mountpoint.startswith("/media/autofs"):
            return self.description
        return self.description + "\t" + self.mountpoint

    def mounted(self, mounts=None):
        if self.force_mounted:
            return True
        else:
            if self.mountpoint:
                if mounts is None:
                    mounts = getProcMounts()
                for parts in mounts:
                    if (
                        parts
                        and len(parts) > 1
                        and self.mountpoint.startswith(parts[1])
                    ):
                        return True
            return False

    def filesystem(self, mounts=None):
        if self.mountpoint:
            if mounts is None:
                mounts = getProcMounts()
            for fields in mounts:
                if len(fields) < 3:
                    continue
                if self.mountpoint.endswith(
                        "/") and not self.mountpoint == "/":
                    if fields[1] + "/" == self.mountpoint:
                        return fields[2]
                elif fields[1] == self.mountpoint:
                    return fields[2]
        return ""


def addInstallTask(job, package):
    task = Task.LoggingTask(job, "update packages")
    task.setTool("opkg")
    task.args.append("update")
    task = Task.LoggingTask(job, "Install " + package)
    task.setTool("opkg")
    task.args.append("install")
    task.args.append(package)


class HarddiskManager:

    def __init__(self):
        self.hdd = []
        self.cd = ""
        self.partitions = []
        self.devices_scanned_on_init = []
        self.on_partition_list_change = CList()
        try:
            self.enumerateBlockDevices()
        except Exception as ex:
            print("[HarddiskManager] enumerateBlockDevices failed:", ex)
        p = (
            ("/media/hdd", _("Hard disk")),
            ("/media/card", _("Card")),
            ("/media/cf", _("Compact flash")),
            ("/media/mmc1", _("MMC card")),
            ("/media/net", _("Network mount")),
            ("/media/net1", _("Network mount %s") % "1"),
            ("/media/net2", _("Network mount %s") % "2"),
            ("/media/net3", _("Network mount %s") % "3"),
            ("/media/ram", _("Ram disk")),
            ("/media/usb", _("USB stick")),
            ("/media/usb1", _("USB1 stick")),
            ("/media/usb2", _("USB2 stick")),
            ("/", _("Internal flash")),
        )
        known = set([os.path.normpath(a.mountpoint)
                     for a in self.partitions if a.mountpoint])
        for m, d in p:
            if m not in known and os.path.ismount(m):
                self.partitions.append(Partition(mountpoint=m, description=d))

    def getBlockDevInfo(self, blockdev):
        HasMMC = False
        try:
            if fileExists("/proc/cmdline"):
                with open(
                    "/proc/cmdline", "r", encoding="utf-8", errors="ignore"
                ) as fh:
                    HasMMC = "root=/dev/mmcblk" in fh.read()
        except Exception:
            HasMMC = False

        devpath = "/sys/block/" + blockdev
        error = False
        removable = False
        blacklisted = False
        is_cdrom = False
        partitions = []
        try:
            if os.path.exists(devpath + "/removable"):
                removable = bool(int(readFile(devpath + "/removable") or 0))
            if os.path.exists(devpath + "/dev"):
                dev_raw = readFile(devpath + "/dev")
                try:
                    dev = int(dev_raw.split(":")[0])
                except Exception:
                    dev = None
            else:
                dev = None
            blacklist_list = [1, 7, 31, 253, 254]
            if HasMMC:
                blacklist_list.append(179)
            blacklisted = dev in blacklist_list if dev is not None else False
            if blockdev.startswith("sr"):
                is_cdrom = True
            if blockdev.startswith("hd"):
                try:
                    media = readFile("/proc/ide/%s/media" % blockdev)
                    if "cdrom" in media:
                        is_cdrom = True
                except IOError:
                    error = True

            if not is_cdrom and os.path.exists(devpath):
                for partition in os.listdir(devpath):
                    if not partition.startswith(blockdev):
                        continue
                    partitions.append(partition)
            else:
                self.cd = blockdev
        except IOError:
            error = True

        medium_found = True
        try:
            open("/dev/" + blockdev).close()
        except IOError as err:
            try:
                if hasattr(err, "errno") and err.errno == 159:
                    medium_found = False
            except Exception:
                medium_found = True

        return (
            error,
            blacklisted,
            removable,
            is_cdrom,
            partitions,
            medium_found)

    def enumerateBlockDevices(self):
        print("[Harddisk] enumerating block devices...")
        if not os.path.exists("/sys/block"):
            return
        for blockdev in os.listdir("/sys/block"):
            try:
                error, blacklisted, removable, is_cdrom, partitions, medium_found = (
                    self.addHotplugPartition(blockdev))
                if not error and not blacklisted and medium_found:
                    for part in partitions:
                        self.addHotplugPartition(part)
                    self.devices_scanned_on_init.append(
                        (blockdev, removable, is_cdrom, medium_found)
                    )
            except Exception as ex:
                print(
                    "[Harddisk] enumerateBlockDevices error for",
                    blockdev,
                    ex)

    def getAutofsMountpoint(self, device):
        r = self.getMountpoint(device)
        if r is None:
            return "/media/" + device
        else:
            return r

    def getMountpoint(self, device):
        dev = "/dev/%s" % device
        for item in getProcMounts():
            if item and item[0] == dev:
                return item[1]
        return None

    def addHotplugPartition(self, device, physdev=None):
        if not physdev:
            dev, part = self.splitDeviceName(device)
            try:
                raw = os.path.realpath("/sys/block/" + dev + "/device")
                physdev = raw[4:] if len(raw) > 4 else raw
            except OSError:
                physdev = dev
                print("couldn't determine blockdev physdev for device", device)

        error, blacklisted, removable, is_cdrom, partitions, medium_found = (
            self.getBlockDevInfo(device)
        )
        if not blacklisted and medium_found:
            description = self.getUserfriendlyDeviceName(device, physdev)
            p = Partition(
                mountpoint=self.getMountpoint(device),
                description=description,
                force_mounted=True,
                device=device,
            )
            self.partitions.append(p)
            if p.mountpoint:
                self.on_partition_list_change("add", p)
            l = len(device)
            if l and (not device[l - 1].isdigit() or device == "mmcblk0"):
                try:
                    self.hdd.append(Harddisk(device, removable))
                    self.hdd.sort()
                    SystemInfo["Harddisk"] = True
                except Exception as ex:
                    print("[HarddiskManager] adding Harddisk failed:", ex)
        return (
            error,
            blacklisted,
            removable,
            is_cdrom,
            partitions,
            medium_found)

    def addHotplugAudiocd(self, device, physdev=None):
        if not physdev:
            dev, part = self.splitDeviceName(device)
            try:
                raw = os.path.realpath("/sys/block/" + dev + "/device")
                physdev = raw[4:] if len(raw) > 4 else raw
            except OSError:
                physdev = dev
                print("couldn't determine blockdev physdev for device", device)

        error, blacklisted, removable, is_cdrom, partitions, medium_found = (
            self.getBlockDevInfo(device)
        )
        if not blacklisted and medium_found:
            description = self.getUserfriendlyDeviceName(device, physdev)
            p = Partition(
                mountpoint="/media/audiocd",
                description=description,
                force_mounted=True,
                device=device,
            )
            self.partitions.append(p)
            self.on_partition_list_change("add", p)
            SystemInfo["Harddisk"] = False
        return (
            error,
            blacklisted,
            removable,
            is_cdrom,
            partitions,
            medium_found)

    def removeHotplugPartition(self, device):
        for x in self.partitions[:]:
            if x.device == device:
                self.partitions.remove(x)
                if x.mountpoint:
                    self.on_partition_list_change("remove", x)

        l = len(device)
        if l and not device[l - 1].isdigit():
            for hdd in self.hdd[:]:
                if hdd.device == device:
                    try:
                        hdd.stop()
                    except Exception:
                        pass
                    try:
                        self.hdd.remove(hdd)
                    except ValueError:
                        pass
                    break
            SystemInfo["Harddisk"] = len(self.hdd) > 0

    def HDDCount(self):
        return len(self.hdd)

    def HDDList(self):
        ret = []
        for hd in self.hdd:
            hddname = hd.model() + " - " + hd.bus()
            cap = hd.capacity()
            if cap != "":
                hddname += " (" + cap + ")"
            ret.append((hddname, hd))
        return ret

    def getCD(self):
        return self.cd

    def getMountedPartitions(self, onlyhotplug=False, mounts=None):
        if mounts is None:
            mounts = getProcMounts()
        parts = [
            x
            for x in self.partitions
            if (x.is_hotplug or not onlyhotplug) and x.mounted(mounts)
        ]
        devs = set([x.device for x in parts])
        for devname in list(devs):
            if not devname:
                continue
            dev, part = self.splitDeviceName(devname)
            if part and dev in devs:
                devs.discard(dev)
        return [x for x in parts if not x.device or x.device in devs]

    def splitDeviceName(self, devname):
        if len(devname) >= 3:
            dev = devname[:3]
            part = devname[3:]
        else:
            dev = devname
            part = ""
        for p in part:
            if not p.isdigit():
                return (devname, 0)
        return (dev, int(part) if part else 0)

    def getUserfriendlyDeviceName(self, dev, phys):
        dev, part = self.splitDeviceName(dev)
        description = _("External Storage %s") % dev
        try:
            description = readFile("/sys" + phys + "/model") or description
        except IOError as s:
            print("couldn't read model:", s)

        if part and part != 1:
            description += _(" (Partition %d)") % part
        return description

    def addMountedPartition(self, device, desc):
        for x in self.partitions:
            if x.mountpoint == device:
                return
        self.partitions.append(Partition(mountpoint=device, description=desc))

    def removeMountedPartition(self, mountpoint):
        for x in self.partitions[:]:
            if x.mountpoint == mountpoint:
                self.partitions.remove(x)
                self.on_partition_list_change("remove", x)

    def setDVDSpeed(self, device, speed=0):
        ioctl_flag = int(21282)
        if not device.startswith("/"):
            device = "/dev/" + device
        try:
            from fcntl import ioctl

            with open(device, "rb") as cd:
                ioctl(cd.fileno(), ioctl_flag, speed)
        except Exception as ex:
            print(
                "[Harddisk] Failed to set %s speed to %s" %
                (device, speed), ex)


class UnmountTask(Task.LoggingTask):

    def __init__(self, job, hdd):
        Task.LoggingTask.__init__(self, job, _("Unmount"))
        self.hdd = hdd
        self.mountpoints = []

    def prepare(self):
        try:
            dev = self.hdd.disk_path.split("/")[-1]
            with open(
                "/dev/nomount.%s" % dev, "w", encoding="utf-8", errors="ignore"
            ) as f:
                f.write("")
        except Exception as e:
            print("ERROR: Failed to create /dev/nomount file:", e)

        self.setTool("umount")
        self.args.append("-f")
        for dev in self.hdd.enumMountDevices():
            self.args.append(dev)
            try:
                self.postconditions.append(Task.ReturncodePostcondition())
            except Exception:
                pass
            self.mountpoints.append(dev)

        if not self.mountpoints:
            print("UnmountTask: No mountpoints found?")
            self.cmd = "true"
            self.args = [self.cmd]

    def afterRun(self):
        for path in self.mountpoints:
            try:
                os.rmdir(path)
            except Exception as ex:
                print(("Failed to remove path '%s':" % path, ex))


class MountTask(Task.LoggingTask):

    def __init__(self, job, hdd):
        Task.LoggingTask.__init__(self, job, _("Mount"))
        self.hdd = hdd

    def prepare(self):
        try:
            dev = self.hdd.disk_path.split("/")[-1]
            try:
                os.unlink("/dev/nomount.%s" % dev)
            except Exception:
                pass
        except Exception as e:
            print("ERROR: Failed to remove /dev/nomount file:", e)

        if self.hdd.mount_device is None:
            dev = self.hdd.partitionPath("1")
        else:
            dev = self.hdd.mount_device
        try:
            with open("/etc/fstab", "r", encoding="utf-8", errors="ignore") as fstab:
                lines = fstab.readlines()
        except Exception:
            lines = []

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            fspath = os.path.realpath(parts[0])
            if os.path.realpath(fspath) == dev:
                self.setCmdline("mount -t auto " + fspath)
                try:
                    self.postconditions.append(Task.ReturncodePostcondition())
                except Exception:
                    pass
                return

        if self.hdd.type == DEVTYPE_UDEV:
            self.setCmdline("sleep 2; hdparm -z " + self.hdd.disk_path)
            try:
                self.postconditions.append(Task.ReturncodePostcondition())
            except Exception:
                pass
        return


class MkfsTask(Task.LoggingTask):

    def prepare(self):
        self.fsck_state = None
        return

    def processOutput(self, data):
        print("[Mkfs]", data)
        if "Writing inode tables:" in data:
            self.fsck_state = "inode"
        elif "Creating journal" in data:
            self.fsck_state = "journal"
            try:
                self.setProgress(80)
            except Exception:
                pass
        elif "Writing superblocks " in data:
            try:
                self.setProgress(95)
            except Exception:
                pass
        elif self.fsck_state == "inode":
            if "/" in data:
                try:
                    d = data.strip(" \x08\r\n").split("/", 1)
                    if len(d) > 1:
                        left = d[0].strip()
                        right = d[1].split("\x08", 1)[0].strip()
                        try:
                            prog = 80 * (int(left) / int(right))
                            self.setProgress(prog)
                        except Exception:
                            pass
                except Exception as e:
                    print("[Mkfs] E:", e)
                return
        try:
            self.log.append(data)
        except Exception:
            pass


class HarddiskSetup(Screen):

    def __init__(self, session, hdd, action, text, question):
        Screen.__init__(self, session)
        self.action = action
        self.question = question
        self.hdd = hdd
        self.setTitle(_("Setup hard disk"))
        self["model"] = Label(_("Model: ") + hdd.model())
        self["capacity"] = Label(_("Capacity: ") + hdd.capacity())
        self["bus"] = Label(_("Bus: ") + hdd.bus())
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(text)
        self["actions"] = ActionMap(
            ["OkCancelActions"], {"ok": self.hddQuestion, "cancel": self.close}
        )
        self["shortcuts"] = ActionMap(
            ["ShortcutActions"], {"red": self.close, "green": self.hddQuestion}
        )

    def hddQuestion(self):
        message = (
            self.question
            + "\n"
            + _("You can continue watching TV etc. while this is running.")
        )
        self.session.openWithCallback(self.hddConfirmed, MessageBox, message)

    def hddConfirmed(self, confirmed):
        if not confirmed:
            return
        try:
            from .Task import job_manager
        except Exception:
            from Components.Task import job_manager
        try:
            job = self.action()
            job_manager.AddJob(job, onSuccess=job_manager.popupTaskView)
            from Screens.TaskView import JobView

            self.session.open(JobView, job, afterEventChangeable=False)
        except Exception as ex:
            self.session.open(
                MessageBox, str(ex), type=MessageBox.TYPE_ERROR, timeout=10
            )
        self.close()


class HarddiskSelection(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.setTitle(_("Select hard disk"))
        self.skinName = "HarddiskSelection"
        if harddiskmanager.HDDCount() == 0:
            tlist = []
            tlist.append((_("no storage devices found"), 0))
            self["hddlist"] = MenuList(tlist)
        else:
            self["hddlist"] = MenuList(harddiskmanager.HDDList())
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Select"))
        self["actions"] = ActionMap(
            ["OkCancelActions"], {
                "ok": self.okbuttonClick, "cancel": self.close})
        self["shortcuts"] = ActionMap(
            ["ShortcutActions"], {
                "red": self.close, "green": self.okbuttonClick})

    def doIt(self, selection):
        self.session.openWithCallback(
            self.close,
            HarddiskSetup,
            selection,
            action=selection.createInitializeJob,
            text=_("Initialize"),
            question=_(
                "Do you really want to initialize the device?\nAll data on the disk will be lost!"
            ),
        )

    def okbuttonClick(self):
        selection = self["hddlist"].getCurrent()
        if selection and selection[1] != 0:
            self.doIt(selection[1])


class HarddiskFsckSelection(HarddiskSelection):

    def doIt(self, selection):
        self.session.openWithCallback(
            self.close,
            HarddiskSetup,
            selection,
            action=selection.createCheckJob,
            text=_("Check"),
            question=_(
                "Do you really want to check the filesystem?\nThis could take lots of time!"
            ),
        )


def isSleepStateDevice(device):
    """
    Uses hdparm -C <device> and interprets output.
    Returns True for sleeping, False for active, None for unknown/error.
    """
    try:
        res = subprocess.run(
            ["hdparm", "-C", device], capture_output=True, text=True, timeout=5
        )
        ret = res.stdout + res.stderr
    except Exception:
        try:
            ret = os.popen("hdparm -C %s" % device).read()
        except Exception:
            return None

    if "SG_IO" in ret or "HDIO_DRIVE_CMD" in ret:
        return None
    if "drive state is:  standby" in ret or "drive state is:  idle" in ret:
        return True
    if "drive state is:  active/idle" in ret or "drive state is: active/idle" in ret:
        return False
    return None


def internalHDDNotSleeping(external=False):
    state = False
    if harddiskmanager.HDDCount():
        for hdd in harddiskmanager.HDDList():
            try:
                hdobj = hdd[1]
                if hdobj.internal or external:
                    if (
                        hdobj.idle_running
                        and hdobj.max_idle_time
                        and not hdobj.isSleeping()
                    ):
                        state = True
            except Exception:
                continue
    return state


try:
    harddiskmanager = HarddiskManager()
except Exception as ex:
    print("[Harddisk] HarddiskManager initialization failed:", ex)
    harddiskmanager = None

try:
    SystemInfo["ext4"] = isFileSystemSupported(
        "ext4") or isFileSystemSupported("ext3")
except Exception:
    try:
        SystemInfo["ext4"] = False
    except Exception:
        pass

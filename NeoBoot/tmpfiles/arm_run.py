from Plugins.Extensions.NeoBoot.__init__ import _
from Plugins.Extensions.NeoBoot.files.stbbranding import (
    getSupportedTuners,
    getCPUtype,
    getCPUSoC,
    getImageNeoBoot,
    getBoxHostName,
    getNeoLocation,
    getMountPointNeo2,
)
from enigma import getDesktop
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from Components.Sources.List import List
from Components.ActionMap import ActionMap
from Components.GUIComponent import *
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.config import *
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists
import os
import subprocess


def run_shell_command(cmd):
    """
    Modern replacement for os.system(cmd) using subprocess.run.
    Returns the exit code, mimicking os.system's behavior.
    """
    try:
        result = subprocess.run(cmd, shell=True, check=False)
        return result.returncode
    except Exception as e:
        print(f"[run_shell_command] Failed to run '{cmd}'. Error: {e}")
        return -1  # Return a non-zero code to indicate failure


def _is_device_mounted(
        device="/dev/mmcblk0p23",
        mount_point="/media/InternalFlash"):
    """
    Checks if the specified device is currently mounted on the given mount point.
    """
    try:
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.split()
                if len(
                        parts) >= 2 and parts[0] == device and parts[1] == mount_point:
                    return True
        return False
    except FileNotFoundError:
        return False


def _append_fstab_entry(device, mount_point, fstab_file="/etc/fstab"):
    """
    Appends the required fstab line if it's not already present.
    """
    FSTAB_LINE = f"{device}\t\t{mount_point}\t\tauto\t\tdefaults\t\t\t\t\t\t0\t0\n"
    try:
        with open(fstab_file, "r") as f:
            if any(line.strip().startswith(device) for line in f):
                print(
                    f"Fstab entry for {device} already exists or device is in use.")
                return False
    except OSError as e:
        print(f"Error reading {fstab_file}: {e}")
        return False
    try:
        with open(fstab_file, "a") as f:
            f.write(FSTAB_LINE)
        return True
    except OSError as e:
        print(f"Error writing to {fstab_file}. Check permissions. Error: {e}")
        return False


LinkNeoBoot = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot"


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
        self["list"] = List(self.list)
        self.select()
        self["actions"] = ActionMap(["WizardActions", "ColorActions"], {
            "ok": self.KeyOk, "back": self.close})
        self["label1"] = Label(_("Start the chosen system now ?"))
        self["label2"] = Label(_("Select OK to run the image."))

    def select(self):
        self.list = []
        mypath = "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot"
        if not fileExists(mypath + "icons"):
            mypixmap = (
                "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png"
            )
        png = LoadPixmap(mypixmap)
        res = (_("OK Start image..."), png, 0)
        self.list.append(res)
        self["list"].list = self.list

    def KeyOk(self):
        image = getImageNeoBoot()
        neo_location = getNeoLocation()
        cmd = f"rm -rf {neo_location}ImageBoot/{image}/usr/bin/enigma2_pre_start.sh"
        run_shell_command(cmd)

        self.StartImageInNeoBoot()
        getMountPointNeo2()
        run_shell_command("touch /tmp/.init_reboot")

    def novalerReboot(self, result):
        """Callback to reboot after the fstab edit message."""
        self.session.open(TryQuitMainloop, 2)

    def StartImageInNeoBoot(self):
        DEVICE = "/dev/mmcblk0p23"
        MOUNT_POINT = "/media/InternalFlash"

        if getBoxHostName() == "novaler4kpro":
            if not _is_device_mounted(DEVICE, MOUNT_POINT):
                print(
                    f"Novaler4kpro: {DEVICE} not mounted on {MOUNT_POINT}. Checking fstab...")
                if not os.path.isdir(MOUNT_POINT):
                    try:
                        os.mkdir(MOUNT_POINT)
                        print(f"Created mount point {MOUNT_POINT}")
                    except OSError as e:
                        print(f"Error creating mount point: {e}")

                if _append_fstab_entry(DEVICE, MOUNT_POINT):
                    print("fstab file edited. rebooting your novaler4kpro")
                    self.session.open(
                        MessageBox,
                        _("fstab file edited. rebooting your novaler4kpro"),
                        MessageBox.TYPE_INFO,
                        5,  # <--- TIMEOUT PASSED POSITIONALLY
                        self.novalerReboot,
                    )
                    return  # Exit the function after scheduling the reboot
                else:
                    print(
                        "Novaler4kpro: fstab entry already present or write failed. Proceeding."
                    )

        if getImageNeoBoot() != "Flash":
            if fileExists(
                "%sImageBoot/%s/.control_ok" %
                    (getNeoLocation(), getImageNeoBoot())):
                run_shell_command("touch /tmp/.control_ok ")
            else:
                run_shell_command(
                    "touch %sImageBoot/%s/.control_boot_new_image "
                    % (getNeoLocation(), getImageNeoBoot())
                )

        if fileExists("/.multinfo") and getCPUtype() == "ARMv7":
            run_shell_command(
                f"{LinkNeoBoot}/files/findsk.sh; mkdir -p /media/InternalFlash; mount /tmp/root /media/InternalFlash; sleep 1")

        self.sel = self["list"].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            if not fileExists("/bin/busybox.nosuid"):
                run_shell_command('ln -sf "busybox" "/bin/busybox.nosuid" ')
            if fileExists("/media/InternalFlash/etc/init.d/neomountboot.sh"):
                run_shell_command(
                    "rm -f /media/InternalFlash/etc/init.d/neomountboot.sh;"
                )
            if fileExists(
                "/media/InternalFlash/linuxrootfs1/etc/init.d/neomountboot.sh"
            ):
                run_shell_command(
                    "rm -f /media/InternalFlash/linuxrootfs1/etc/init.d/neomountboot.sh;"
                )
            if fileExists(
                "/media/InternalFlash/linuxrootfs2/etc/init.d/neomountboot.sh"
            ):
                run_shell_command(
                    "rm -f /media/InternalFlash/linuxrootfs2/etc/init.d/neomountboot.sh;"
                )
            if fileExists(
                "/media/InternalFlash/linuxrootfs3/etc/init.d/neomountboot.sh"
            ):
                run_shell_command(
                    "rm -f /media/InternalFlash/linuxrootfs3/etc/init.d/neomountboot.sh;"
                )
            if fileExists(
                "/media/InternalFlash/linuxrootfs4/etc/init.d/neomountboot.sh"
            ):
                run_shell_command(
                    "rm -f /media/InternalFlash/linuxrootfs4/etc/init.d/neomountboot.sh;"
                )

            if getSupportedTuners():
                if getImageNeoBoot() == "Flash":
                    if fileExists("/.multinfo"):
                        if fileExists(
                            "/media/InternalFlash/linuxrootfs1/sbin/neoinitarm"
                        ):
                            run_shell_command(
                                'ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs1/sbin/init"'
                            )
                        if fileExists(
                            "/media/InternalFlash/linuxrootfs2/sbin/neoinitarm"
                        ):
                            run_shell_command(
                                'ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs2/sbin/init"'
                            )
                        if fileExists(
                            "/media/InternalFlash/linuxrootfs3/sbin/neoinitarm"
                        ):
                            run_shell_command(
                                'ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs3/sbin/init"'
                            )
                        if fileExists(
                            "/media/InternalFlash/linuxrootfs4/sbin/neoinitarm"
                        ):
                            run_shell_command(
                                'ln -sf "init.sysvinit" "/media/InternalFlash/linuxrootfs4/sbin/init"'
                            )
                        if fileExists("/media/InternalFlash/sbin/init"):
                            run_shell_command(
                                'ln -sfn "init.sysvinit" "/media/InternalFlash/sbin/init"'
                            )

                        self.session.open(TryQuitMainloop, 2)

                    else:
                        cmd = "ln -sfn /sbin/init.sysvinit /sbin/init"
                        run_shell_command(cmd)  # Removed unused 'rc'
                        self.session.open(TryQuitMainloop, 2)

                elif getImageNeoBoot() != "Flash":
                    if fileExists("/.multinfo"):
                        if fileExists(
                            "/media/InternalFlash/linuxrootfs1/sbin/neoinitarm"
                        ):
                            cmd = "cd /media/InternalFlash/linuxrootfs1; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs1/sbin/init"
                            run_shell_command(cmd)  # Removed unused 'rc'
                            self.session.open(TryQuitMainloop, 2)
                        elif fileExists(
                            "/media/InternalFlash/linuxrootfs2/sbin/neoinitarm"
                        ):
                            cmd = "cd /media/InternalFlash/linuxrootfs2; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs2/sbin/init"
                            run_shell_command(cmd)  # Removed unused 'rc'
                            self.session.open(TryQuitMainloop, 2)
                        elif fileExists(
                            "/media/InternalFlash/linuxrootfs3/sbin/neoinitarm"
                        ):
                            cmd = "cd /media/InternalFlash/linuxrootfs3; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs3/sbin/init"
                            run_shell_command(cmd)  # Removed unused 'rc'
                            self.session.open(TryQuitMainloop, 2)
                        elif fileExists(
                            "/media/InternalFlash/linuxrootfs4/sbin/neoinitarm"
                        ):
                            cmd = "cd /media/InternalFlash/linuxrootfs4; ln -sfn /sbin/neoinitarm /media/InternalFlash/linuxrootfs4/sbin/init"
                            run_shell_command(cmd)  # Removed unused 'rc'
                            self.session.open(TryQuitMainloop, 2)
                        else:
                            self.session.open(TryQuitMainloop, 2)

                    elif not fileExists("/.multinfo"):
                        cmd = "ln -sfn /sbin/neoinitarm /sbin/init"
                        run_shell_command(cmd)  # Removed unused 'rc'
                        self.session.open(TryQuitMainloop, 2)
                    else:
                        cmd = "ln -sfn /sbin/init.sysvinit /sbin/init"
                        run_shell_command(cmd)  # Removed unused 'rc'
                        self.session.open(TryQuitMainloop, 2)
                else:
                    run_shell_command(
                        'echo "Flash "  >> '
                        + getNeoLocation()
                        + "ImageBoot/.neonextboot"
                    )
                    self.messagebox = self.session.open(
                        MessageBox,
                        _("It looks like it that multiboot does not support this STB."),
                        MessageBox.TYPE_INFO,
                        8,
                    )
                    self.close()
            else:
                run_shell_command(
                    'echo "Flash "  >> ' +
                    getNeoLocation() +
                    "ImageBoot/.neonextboot")
                self.messagebox = self.session.open(
                    MessageBox,
                    _("It looks like it that multiboot does not support this STB."),
                    MessageBox.TYPE_INFO,
                    8,
                )
                self.close()

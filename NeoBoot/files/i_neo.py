try:
    from boxbranding import getBoxType, getImageType, getImageDistro, getImageVersion, getImageBuild, getImageDevBuild, getImageFolder, getImageFileSystem, getBrandOEM, getMachineBrand, getMachineName, getMachineBuild, getMachineMake, getMachineMtdRoot, getMachineRootFile, getMachineMtdKernel, getMachineKernelFile, getMachineMKUBIFS, getMachineUBINIZE
    import Tools.CopyFiles
    from Tools.Multiboot import getImagelist, getCurrentImage, getCurrentImageMode, deleteImage, restoreImages
    from Tools.Multiboot import GetImagelist
    from Tools.Notifications import AddPopupWithCallback
except:
        pass
        
from os import path, stat, system, mkdir, makedirs, listdir, remove, rename, rmdir, sep as ossep, statvfs, chmod, walk, symlink, unlink
from shutil import copy, copyfile, move, rmtree
from time import localtime, time, strftime, mktime

from . import _, PluginLanguageDomain
from Components.Button import Button
from Components.Harddisk import harddiskmanager, getProcMounts
from Components.MenuList import MenuList
import Components.Task
from Screens.Standby import TryQuitMainloop
from Screens.Setup import Setup
from Screens.TaskView import JobView
from Screens.TextBox import TextBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Sources.StaticText import StaticText
from Components.ChoiceList import ChoiceList, ChoiceEntryComponent
from Components.config import config, ConfigSubsection, ConfigYesNo, ConfigSelection, ConfigText, ConfigNumber, NoSave, ConfigClock, configfile
from Components.ActionMap import ActionMap
from Components.Console import Console
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from Components.SystemInfo import BoxInfo, SystemInfo
from Tools.BoundFunction import boundFunction
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, fileExists, pathExists, fileHas
from Tools.Downloader import downloadWithProgress
import os
import re
from urllib.request import urlopen, Request
from urllib.parse import urlparse
import xml.etree.ElementTree
import json
import time
import zipfile
import shutil
import tempfile
import struct

from enigma import eEPGCache, eEnv, eTimer, fbClass

try:
    from Tools.HardwareInfo import HardwareInfo
except:
    from Plugins.Extensions.NeoBoot.files import HardwareInfo    
try:
    from Screens.Standby import getReasons 
except:
    pass
    

def getMountChoices():
	choices = []
	for p in harddiskmanager.getMountedPartitions():
		if path.exists(p.mountpoint):
			d = path.normpath(p.mountpoint)
			entry = (p.mountpoint, d)
			if p.mountpoint != "/" and entry not in choices:
				choices.append(entry)
	choices.sort()
	return choices


def getMountDefault(choices):
	if fileExists("/media/usb/ImagesUpload/"):
	        choices = {x[1]: x[0] for x in choices}
	        default = choices.get("/media/usb") or choices.get("/media/hdd")
	        return default
	else:
	        choices = {x[1]: x[0] for x in choices}
	        default = choices.get("/media/hdd") or choices.get("/media/usb")
	        return default

def __onPartitionChange(*args, **kwargs):
	global choices
	choices = getMountChoices()
	config.imagemanager.backuplocation.setChoices(choices=choices, default=getMountDefault(choices))

try:
        defaultprefix = getImageDistro()
        config.imagemanager = ConfigSubsection()
        config.imagemanager.autosettingsbackup = ConfigYesNo(default=True)
        choices = getMountChoices()
        config.imagemanager.backuplocation = ConfigSelection(choices=choices, default=getMountDefault(choices))
        config.imagemanager.extensive_location_search = ConfigYesNo(default=True)
        harddiskmanager.on_partition_list_change.append(__onPartitionChange) # to update backuplocation choices on mountpoint change
        config.imagemanager.backupretry = ConfigNumber(default=30)
        config.imagemanager.backupretrycount = NoSave(ConfigNumber(default=0))
        config.imagemanager.folderprefix = ConfigText(default=defaultprefix, fixed_size=False)
        config.imagemanager.nextscheduletime = NoSave(ConfigNumber(default=0))
        config.imagemanager.repeattype = ConfigSelection(default="daily", choices=[("daily", _("Daily")), ("weekly", _("Weekly")), ("monthly", _("30 Days"))])
        config.imagemanager.schedule = ConfigYesNo(default=False)
        config.imagemanager.scheduletime = ConfigClock(default=0)  # 1:00
        config.imagemanager.query = ConfigYesNo(default=True)
        config.imagemanager.lastbackup = ConfigNumber(default=0)
        config.imagemanager.number_to_keep = ConfigNumber(default=0)
        # Add a method for users to download images directly from their own build servers.
        # Script must be able to handle urls in the form http://domain/scriptname/boxname.
        # Format of the JSON output from the script must be the same as the official urls above.
        # The option will only show once a url has been added.
        config.imagemanager.imagefeed_MyBuild = ConfigText(default="", fixed_size=False)
        config.imagemanager.login_as_ViX_developer = ConfigYesNo(default=False)
        config.imagemanager.developer_username = ConfigText(default="username", fixed_size=False)
        config.imagemanager.developer_password = ConfigText(default="password", fixed_size=False)

except :
                pass 

DISTRO = 0
URL = 1
ACTION = 2

FEED_URLS = [
	("OpenViX", "https://www.openvix.co.uk/json/%s", "getMachineMake"),
	("OpenATV", "https://images.mynonpublic.com/openatv/json/%s", "getMachineMake"),
	("OpenBH", "https://images.openbh.net/json/%s", "getMachineMake"),
	("OpenPLi", "http://downloads.openpli.org/json/%s", "HardwareInfo"),
]


class tmp:
	dir = None


def checkimagefiles(files):
	return len([x for x in files if 'kernel' in x and '.bin' in x or x in ('uImage', 'rootfs.bin', 'root_cfe_auto.bin', 'root_cfe_auto.jffs2', 'oe_rootfs.bin', 'e2jffs2.img', 'rootfs.tar.bz2', 'rootfs.ubi')]) == 2


############################other image###############################################

class ImageManager(Screen):
	skin = """<screen name="ImageManager" position="center,center" size="663,195">
		<widget name="key_green" position="215,2" zPosition="1" size="195,50" font="Regular;15" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget name="lab1" position="0,65" size="663,130" font="Regular; 20" zPosition="2" transparent="0" halign="center" />
	</screen>"""
		
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("NeoBoot image download"))
		self["lab1"] = Label()
		self["key_green"] = Button(_("Downloads"))
		self["infoactions"] = ActionMap(["SetupActions"], {
			"info": self.showInfo,
		}, -1)
		self["defaultactions"] = ActionMap(["OkCancelActions"], {
			"cancel": self.close,
		}, -1)
		self["mainactions"] = ActionMap(["ColorActions", "OkCancelActions", "DirectionActions", "KeyboardInputActions"], {
			"green": self.doDownload,
			"ok": self.doDownload,
			"up": self.refreshUp,
			"down": self.refreshDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"upRepeated": self.refreshUp,
			"downRepeated": self.refreshDown,
			"leftRepeated": self.keyLeft,
			"rightRepeated": self.keyRight,
		}, -1)
		self["mainactions"].setEnabled(False)
		self.BackupRunning = False
		self.mountAvailable = False
		self.BackupDirectory = " "
		if SystemInfo["canMultiBoot"]:
			self.mtdboot = SystemInfo["MBbootdevice"]
		self.onChangedEntry = []
		if choices:
			self["list"] = MenuList(list=[((_("No images found on the selected download server...if password check validity")), "Waiter")])

		else:
			self["list"] = MenuList(list=[((_(" Press 'Menu' to select a storage device - none available")), "Waiter")])
			self["key_red"].hide()
			self["key_green"].hide()
			self["key_yellow"].hide()
			self["key_blue"].hide()
		self.populate_List()
		self.activityTimer = eTimer()
		self.activityTimer.startLongTimer(10)
		self.Console = Console()
		self.ConsoleB = Console(binary=True)

		if self.selectionChanged not in self["list"].onSelectionChanged:
			self["list"].onSelectionChanged.append(self.selectionChanged)

	def selectionChanged(self):
		# Where is this used? self.onChangedEntry does not appear to be populated anywhere. Maybe dead code.
		item = self["list"].getCurrent() # (name, link)
		if item:
			name = item[1]
		else:
			name = ""
		for cb in self.onChangedEntry:
			cb(name, desc)

	def refreshUp(self):
		self["list"].moveUp()

	def refreshDown(self):
		self["list"].moveDown()

	def keyLeft(self):
		self["list"].pageUp()
		self.selectionChanged()

	def keyRight(self):
		self["list"].pageDown()
		self.selectionChanged()

	def refreshList(self):
		if self.BackupDirectory == " ":
			return
		imglist = []
		imagesDownloadedList = self.getImagesDownloaded()
		for image in imagesDownloadedList:
			imglist.append((image["name"], image["link"]))
		if imglist:
			self["key_green"].show()
		else:
			self["key_green"].hide()
			
		self["list"].setList(imglist)
		self["list"].show()
		self.selectionChanged()

	def getJobName(self, job):
		return "%s: %s (%d%%)" % (job.getStatustext(), job.name, int(100 * job.progress / float(job.end)))

	def showJobView(self, job):
		Components.Task.job_manager.in_background = False
		self.session.openWithCallback(self.JobViewCB, JobView, job, cancelable=False, backgroundable=True, afterEventChangeable=False, afterEvent="close")

	def JobViewCB(self, in_background):
		Components.Task.job_manager.in_background = in_background

	def populate_List(self):
		if config.imagemanager.backuplocation.value.endswith("/"):
			mount = config.imagemanager.backuplocation.value, config.imagemanager.backuplocation.value[:-1]
		else:
			mount = config.imagemanager.backuplocation.value + "/", config.imagemanager.backuplocation.value
			
		if fileExists("/media/usb/ImagesUpload/"):
                        hdd = '/media/usb/', '/media/usb/'
		else:
                        hdd = '/media/hdd/', '/media/hdd/'
	                
		if mount not in config.imagemanager.backuplocation.choices.choices and hdd not in config.imagemanager.backuplocation.choices.choices:
			self["mainactions"].setEnabled(False)
			self.mountAvailable = False
			self["key_green"].hide()
			self["lab1"].setText(_("Device: None available") + "\n" + _("Press 'Menu' to select a storage device"))
		else: 
			self.BackupDirectory = config.imagemanager.backuplocation.value + "ImagesUpload/"
			s = statvfs(config.imagemanager.backuplocation.value)
			free = (s.f_bsize * s.f_bavail) // (1024 * 1024)
			self["lab1"].setText(_("Device: ") + config.imagemanager.backuplocation.value + " " + _("Free space:") + " " + str(free) + _("MB") + "\n" + _("Press the OK or green button to download iamge.\nTo stop the download, press the blue button."))
			
			try:
				if not path.exists(self.BackupDirectory):
					mkdir(self.BackupDirectory, 0o755)
				self.refreshList()
			except Exception:
				self["lab1"].setText(_("Device: ") + config.imagemanager.backuplocation.value + "\n" + _("Press the green button to download image.."))
			self["mainactions"].setEnabled(True)
			self.mountAvailable = True
			

	def doDownload(self):
		choices = [(x[DISTRO], x) for x in FEED_URLS]
		if config.imagemanager.imagefeed_MyBuild.value.startswith("http"):
			choices.insert(0, ("My build", ("My build", config.imagemanager.imagefeed_MyBuild.value, "getMachineMake")))
		message = _("From which image library do you want to download?")
		self.session.openWithCallback(self.doDownloadCallback, MessageBox, message, list=choices, default=1, simple=True)

	def doDownloadCallback(self, retval): # retval will be the config element (or False, in the case of aborting the MessageBox).
		if retval:
			self.session.openWithCallback(self.refreshList, ImageManagerDownload, self.BackupDirectory, retval)


	def getImagesDownloaded(self):
		def getImages(files):
			for file in files:
				imagesFound.append({'link': file, 'name': file.split(ossep)[-1], 'mtime': stat(file).st_mtime})

		def checkMachineNameInFilename(filename):
			return model in filename or "-" + device_name + "-" in filename

		model = getMachineMake()
		try:
		    device_name = HardwareInfo().get_device_name()
		except:
                    self.close

		imagesFound = []
		if config.imagemanager.extensive_location_search.value:
			mediaList = ['/media/%s' % x for x in listdir('/media')] + (['/media/net/%s' % x for x in listdir('/media/net')] if path.isdir('/media/net') else []) + (['/media/autofs/%s' % x for x in listdir('/media/autofs')] if path.isdir('/media/autofs') else [])
		else:
			mediaList = [config.imagemanager.backuplocation.value]

		imagesFound.sort(key=lambda x: x['mtime'], reverse=True)
		# print("[ImageManager][getImagesDownloaded] imagesFound=%s" % imagesFound)
		return imagesFound


	def showInfo(self):
		self.session.open(TextBox, self.infoText(), self.title + " - " + _("info"))


class ImageManagerDownload(Screen):
	skin = """
	<screen name="ImageManager" position="center,center" size="663,195">
		<widget name="key_green" position="215,2" zPosition="1" size="195,50" font="Regular;15" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget name="lab1" position="0,65" size="663,130" font="Regular; 20" zPosition="2" transparent="0" halign="center" />
	</screen>"""


	def __init__(self, session, BackupDirectory, imagefeed):
		Screen.__init__(self, session)
		self.setTitle(_("%s downloads") % imagefeed[DISTRO])
		self.imagefeed = imagefeed
		self.BackupDirectory = BackupDirectory
		self["lab1"] = Label(_("Select an image to download for %s:") % getMachineMake())
		self["key_red"] = Button(_("Close"))
		self["key_green"] = Button(_("Download"))
		self["ImageDown"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "KeyboardInputActions", "MenuActions"], {
			"cancel": self.close,
			"red": self.close,
			"green": self.keyDownload,
			"ok": self.keyDownload,
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"upRepeated": self.keyUp,
			"downRepeated": self.keyDown,
			"leftRepeated": self.keyLeft,
			"rightRepeated": self.keyRight,
			"menu": self.close,
		}, -1)
		self.imagesList = {}
		self.setIndex = 0
		self.expanded = []
		self["list"] = ChoiceList(list=[ChoiceEntryComponent("", ((_("No images found on the selected download server...if password check validity")), "Waiter"))])
		self.getImageDistro()

	def showError(self):
		self.session.open(MessageBox, self.msg, MessageBox.TYPE_ERROR)
		self.close()

	def getImageDistro(self):
		if not path.exists(self.BackupDirectory):
			try:
				mkdir(self.BackupDirectory, 0o755)
			except Exception as err:
				self.msg = _("Error creating backup folder:\n%s: %s") % (type(err).__name__, err)
				print("[ImageManagerDownload][getImageDistro] " + self.msg)
				self.pausetimer = eTimer()
				self.pausetimer.callback.append(self.showError)
				self.pausetimer.start(50, True)
				return
		boxtype = getMachineMake()
		if self.imagefeed[ACTION] == "HardwareInfo":
			boxtype = HardwareInfo().get_device_name()
			print("[ImageManager1] boxtype:%s" % (boxtype))
			if "dm800" in boxtype:
				boxtype = getMachineMake()

		if not self.imagesList:
			# Legacy: self.imagefeed[URL] didn't contain "%s" where to insert the boxname.
			# So just tag the boxname onto the end of the url like it is a subfolder.
			# Obviously the url needs to exist.
			if "%s" not in self.imagefeed[URL] and "?" not in self.imagefeed[URL]:
				url = path.join(self.imagefeed[URL], boxtype)
			else: # New style: self.imagefeed[URL] contains "%s" and boxname is inserted there.
				url = self.imagefeed[URL] % boxtype
			
			# special case for openvix developer downloads using user/pass
			if self.imagefeed[DISTRO].lower() == "openvix" \
				and self.imagefeed[URL].startswith("https") \
				and config.imagemanager.login_as_ViX_developer.value \
				and config.imagemanager.developer_username.value \
				and config.imagemanager.developer_username.value != config.imagemanager.developer_username.default \
				and config.imagemanager.developer_password.value \
				and config.imagemanager.developer_password.value != config.imagemanager.developer_password.default:
				url = path.join(url, config.imagemanager.developer_username.value, config.imagemanager.developer_password.value)
			try:
				self.imagesList = dict(json.load(urlopen(url)))
			except Exception:
				print("[ImageManager] no images available for: the '%s' at '%s'" % (boxtype, url))
				return

		if not self.imagesList: # Nothing has been found on that server so we might as well give up.
			return

		imglist = [] # this is reset on every "ok" key press of an expandable item so it reflects the current state of expandability of that item
		for categorie in sorted(self.imagesList.keys(), reverse=True):
			if categorie in self.expanded:
				imglist.append(ChoiceEntryComponent("expanded", ((str(categorie)), "Expander")))
				for image in sorted(self.imagesList[categorie].keys(), reverse=True):
					imglist.append(ChoiceEntryComponent("verticalline", ((str(self.imagesList[categorie][image]["name"])), str(self.imagesList[categorie][image]["link"]))))
			else:
				# print("[ImageManager] [GetImageDistro] keys: %s" % list(self.imagesList[categorie].keys()))
				for image in list(self.imagesList[categorie].keys()):
					imglist.append(ChoiceEntryComponent("expandable", ((str(categorie)), "Expander")))
					break
		if imglist:
			# print("[ImageManager] [GetImageDistro] imglist: %s" % imglist)
			self["list"].setList(imglist)
			if self.setIndex:
				self["list"].moveToIndex(self.setIndex if self.setIndex < len(list) else len(list) - 1)
				if self["list"].getCurrent()[0][1] == "Expander":
					self.setIndex -= 1
					if self.setIndex:
						self["list"].moveToIndex(self.setIndex if self.setIndex < len(list) else len(list) - 1)
				self.setIndex = 0
			self.SelectionChanged()

	def SelectionChanged(self):
		currentSelected = self["list"].getCurrent()
		if currentSelected[0][1] == "Waiter":
			self["key_green"].setText("")
		else:
			if currentSelected[0][1] == "Expander":
				self["key_green"].setText(_("Compress") if currentSelected[0][0] in self.expanded else _("Expand"))
			else:
				self["key_green"].setText(_("Download"))

	def keyLeft(self):
		self["list"].pageUp()
		self.SelectionChanged()

	def keyRight(self):
		self["list"].pageDown()
		self.SelectionChanged()

	def keyUp(self):
		self["list"].moveUp()
		self.SelectionChanged()

	def keyDown(self):
		self["list"].moveDown()
		self.SelectionChanged()

	def keyDownload(self):
		currentSelected = self["list"].getCurrent()
		if currentSelected[0][1] == "Expander":
			if currentSelected[0][0] in self.expanded:
				self.expanded.remove(currentSelected[0][0])
			else:
				self.expanded.append(currentSelected[0][0])
			self.getImageDistro()

		elif currentSelected[0][1] != "Waiter":
			self.sel = currentSelected[0][0]
			if self.sel:
				message = _("Are you sure you want to download this image:\n ") + self.sel
				ybox = self.session.openWithCallback(self.doDownloadX, MessageBox, message, MessageBox.TYPE_YESNO)
				ybox.setTitle(_("Download confirmation"))
			else:
				self.close()

	def doDownloadX(self, answer):
		if answer:
			currentSelected = self["list"].getCurrent()
			selectedimage = currentSelected[0][0]
			headers, fileurl = self.processAuthLogin(currentSelected[0][1])
			fileloc = self.BackupDirectory + selectedimage
			Tools.CopyFiles.downloadFile(fileurl, fileloc, selectedimage.replace("_usb", ""), headers=headers)
			for job in Components.Task.job_manager.getPendingJobs():
				if job.name.startswith(_("Downloading")):
					break
			self.showJobView(job)
			self.close()

	def showJobView(self, job):
		Components.Task.job_manager.in_background = False
		self.session.openWithCallback(self.JobViewCB, JobView, job, cancelable=False, backgroundable=True, afterEventChangeable=False, afterEvent="close")

	def JobViewCB(self, in_background):
		Components.Task.job_manager.in_background = in_background

	def processAuthLogin(self, url):
		headers = None
		parsed = urlparse(url)
		scheme = parsed.scheme
		username = parsed.username if parsed.username else ""
		password = parsed.password if parsed.password else ""
		hostname = parsed.hostname
		port = ":%s" % parsed.port if parsed.port else ""
		query = "?%s" % parsed.query if parsed.query else ""
		if username or password:
			import base64
			base64bytes = base64.b64encode(('%s:%s' % (username, password)).encode())
			headers = {("Authorization").encode(): ("Basic %s" % base64bytes.decode()).encode()}
		return headers, scheme + "://" + hostname + port + parsed.path + query



########################____PLi image____#################################


class SelectImage(Screen):
	def __init__(self, session, *args):
		Screen.__init__(self, session)
		self.imageBrandList = {}
		self.jsonlist = {}
		self.imagesList = {}
		self.setIndex = 0
		self.expanded = []
		self.model = HardwareInfo().get_machine_name()
		self.selectedImage = ["OpenPLi", {"url": "https://downloads.openpli.org/json/%s" % self.model, "model": self.model}]
		self.models = [self.model]
		self.setTitle(_("Select image"))
		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText()
		self["key_blue"] = StaticText()
		self["description"] = Label()
		self["list"] = ChoiceList(list=[ChoiceEntryComponent('', ((_("Retrieving image list - Please wait...")), "Waiter"))])

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "KeyboardInputActions", "MenuActions"],
		{
			"ok": self.keyOk,
			"cancel": boundFunction(self.close, None),
			"red": boundFunction(self.close, None),
			"green": self.keyOk,
			"blue": self.otherImages,
			"up": self.keyUp,
			"down": self.keyDown,
			"left": self.keyLeft,
			"right": self.keyRight,
			"upRepeated": self.keyUp,
			"downRepeated": self.keyDown,
			"leftRepeated": self.keyLeft,
			"rightRepeated": self.keyRight,
			"menu": boundFunction(self.close, True),
		}, -1)

		self.callLater(self.getImagesList)

	def getImagesList(self):

		def getImages(path, files):
			for file in files:
				try:
					if checkimagefiles([x.split(os.sep)[-1] for x in zipfile.ZipFile(file).namelist()]):
						imagetyp = _("Downloaded Images")
						if 'backup' in file.split(os.sep)[-1]:
							imagetyp = _("Fullbackup Images")
						if imagetyp not in self.imagesList:
							self.imagesList[imagetyp] = {}
						self.imagesList[imagetyp][file] = {'link': file, 'name': file.split(os.sep)[-1]}
				except:
					pass

		def checkModels(file):
			for model in self.models:
				if '-%s-' % model or '-%_' % model in file:
					return True
			return False

		def conditional_sort(ls, f):
			y = iter(reversed(sorted(w for w in ls if f(w))))
			return [w if not f(w) else next(y) for w in ls]

		if not self.imageBrandList:
				url = "%s%s" % ("https://raw.githubusercontent.com/OpenPLi/FlashImage/main/", self.model)
				try:
					self.imageBrandList = json.load(urlopen(url, timeout=3))
				except:
					print("[DownloadImage] getImageBrandList Error: Unable to load json data from URL '%s'!" % url)
				if self.imageBrandList:
					self.imageBrandList.update({self.selectedImage[0]: self.selectedImage[1]})
					self.models = set([self.imageBrandList[image]['model'] for image in self.imageBrandList.keys()])
					if len(self.imageBrandList) > 1:
						self["key_blue"].setText(_("Other Images"))
		if not self.imagesList:
			if not self.jsonlist:
				try:
					self.jsonlist = dict(json.load(urlopen(self.selectedImage[1]["url"], timeout=3)))
				except:
					print("[DownloadImage] getImagesList Error: Unable to load json data from URL '%s'!" % self.selectedImage[1]["url"])
				alternative_imagefeed = config.usage.alternative_imagefeed.value
				if alternative_imagefeed:
					if "http" in alternative_imagefeed:
						url = "%s%s" % (config.usage.alternative_imagefeed.value, self.model)
						try:
							self.jsonlist.update(dict(json.load(urlopen(url, timeout=3))))
						except:
							print("[DownloadImage] getImagesList Error: Unable to load json data from alternative URL '%s'!" % url)

			self.imagesList = dict(self.jsonlist)

			for media in ['/media/%s' % x for x in os.listdir('/media')] + (['/media/net/%s' % x for x in os.listdir('/media/net')] if os.path.isdir('/media/net') else []):
				try:
					getImages(media, [os.path.join(media, x) for x in os.listdir(media) if os.path.splitext(x)[1] == ".zip" and checkModels(x)])
					for folder in ["ImagesUpload"]:
						if folder in os.listdir(media):
							subfolder = os.path.join(media, folder)
							if os.path.isdir(subfolder) and not os.path.islink(subfolder) and not os.path.ismount(subfolder):
								getImages(subfolder, [os.path.join(subfolder, x) for x in os.listdir(subfolder) if os.path.splitext(x)[1] == ".zip" and checkModels(x)])
								for dir in [dir for dir in [os.path.join(subfolder, dir) for dir in os.listdir(subfolder)] if os.path.isdir(dir) and os.path.splitext(dir)[1] == ".unzipped"]:
									shutil.rmtree(dir)
				except:
					pass

		list = []
		for catagorie in conditional_sort(self.imagesList.keys(), lambda w: _("Downloaded Images") not in w):
			if catagorie in self.expanded:
				list.append(ChoiceEntryComponent('expanded', ((str(catagorie)), "Expander")))
				for image in reversed(sorted(self.imagesList[catagorie].keys())):
					list.append(ChoiceEntryComponent('verticalline', ((str(self.imagesList[catagorie][image]['name'])), str(self.imagesList[catagorie][image]['link']))))
			else:
				for image in self.imagesList[catagorie].keys():
					list.append(ChoiceEntryComponent('expandable', ((str(catagorie)), "Expander")))
					break
		if list:
			self["list"].setList(list)
			if self.setIndex:
				self["list"].moveToIndex(self.setIndex if self.setIndex < len(list) else len(list) - 1)
				if self["list"].l.getCurrentSelection()[0][1] == "Expander":
					self.setIndex -= 1
					if self.setIndex:
						self["list"].moveToIndex(self.setIndex if self.setIndex < len(list) else len(list) - 1)
				self.setIndex = 0
			self.selectionChanged()
		else:
			self["list"].setList([ChoiceEntryComponent('', ((_("Cannot find images - please try later or select an alternate image")), "Waiter"))])

	def keyOk(self):
		currentSelected = self["list"].l.getCurrentSelection()
		if currentSelected[0][1] == "Expander":
			if currentSelected[0][0] in self.expanded:
				self.expanded.remove(currentSelected[0][0])
			else:
				self.expanded.append(currentSelected[0][0])
			self.getImagesList()
		elif currentSelected[0][1] != "Waiter":
			self.session.openWithCallback(self.reloadImagesList, DownloadImageNeo, currentSelected[0][0], currentSelected[0][1])

	def reloadImagesList(self):
		self["list"].setList([ChoiceEntryComponent('', ((_("Retrieving image list - Please wait...")), "Waiter"))])
		self["list"].moveToIndex(0)
		self.selectionChanged()
		self.imagesList = {}
		self.callLater(self.getImagesList)


	def otherImages(self):
		if len(self.imageBrandList) > 1:
			self.session.openWithCallback(self.otherImagesCallback, ChoiceBox, list=[(key, self.imageBrandList[key]) for key in self.imageBrandList.keys()], windowTitle=_("Select an image brand"))

	def otherImagesCallback(self, image):
		if image:
			self.selectedImage = image
			self.jsonlist = {}
			self.expanded = []
			self.reloadImagesList()

	def selectionChanged(self):
		currentSelected = self["list"].l.getCurrentSelection()
		if currentSelected[0][1] == "Waiter":
			self["key_green"].setText("")
		else:
			if currentSelected[0][1] == "Expander":
				self["key_green"].setText(_("Collapse") if currentSelected[0][0] in self.expanded else _("Expand"))
				self["description"].setText("")
			else:
				self["key_green"].setText(_("Download Image"))
				self["description"].setText(currentSelected[0][1])

	def keyLeft(self):
		self["list"].instance.moveSelection(self["list"].instance.pageUp)
		self.selectionChanged()

	def keyRight(self):
		self["list"].instance.moveSelection(self["list"].instance.pageDown)
		self.selectionChanged()

	def keyUp(self):
		self["list"].instance.moveSelection(self["list"].instance.moveUp)
		self.selectionChanged()

	def keyDown(self):
		self["list"].instance.moveSelection(self["list"].instance.moveDown)
		self.selectionChanged()



class DownloadImageNeo(Screen):
	skin = """<screen position="center,center" size="640,180" flags="wfNoBorder" backgroundColor="#54242424">
		<widget name="header" position="5,10" size="e-10,50" font="Regular;40" backgroundColor="#54242424"/>
		<widget name="info" position="5,60" size="e-10,130" font="Regular;24" backgroundColor="#54242424"/>
		<widget name="progress" position="5,e-39" size="e-10,24" backgroundColor="#54242424"/>
	</screen>"""

	def __init__(self, session, imagename, source):
		Screen.__init__(self, session)
		self.containerbackup = None
		self.containerofgwrite = None
		self.getImageList = None
		self.downloader = None
		self.source = source
		self.imagename = imagename
		self.reasons = getReasons(session)

		self["header"] = Label(_("Backup settings"))
		self["info"] = Label(_("Save settings and EPG data"))
		self["progress"] = ProgressBar()
		self["progress"].setRange((0, 100))
		self["progress"].setValue(0)

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
		{
			"cancel": self.abort,
			"red": self.abort,
			"ok": self.ok,
			"green": self.ok,
		}, -1)

		self.callLater(self.confirmation)

	def confirmation(self):
		if self.reasons:
			self.message = _("%s\nDo you still want to download image\n%s?") % (self.reasons, self.imagename)
		else:
			self.message = _("Do you want to download image\n%s") % self.imagename
		if BoxInfo.getItem("canMultiBoot"):
			pass

		else:
			choices = [(_("Download Image neoboot"))]
			choices.append((_("No, do not flash image"), False))
			self.session.openWithCallback(self.checkMedia, MessageBox, self.message, list=choices, default=False, simple=True)

	def checkMedia(self, retval):
		if retval:
			if BoxInfo.getItem("canMultiBoot"):
				self.multibootslot = retval[0]
				self.onlyDownload = retval[1] == "only download"
			else:
				self.onlyDownload = retval == "only download"

			def findmedia(path):
				def avail(path):
					if not path.startswith('/mmc') and os.path.isdir(path) and os.access(path, os.W_OK):
						try:
							statvfs = os.statvfs(path)
							return (statvfs.f_bavail * statvfs.f_frsize) // (1 << 20)
						except OSError as err:
							print("[DownloadImage] checkMedia Error %d: Unable to get status for '%s'! (%s)" % (err.errno, path, err.strerror))
					return 0

				def checkIfDevice(path, diskstats):
					st_dev = os.stat(path).st_dev
					return (os.major(st_dev), os.minor(st_dev)) in diskstats

				diskstats = [(int(x[0]), int(x[1])) for x in [x.split()[0:3] for x in open('/proc/diskstats').readlines()] if x[2].startswith("sd")]
				if os.path.isdir(path) and checkIfDevice(path, diskstats) and avail(path) > 500:
					return (path, True)
				mounts = []
				devices = []
				for path in ['/media/%s' % x for x in os.listdir('/media')] + (['/media/net/%s' % x for x in os.listdir('/media/net')] if os.path.isdir('/media/net') else []):
					try:
						if checkIfDevice(path, diskstats):
							devices.append((path, avail(path)))
						else:
							mounts.append((path, avail(path)))
					except OSError:
						pass
				devices.sort(key=lambda x: x[1], reverse=True)
				mounts.sort(key=lambda x: x[1], reverse=True)
				return ((devices[0][1] > 500 and (devices[0][0], True)) if devices else mounts and mounts[0][1] > 500 and (mounts[0][0], False)) or (None, None)

			if os.path.isdir('/media/usb/ImagesUpload'):
			        self.destination, isDevice = findmedia('/media/usb')
			else:
                                self.destination, isDevice = findmedia('/media/hdd')   


			if self.destination:
				destination = os.path.join(self.destination, 'ImagesUpload')
				self.zippedimage = "://" in self.source and os.path.join(destination, self.imagename) or self.source
				self.unzippedimage = os.path.join(destination, '%s.unzipped' % self.imagename[:-4])

				try:
					if os.path.isfile(destination):
						os.remove(destination)
					if not os.path.isdir(destination):
						os.mkdir(destination)
					self.startDownload()
				except:
					self.session.openWithCallback(self.abort, MessageBox, _("Unable to create the required directories on the media (e.g. USB stick or Harddisk) - Please verify media and try again!"), type=MessageBox.TYPE_ERROR, simple=True)
			else:
				self.session.openWithCallback(self.abort, MessageBox, _("Could not find suitable media - Please remove some downloaded images or insert a media (e.g. USB stick) with sufficiant free space and try again!"), type=MessageBox.TYPE_ERROR, simple=True)
		else:
			self.abort()

	def startDownload(self, reply=True):
		self.show()
		if reply:
			if "://" in self.source:
				from Tools.Downloader import downloadWithProgress
				self["header"].setText(_("Downloading Image"))
				self["info"].setText(self.imagename)
				self.downloader = downloadWithProgress(self.source, self.zippedimage)
				self.downloader.addProgress(self.downloadProgress)
				self.downloader.addEnd(self.downloadEnd)
				self.downloader.addError(self.downloadError)
				self.downloader.start()
			else:
				pass
		else:
			self.abort()

	def downloadProgress(self, current, total):
		self["progress"].setValue(int(100 * current / total))

	def downloadError(self, reason, status):
		self.downloader.stop()
		self.session.openWithCallback(self.abort, MessageBox, _("Error during downloading image\n%s\n%s") % (self.imagename, reason), type=MessageBox.TYPE_ERROR, simple=True )

	def downloadEnd(self):
		self.downloader.stop()
		self.downloadfinish()
		
	def downloadfinish(self):
				self.abort(self.session.open(MessageBox, _("Downloading image successful. Press Exit..."), MessageBox.TYPE_INFO, 30, simple=True ))
		
	def abort(self, reply=None):
		if self.getImageList or self.containerofgwrite:
			return 0
		if self.downloader:
			self.downloader.stop()
		if self.containerbackup:
			self.containerbackup.killAll()
		self.close()
		
		
	def ok(self):
		if self["header"].text == _("Downloading image successful"):
			self.session.openWithCallback(self.abort, MultibootSelection)
		else:
			return 0
                        
                        	
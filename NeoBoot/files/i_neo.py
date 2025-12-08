from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import getReasons
from Components.Sources.StaticText import StaticText
from Components.ChoiceList import ChoiceList, ChoiceEntryComponent
from Components.config import config, configfile
from Components.ActionMap import ActionMap
from Components.Console import Console
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from Components.SystemInfo import BoxInfo
from Tools.BoundFunction import boundFunction
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, fileExists, pathExists, fileHas
from Tools.Downloader import downloadWithProgress
from Tools.HardwareInfo import HardwareInfo
from Tools.Multiboot import getImagelist, getCurrentImage, getCurrentImageMode, deleteImage, restoreImages
import os
import re
from urllib.request import urlopen, Request
import xml.etree.ElementTree
import json
import time
import zipfile
import shutil
import tempfile
import struct

from enigma import eEPGCache, eEnv


def checkimagefiles(files):
	return len([x for x in files if 'kernel' in x and '.bin' in x or x in ('uImage', 'rootfs.bin', 'root_cfe_auto.bin', 'root_cfe_auto.jffs2', 'oe_rootfs.bin', 'e2jffs2.img', 'rootfs.tar.bz2', 'rootfs.ubi')]) == 2


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
		self.session.openWithCallback(self.abort, MessageBox, _("Error during downloading image\n%s\n%s") % (self.imagename, reason), type=MessageBox.TYPE_ERROR, simple=True)

	def downloadEnd(self):
		self.downloader.stop()
		self.downloadfinish()
		
	def downloadfinish(self):
		self.session.openWithCallback(self.abort, MessageBox, _("Downloading image successful"), type=MessageBox.TYPE_INFO, simple=True)
		
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
			

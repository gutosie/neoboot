
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os

# mercus = /neoskins/mercus/mercus_skin.py

### ImageChooseFULLHD  - mercus
ImageChooseFULLHD = """
<screen name="ImageChooseFULLHD" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/test1.png" alphatest="blend" position="15,center" size="1920,1080" zPosition="-2" />
  <widget name="config" position="1200,200" size="660,365" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" itemHeight="43" font="baslk;30" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#99FFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
  <widget name="progreso" position="91,543" size="530,12" borderWidth="1" zPosition="3" />
  <widget name="device_icon" position="681,483" size="147,136" alphatest="on" zPosition="2" />
  <widget name="key_red" position="140,992" zPosition="1" size="552,38" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="key_green" position="761,992" zPosition="1" size="229,38" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="key_yellow" position="1080,992" zPosition="1" size="550,38" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="key_blue" position="1684,992" zPosition="1" size="235,38" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red.png" position="90,992" size="34,34" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green.png" position="714,992" size="34,34" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow.png" position="1030,992" size="34,34" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue.png" position="1637,992" size="34,34" zPosition="1" alphatest="blend" />
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="foreground" position="85,58" size="1000,55" text=" NeoBoot  Multi-image " transparent="1" />
  <widget name="key_1" position="150,768" zPosition="1" size="363,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="key_2" position="150,818" zPosition="1" size="431,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="key_3" position="150,868" zPosition="1" size="367,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="label1" position="1200,145" size="660,48" zPosition="1" halign="center" font="Regular; 30" foregroundColor="red" backgroundColor="black" transparent="1" />
  <widget name="label2" position="90,200" zPosition="1" size="652,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="label3" position="77,606" zPosition="1" size="540,99" font="Regular; 28" halign="center" valign="bottom" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label4" position="90,255" zPosition="1" size="550,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="label5" position="801,200" zPosition="1" size="340,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />
  <widget name="label6" position="627,255" zPosition="1" size="516,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label7" position="835,310" zPosition="1" size="308,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label8" position="90,310" zPosition="1" size="666,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="label9" position="90,420" zPosition="1" size="784,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="label10" position="1019,365" zPosition="1" size="125,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label13" position="90,365" zPosition="1" size="415,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="label14" position="90,145" zPosition="1" size="350,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
  <widget name="label15" position="90,475" zPosition="1" size="265,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" foregroundColor="green" transparent="1" />
  <widget name="label9" position="422,146" zPosition="1" size="720,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget source="global.CurrentTime" render="Label" position="1646,45" size="225,37" backgroundColor="black" transparent="1" zPosition="1" font="Regular;33" valign="center" halign="right">
    <convert type="ClockToText">Format:%-H:%M</convert>
  </widget>
  <widget source="global.CurrentTime" render="Label" position="1421,82" size="450,38" backgroundColor="black" transparent="1" zPosition="1" font="Regular;22" valign="center" halign="right">
    <convert type="ClockToText">Date</convert>
  </widget>
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_1.png" alphatest="blend" position="90,770" size="52,38" zPosition="3" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_2.png" alphatest="blend" position="90,820" size="52,38" zPosition="3" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_3.png" alphatest="blend" position="90,870" size="52,38" zPosition="3" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_menu.png" alphatest="blend" position="90,920" size="52,38" zPosition="3" />
  <widget source="session.VideoPicture" render="Pig" position="1200,582" size="660,370" backgroundColor="transparent" zPosition="1" />
  <widget name="key_menu" position="135,915" zPosition="1" size="249,46" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#99FFFF" />
</screen>
"""

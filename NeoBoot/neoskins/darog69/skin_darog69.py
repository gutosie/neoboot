
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os
# darog69 = ./neoskins/darog69/skin_darog69.py

### ImageChooseFULLHD  - darog69
ImageChooseFULLHD = """
<screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">
  <widget name="progreso" position="594,590" size="530,10" borderWidth="1" zPosition="3" />
  <ePixmap position="center,0" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/darog69/skin3.png" />
  <widget name="config" position="1290,256" size="595,380" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/darog69/selektor.png" itemHeight="43" zPosition="3" font="baslk;32" scrollbarMode="showOnDemand" foregroundColor="#99FFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="yellow" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#99FFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
  <ePixmap position="54,1008" zPosition="-7" size="1809,45" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek.png" />
  <ePixmap position="71,903" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,820" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,736" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="70,655" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="64,417" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="1865,190" size="40,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/updown.png" alphatest="on" />
  <ePixmap position="1340,780" zPosition="4" size="510,185" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/box.png" />
  <ePixmap position="1305,660" zPosition="5" size="565,107" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/logo.png" alphatest="on" />
  <eLabel position="70,615" size="1080,2" backgroundColor="red" foregroundColor="red" name="linia" />
  <widget name="device_icon" position="123,476" size="146,136" alphatest="on" zPosition="2" />
  <widget name="key_red" position="80,1010" zPosition="1" size="567,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_green" position="692,1010" zPosition="1" size="325,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="key_yellow" position="1030,1010" zPosition="1" size="547,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="key_blue" position="1600,1010" zPosition="1" size="260,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="red" position="60,25" size="400,50" text=" NeoMultiBoot " valign="center" transparent="1" />
  <ePixmap position="65,429" size="73,42" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/darog69/menu.png" alphatest="on" zPosition="6" />
  <widget name="key_menu" position="165,420" size="269,45" font="Regular;30" zPosition="1" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#808080" position="90,659" size="80,46" text="1 &gt;" valign="center" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#808080" position="92,742" size="80,43" text="2 &gt;" valign="center" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#808080" position="90,826" size="80,42" text="3 &gt;" valign="center" transparent="1" />
  <widget name="key_1" position="178,660" zPosition="1" size="397,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_2" position="177,742" zPosition="1" size="403,42" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="key_3" position="176,826" zPosition="1" size="403,43" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label1" position="1288,145" size="601,99" zPosition="1" halign="center" font="Regular;28" foregroundColor="red" backgroundColor="black" transparent="1" />
  <widget name="label2" position="69,164" zPosition="1" size="543,66" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label3" position="588,475" zPosition="1" size="545,97" font="Regular;28" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label4" position="65,245" zPosition="1" size="481,66" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label5" position="840,163" zPosition="1" size="305,66" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />
  <widget name="label7" position="1074,324" zPosition="1" size="70,66" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label8" position="67,324" zPosition="1" size="1004,66" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label9" position="841,25" zPosition="1" size="292,50" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="label10" position="990,420" zPosition="1" size="125,55" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="label13" position="599,420" zPosition="1" size="374,55" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label15" position="322,573" zPosition="1" size="265,40" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget source="session.VideoPicture" render="Pig" position="586,625" size="645,328" zPosition="3" backgroundColor="transparent" />
  <widget name="label14" position="470,25" zPosition="1" size="350,50" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label19" position="75,909" size="498,43" font="Regular;22" halign="left" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="orange" />
  <widget name="label6" position="550,235" zPosition="1" size="594,84" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label17" position="619,164" size="213,66" font="Regular;30" halign="right" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#00ff7f50" />
  <widget name="label16" position="1137,25" zPosition="1" size="142,50" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label20" position="1295,25" zPosition="1" size="625,50" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />

</screen>

"""

###

# neo = /neoskins/neo/neo_skin.py - gutosie

from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os


#Colors (#AARRGGBB)
#____Recommended colors - Zalecane kolory :
#color name="white" value="#ffffff"
#color name="darkwhite" value="#00dddddd"
#color name="red" value="#f23d21"
#color name="green" value="#389416"
#color name="blue" value="#0064c7"
#color name="yellow" value="#bab329"
#color name="orange" value="#00ffa500"
#color name="gray" value="#808080"
#color name="lightgrey" value="#009b9b9b"

#   font genel
#   font baslk
#   font tasat
#   font dugme

#jak by chcial ktos wlasny selektor, to przyklad:
#  <widget name="label19" position="73,422" size="596,25" font="tasat;22" halign="left" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="orange" />

### ImageChooseFULLHD
ImageChooseFULLHD = """
<screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">
  <eLabel backgroundColor="black" font="tasat;30" foregroundColor="red" position="75,50" size="309,45" valign="center" text="NEOBoot Multi-image" transparent="1" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/skin.png" position="center,center" zPosition="-7" size="1920,1080"  />
  <ePixmap position="54,981" zPosition="-7" size="1809,55" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek.png" />
  <ePixmap position="71,890" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,803" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,727" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="70,652" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="64,410" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="1170,186" size="45,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/updown.png" alphatest="on" />

  <eLabel position="70,152" size="1075,2" backgroundColor="blue" name="linia" />
  <eLabel position="70,395" size="1075,2" backgroundColor="blue" name="linia2" />
  <widget name="device_icon" position="355,465" size="185,115" alphatest="on" zPosition="2" />
  <ePixmap position="70,471" size="275,179" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" alphatest="blend" zPosition="3" />

  <widget source="session.VideoPicture" render="Pig" position="588,625" size="545,340" backgroundColor="transparent" zPosition="1" />

  <widget name="key_red" position="130,990" zPosition="1" size="505,38" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00dddddd" />
  <widget name="key_green" position="690,990" zPosition="1" size="328,38" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00dddddd" />
  <widget name="key_yellow" position="1085,990" zPosition="1" size="476,38" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00dddddd" />
  <widget name="key_blue" position="1620,990" zPosition="1" size="240,38" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00dddddd" />

 <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red.png" position="80,990" size="34,38" zPosition="1" alphatest="blend" />
 <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green.png" position="640,990" size="34,38" zPosition="1" alphatest="blend" />
 <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow.png" position="1035,990" size="34,38" zPosition="1" alphatest="blend" />
 <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue.png" position="1570,990" size="34,38" zPosition="1" alphatest="blend" />

#Window image selection - Okno wyboru image
  <widget name="config" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" position="1175,256" size="680,689" itemHeight="45" font="dugme;30" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#99FFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />

#Used Kernel:
  <widget name="label19" position="73,422" size="596,25" font="tasat;22" halign="left" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="orange" />

#More options - Menu
  <ePixmap position="70,898" size="55,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_menu.png" alphatest="blend" zPosition="3" />
  <ePixmap position="150,902" size="66,35" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/arrowleft.png" alphatest="blend" zPosition="3" />
  <widget name="key_menu" position="232,895" zPosition="1" size="343,40" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />

#key 1&gt; 2&gt; 3&gt;
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_1.png" alphatest="blend" position="65,657" size="55,40" zPosition="3" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_2.png" alphatest="blend" position="65,732" size="55,40" zPosition="3" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_3.png" alphatest="blend" position="65,807" size="55,40" zPosition="3" />
  <widget name="key_1" position="130,657" zPosition="1" size="445,45" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_2" position="130,732" zPosition="1" size="445,45" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="key_3" position="130,807" zPosition="1" size="445,45" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />

#Please choose an image to boot
  <widget name="label1" position="1177,150" size="703,105" zPosition="1" halign="left" font="tasat;30" foregroundColor="red" backgroundColor="black" transparent="1" />

#NeoBoot is running from:
  <widget name="label2" position="70,164" zPosition="1" size="538,66" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00dddddd" />
  <widget name="label5" position="837,164" zPosition="1" size="305,66" font="tasat;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00ffa500" />

#NeoBoot is running image:
  <widget name="label4" position="70,245" zPosition="1" size="505,65" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00dddddd" />
  <widget name="label6" position="580,235" zPosition="1" size="565,82" font="tasat;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00f23d21" />

#Memory disc: - Pamiec dysku
  <widget name="label15" position="345,585" zPosition="1" size="240,40" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00ffa500" />
  <widget name="progreso" position="587,600" size="552,10" borderWidth="1" zPosition="3" foregroundColor="#00ffa500" />

#Number of images installed:
  <widget name="label8" position="70,324" zPosition="1" size="987,66" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00dddddd" />
  <widget name="label7" position="1060,324" zPosition="1" size="85,66" font="tasat;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00ff7f50" />

#Version update:
  <widget name="label13" position="675,415" zPosition="1" size="345,40" font="tasat;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
#UPDATEVERSION
  <widget name="label10" position="1030,415" zPosition="1" size="100,40" font="tasat;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />

#NeoBoot version:
  <widget name="label14" position="532,50" zPosition="1" size="302,45" font="tasat;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#009b9b9b" />
#PLUGINVERSION
  <widget name="label9" position="847,50" zPosition="1" size="315,45" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#808080" />

#Kernel Version
  <widget name="label16" position="1171,50" zPosition="1" size="114,45" font="tasat;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#009b9b9b" />
#KERNELVERSION
  <widget name="label20" position="1302,50" zPosition="1" size="608,45" font="tasat;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#808080" />

#hostname
    <widget name="label17" position="619,164" size="213,66" font="tasat;30" halign="right" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#00ff7f50" />

#Memory - Used: Available:
  <widget name="label3" position="533,465" zPosition="1" size="612,120" font="tasat;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />

#VIP
  <widget name="label21" position="384,49" size="148,45" font="dugme;30" halign="center" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#00ff7f50" />

</screen>
"""


###ImageChoose-HD


from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os
# darog69 = ./neoskins/darog69_Ustym4kpro/skin_darog69_Ustym4kpro.py

### ImageChooseFULLHD  - darog69_Ustym4kpro
ImageChooseFULLHD = """
<screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">
  <widget name="progreso" position="595,590" size="530,15" borderWidth="1" zPosition="3" />
  <ePixmap position="center,0" zPosition="-3" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/darog69_Ustym4kpro/skin.png" />
  <ePixmap position="54,981" zPosition="-7" size="1809,55" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek.png" />
  <ePixmap position="71,903" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,820" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,736" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="70,655" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="64,417" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="1822,168" size="45,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/updown.png" alphatest="on" />
  <ePixmap position="1280,700" zPosition="4" size="500,138" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/darog69_Ustym4kpro/ustym4k.png" />
  <ePixmap position="1239,867" zPosition="4" size="580,55" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/darog69_Ustym4kpro/Neoboot-Ustym.png" />
  <eLabel position="60,392" size="1080,2" backgroundColor="red" foregroundColor="red" name="linia1" />
  <eLabel position="60,950" size="1080,2" backgroundColor="red" foregroundColor="red" name="linia2" />
  <widget source="session.VideoPicture" render="Pig" position="590,610" size="540,300" zPosition="3" backgroundColor="transparent" />
  <widget name="device_icon" position="75,470" size="220,155" alphatest="on" zPosition="2" />
  <widget name="key_red" position="149,1010" zPosition="1" size="280,48" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_green" position="571,1010" zPosition="1" size="276,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="key_yellow" position="1010,1010" zPosition="1" size="275,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="key_blue" position="1470,1010" zPosition="1" size="276,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />
  <widget name="config" position="1230,250" size="615,390" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/darog69_Ustym4kpro/sel_image.png" font="Regular;32" itemHeight="43" scrollbarMode="showOnDemand" backgroundColor="black" transparent="1" />
  <widget name="key_menu" position="254,419" zPosition="1" size="249,45" font="Regular;33" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="un99ffff" />
  <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="green" position="34,35" size="560,55" text=" NeoBoot Ustym4kPro - MENU" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="yellow" position="140,424" size="155,41" text="MENU &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="unc0c0c0" position="90,659" size="80,46" text="1 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="unc0c0c0" position="90,742" size="80,43" text="2 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="unc0c0c0" position="90,826" size="80,42" text="3 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="unc0c0c0" position="90,909" size="80,39" text="4 &gt;" transparent="1" />
  <widget name="key_1" position="150,660" zPosition="1" size="363,46" font="Regular;32" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_2" position="149,742" zPosition="1" size="431,42" font="Regular;32" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="key_3" position="149,826" zPosition="1" size="367,43" font="Regular;32" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label1" position="1220,145" size="620,100" zPosition="1" halign="center" font="Regular;35" foregroundColor="red" backgroundColor="black" transparent="1" />
  <widget name="label2" position="69,164" zPosition="1" size="652,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label3" position="315,460" zPosition="1" size="799,124" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label4" position="68,244" zPosition="1" size="606,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label5" position="802,163" zPosition="1" size="340,66" font="Regular;35" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />
  <widget name="label6" position="628,235" zPosition="1" size="516,82" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label7" position="836,323" zPosition="1" size="308,66" font="Regular;35" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label8" position="67,324" zPosition="1" size="666,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label9" position="950,25" zPosition="1" size="950,56" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="unff00" />
  <widget name="label10" position="985,410" zPosition="1" size="125,55" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="unff00" />
  <widget name="label13" position="610,410" zPosition="1" size="415,55" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label14" position="595,25" zPosition="1" size="350,56" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label15" position="322,584" zPosition="1" size="265,42" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label19" position="150,910" zPosition="1" size="750,45" font="Regular;35" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="unff00" />

</screen>

"""

###

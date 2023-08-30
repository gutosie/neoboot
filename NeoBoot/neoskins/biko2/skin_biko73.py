
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os
# biko73 = ./neoskins/biko/skin_biko73.py

### ImageChooseFULLHD  - biko73
ImageChooseFULLHD = """
<screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">
  <widget name="progreso" position="560,525" size="450,10" borderWidth="1" zPosition="3" />
  <widget name="config" position="1120,265" size="700,547" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/selektor.png" itemHeight="50" zPosition="3" font="LiberationSans-Bold;34" scrollbarMode="showOnDemand" foregroundColor="#99ffff" backgroundColor="#1a0f0f0f" foregroundColorSelected="white" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#99FFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
  <widget name="device_icon" position="123,455" size="146,136" alphatest="on" zPosition="2" />
  <widget source="global.CurrentTime" render="Label" position="1120,15" size="500,50" font="Console; 34" valign="bottom" halign="center" backgroundColor="skincolor" transparent="1">
    <convert type="ClockToText">Format:%A, %d %B %Y</convert>
  </widget>
  <widget source="global.CurrentTime" render="Label" position="1590,13" size="269,50" font="LCD; 52" valign="bottom" halign="center" transparent="1" foregroundColor="#FFC200" backgroundColor="background">
    <convert type="ClockToText">Format:%H:%M</convert>
  </widget>
  <widget source="global.CurrentTime" render="Label" position="1790,25" size="55,34" font="LCD; 32" valign="top" halign="left" backgroundColor="black" foregroundColor="#FFC200" transparent="1">
    <convert type="ClockToText">Format::%S</convert>
  </widget>
  <widget source="session.VideoPicture" render="Pig" position="640,650" size="437,236" zPosition="4" backgroundColor="transparent" />
  <widget name="key_menu" position="135,645" size="269,45" font="Regular;38" zPosition="1" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="key_red" position="15,985" zPosition="1" size="567,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#fb353d" />
  <widget name="key_green" position="590,985" zPosition="1" size="325,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#5cbd0a" />
  <widget name="key_yellow" position="1075,985" zPosition="1" size="260,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#fdba2b" />
  <widget name="key_blue" position="1505,985" zPosition="1" size="260,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#036dc1" />
  <eLabel backgroundColor="black" font="Regular; 44" foregroundColor="#1192D7" position="35,10" size="341,50" text=" NeoMultiBoot " valign="bottom" transparent="1" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/button_red.png" position="140,1030" size="317,27" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/button_green.png" position="595,1030" size="317,27" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/button_yellow.png" position="1045,1030" size="317,27" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/button_blue.png" position="1475,1030" size="317,27" zPosition="1" alphatest="blend" />
  <ePixmap position="30,650" size="60,40" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/key_Menu.png" alphatest="on" zPosition="2" />
  <ePixmap position="30,1020" size="60,40" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/key_Exit.png" alphatest="on" zPosition="2" />
  <ePixmap position="635,625" size="450,330" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/video1.png" alphatest="on" zPosition="3" /> 
  <ePixmap position="center,0" size="1920,1078" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/background.png" />  
  <ePixmap position="45,130" size="30,30" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/icon_1.png" alphatest="on" />
  <ePixmap position="45,210" size="30,30" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/icon_1.png" alphatest="on" />
  <ePixmap position="45,300" size="30,30" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/icon_1.png" alphatest="on" />
  <ePixmap position="45,395" size="30,30" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/icon_1.png" alphatest="on" />
  <ePixmap position="1850,765" size="556,122" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/up.png" alphatest="on" />
  <ePixmap position="1850,270" size="556,122" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/down.png" alphatest="on" />
  <ePixmap position="1177,85" zPosition="4" size="573,122" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/logo_neoboot.png" alphatest="blend" />
  <ePixmap position="1107,88" zPosition="5" scale="1" size="714,76" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/bg.png" alphatest="on" />
  <ePixmap position="905,280" zPosition="5" scale="1" size="75,75" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/R.png" alphatest="on" />
  <ePixmap position="1178,835" zPosition="5" size="562,113" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/box.png" alphatest="on" />
  <ePixmap position="45,725" size="40,40" scale="1" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/key_1.png" alphatest="blend" />
  <ePixmap position="45,785" size="40,40" scale="1" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/key_2.png" alphatest="blend" />
  <ePixmap position="45,850" size="40,40" scale="1" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko2/key_3.png" alphatest="blend" />  
  <widget name="key_1" position="135,720" zPosition="1" size="405,45" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#036dc1" />
  <widget name="key_2" position="135,787" zPosition="1" size="405,45" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#fb353d" />
  <widget name="key_3" position="135,851" zPosition="1" size="405,45" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#fdba2b" />
  <widget name="label1" position="1106,153" size="719,126" zPosition="4" halign="center" font="Regular;38" foregroundColor="#fb353d" backgroundColor="black" transparent="1" />
  <widget name="label2" position="105,110" zPosition="1" size="777,66" font="Regular;33" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label4" position="105,195" zPosition="1" size="774,66" font="Regular;33" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label5" position="675,110" zPosition="1" size="305,66" font="Regular;34" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#036dc1" />
  <widget name="label6" position="625,190" zPosition="1" size="357,84" font="Regular;34" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#fdba2b" />
  <widget name="label7" position="905,285" zPosition="1" size="70,66" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#5cbd0a" />
  <widget name="label8" position="105,285" zPosition="1" size="776,66" font="Regular;33" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label9" position="600,5" zPosition="1" size="295,50" font="Regular;30" halign="center" valign="bottom" backgroundColor="black" transparent="1" foregroundColor="#FFD150" />
  <widget name="label10" position="855,385" zPosition="1" size="125,55" font="Regular;34" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#8D5944" />
  <widget name="label11" position="499,460" zPosition="1" size="513,55" font="Regular;28" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#FE999E" />
  <widget name="label13" position="480,385" zPosition="1" size="374,55" font="Regular;38" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#8D5944" />
  <widget name="label14" position="345,5" zPosition="1" size="350,50" font="Regular;30" halign="right" valign="bottom" backgroundColor="black" transparent="1" foregroundColor="#5cbd0a" />
  <widget name="label15" position="285,510" zPosition="1" size="265,40" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#5cbd0a" />
  <widget name="label16" position="25,910" zPosition="1" size="142,50" font="Bold;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#808080" />
  <widget name="label17" position="870,10" size="267,50" font="Regular;40" halign="center" valign="bottom" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#ff7f50" />
  <widget name="label18" position="500,545" zPosition="1" size="597,69" font="Regular;28" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#fdba2b" />
  <widget name="label19" position="105,385" size="500,45" font="Regular;28" halign="left" valign="left" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#808080" />
  <widget name="label20" position="190,910" zPosition="1" size="625,50" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#808080" />
  <widget name="label21" position="385,645" zPosition="1" size="220,50" font="Regular;28" halign="center" valign="left" backgroundColor="black" transparent="1" foregroundColor="#C4A393" />
</screen>

"""

###

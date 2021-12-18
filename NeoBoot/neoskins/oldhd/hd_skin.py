
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os


###____ Skin HD - ImageChoose ___mod. gutosie ___
ImageChooseHD = """
<screen name="NeoBootImageChoose" position="center,center" size="1280, 720" backgroundColor="transpBlack">
  <ePixmap position="0,0" zPosition="-1" size="1274,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1frame_base-fs8.png" />
  <widget source="session.VideoPicture" render="Pig" position=" 836,89" size="370,208" zPosition="3" backgroundColor="#ff000000" />
  <ePixmap position="870,304" zPosition="-1" size="300,14" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1chan_p1_bar.png" alphatest="on" />
  <widget source="Title" render="Label" position="12,5" size="788,30" font="Regular;28" halign="left" foregroundColor="#58bcff" backgroundColor="transpBlack" transparent="1" />
  <widget name="label9" position="818,4" zPosition="10" size="385,30" font="Regular;24" foregroundColor="#58bcff" backgroundColor="black" halign="left" transparent="1" />
  <widget selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/slekvti.png" name="config"  enableWrapAround="1" position="30,150" size="270,370" itemHeight="25" font="Regular;18" zPosition="2" foregroundColor="#00cc99" scrollbarMode="showNever" transparent="1" />
  <widget name="device_icon" position="470,71" size="177,132" alphatest="on" zPosition="2" />
  <ePixmap position="20,135" zPosition="1" size="280,400" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/border_menu1.png"  />
  <widget name="progreso" position="369,216" size="377,11" borderWidth="1" zPosition="3" foregroundColor="white" />
  <widget name="label3" position="328,232" zPosition="1" size="477,60" font="Regular;20" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
  <ePixmap position="319,426" zPosition="4" size="500,4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/separator.png" alphatest="blend" transparent="1" />
  <ePixmap position="319,310" zPosition="4" size="500,4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/separator.png" alphatest="blend" transparent="1" />
  <widget name="label2" position="320,340" zPosition="1" size="275,26" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label5" position="600,339" zPosition="1" size="164,27" font="Regular;20" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
  <widget name="label4" position="25,597" zPosition="1" size="319,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="label6" position="346,597" zPosition="1" size="444,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="label8" position="320,381" zPosition="1" size="378,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label7" position="700,381" zPosition="1" size="66,25" font="Regular;20" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
  <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="319,450" size="51,25" text="1 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="318,480" size="52,25" text="2 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="318,510" size="52,25" text="3 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="317,540" size="53,25" text="4 &gt;" transparent="1" />
  <widget name="key_1" position="375,450" zPosition="1" size="349,25" font="Regular;18" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="key_2" position="374,480" zPosition="1" size="350,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="key_3" position="373,510" zPosition="1" size="350,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label19" position="373,540" zPosition="1" size="438,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <ePixmap position="926,489" zPosition="1" size="228,130" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="-4,650" size="209,40" alphatest="blend" />
  <widget name="key_red" position="0,670" zPosition="2" size="250,45" font="Regular; 15" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green25.png" position="213,650" size="204,40" alphatest="blend" />
  <widget name="key_green" position="259,671" size="155,45" zPosition="1" font="Regular; 15" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow25.png" position="431,650" size="247,40" alphatest="blend" />
  <widget name="key_yellow" position="421,670" size="270,46" zPosition="1" font="Regular; 15" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue25.png" position="690,650" size="197,40" alphatest="blend" />
  <widget name="key_blue" position="712,670" size="209,46" zPosition="1" font="Regular; 15" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
  <widget name="key_menu" position="1065,648" zPosition="1" size="181,45" font="Regular;22" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58bcff" />
  <eLabel backgroundColor="black" font="Regular; 24" foregroundColor="white" position="950,651" size="102,45" halign="left" valign="center" text="MENU &gt;" transparent="1" />
  <widget source="global.CurrentTime" render="Label" position="1052,39" size="152,41" backgroundColor="black" transparent="1" zPosition="1" font="Regular;25" valign="center" halign="right">
  <convert type="ClockToText">Format:%-H:%M</convert>
  </widget>
</screen>
"""

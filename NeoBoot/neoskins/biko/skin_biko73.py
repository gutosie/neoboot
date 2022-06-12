
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os
# biko73 = ./neoskins/biko/skin_biko73.py

### ImageChooseFULLHD  - biko73
ImageChooseFULLHD = """
<screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">
  <widget name="progreso" position="627,590" size="452,10" borderWidth="1" zPosition="3" />    
  <ePixmap position="center,0" size="1920,1078" zPosition="-2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko/background.png" />  
  <widget name="config" position="1289,266" size="620,688" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko/selektor.png" itemHeight="43" zPosition="3" font="baslk;32" scrollbarMode="showOnDemand" foregroundColor="#99FFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="yellow" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#99FFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
  <ePixmap position="1865,190" size="556,122" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko/updown.png" alphatest="on" />
  <ePixmap position="1304,43" zPosition="4" size="556,122" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/logo.png" alphatest="on" />
  <ePixmap position="1304,43" zPosition="5" scale="1" size="556,122" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko/bg.png" alphatest="on" />
  <ePixmap position="1022,166" zPosition="5" size="258,106" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/box.png" alphatest="on" /> 
  <eLabel position="60,615" size="1040,2" backgroundColor="#C0C0C0" foregroundColor="#C0C0C0" name="linia" /> 
  <widget name="device_icon" position="123,476" size="146,136" alphatest="on" zPosition="2" />
  
  <widget source="global.CurrentTime" render="Label" position="864,46" size="430,40" font="Console; 30" valign="center" halign="center" backgroundColor="skincolor" transparent="1">
    <convert type="ClockToText">Format:%A, %d %B %Y</convert>
  </widget>
  <widget source="global.CurrentTime" render="Label" position="1001,100" size="269,45" font="Console; 38" valign="center" halign="center" transparent="1" foregroundColor="clock_color" backgroundColor="background">
   <convert type="ClockToText">Format:%H:%M</convert>
  </widget>
  <widget source="global.CurrentTime" render="Label" position="1205,96" size="55,34" font="Console; 28" valign="top" halign="left" backgroundColor="black" foregroundColor="white" transparent="1">
   <convert type="ClockToText">Format::%S</convert>
  </widget>
  
  <widget name="key_red" position="80,1000" zPosition="1" size="567,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_green" position="692,1000" zPosition="1" size="325,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="key_yellow" position="1310,1000" zPosition="1" size="260,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="key_blue" position="1625,1000" zPosition="1" size="260,40" font="Regular;34" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />
  
  
  <eLabel backgroundColor="black" font="Regular; 44" foregroundColor="red" position="35,45" size="298,50" text=" NeoMultiBoot " valign="center" transparent="1" />  
  <ePixmap position="50,424" size="73,42" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko/menu_setup.png" alphatest="on" zPosition="6" />   
  <widget name="key_menu" position="140,420" size="269,45" font="Regular;30" zPosition="1" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />  
  
  
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#808080" position="90,719" size="80,43" text="1 &gt;" valign="center" transparent="1" /> 
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#808080" position="90,787" size="80,43" text="2 &gt;" valign="center" transparent="1" />
  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#808080" position="90,851" size="80,43" text="3 &gt;" valign="center" transparent="1" />
  
  
  <widget name="key_1" position="178,720" zPosition="1" size="397,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_2" position="177,787" zPosition="1" size="403,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="key_3" position="176,851" zPosition="1" size="403,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />

  
  
  <widget name="label1" position="1288,215" size="601,99" zPosition="4" halign="center" font="Regular;38" foregroundColor="red" backgroundColor="black" transparent="1" />  
  <widget name="label2" position="49,149" zPosition="1" size="543,66" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" /> 
  <widget name="label3" position="637,475" zPosition="1" size="426,97" font="Regular;28" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />  
  <widget name="label4" position="50,235" zPosition="1" size="481,66" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label5" position="615,148" zPosition="1" size="305,66" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />  
  <widget name="label7" position="854,324" zPosition="1" size="70,66" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
  <widget name="label8" position="47,324" zPosition="1" size="498,66" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />    
  <widget name="label9" position="638,45" zPosition="1" size="292,50" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="label10" position="800,420" zPosition="1" size="125,55" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />   
  <widget name="label13" position="414,420" zPosition="1" size="374,55" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label15" position="322,573" zPosition="1" size="265,40" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />   
  <widget source="session.VideoPicture" render="Pig" position="650,665" size="398,223" zPosition="3" backgroundColor="transparent" />
  <ePixmap position="625,645" size="450,330" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko/video.png" alphatest="on" zPosition="4" /> 
  <widget name="label14" position="335,45" zPosition="1" size="350,50" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label19" position="184,641" size="393,43" font="Regular;22" halign="left" valign="left" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="orange" /> 
  <ePixmap position="55,639" size="105,64" scale="1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/biko/arrowright.png" alphatest="on" />
  
  <widget name="label6" position="567,235" zPosition="1" size="357,84" font="Regular;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label17" position="1049,281" size="213,66" font="Regular;30" halign="center" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#00ff7f50" />
  <widget name="label16" position="76,924" zPosition="1" size="142,50" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
  <widget name="label20" position="223,924" zPosition="1" size="625,50" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
</screen>

"""

###

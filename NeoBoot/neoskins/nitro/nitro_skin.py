# skin = ./neoskins/nitro_skin - mod. gutosie

from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os

### ImageChooseFULLHD                      
ImageChooseFULLHD = """
<screen name="ImageChooseFULLHD" position="center,center" size="1920,1080" title=" " flags="wfBorder" backgroundColor="background" >
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/background.png" position="center,0" size="1920,1080" alphatest="blend" />
    <widget name="config" position="1196,182" size="660,386" itemHeight="43" zPosition="3" font="baslk;32" scrollbarMode="showOnDemand" foregroundColor="#99FFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="yellow" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#99FFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
    <widget name="progreso" position="75,459" size="530,10" borderWidth="1" zPosition="3" />
    <widget name="device_icon" position="632,446" size="157,136" alphatest="on" zPosition="2" backgroundColor="black" />
    <widget name="key_red" position="41,960" zPosition="1" size="255,70" font="Regular;30" halign="center" valign="center" foregroundColor="red" transparent="1" backgroundColor="black" />
    <widget name="key_green" position="324,960" zPosition="1" size="255,70" font="Regular;30" halign="center" valign="center" foregroundColor="green" transparent="1" backgroundColor="black" />
    <widget name="key_yellow" position="615,960" zPosition="1" size="255,70" font="Regular;30" halign="center" valign="center" foregroundColor="yellow" transparent="1" backgroundColor="black" />
    <widget name="key_blue" position="900,960" zPosition="1" size="255,70" font="Regular;30" halign="center" valign="center" foregroundColor="blue" transparent="1" backgroundColor="black" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/red.png" position="41,950" size="255,44" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/green.png" position="324,950" size="255,45" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/yellow.png" position="615,950" size="255,45" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/blue.png" position="900,950" size="255,45" alphatest="blend" />
    <widget name="key_1" position="140,660" zPosition="1" size="390,45" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" />
    <widget name="key_2" position="140,728" zPosition="1" size="390,45" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" />    
    <widget name="key_3" position="140,791" zPosition="1" size="390,45" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" />
    <widget name="label1" position="1194,127" size="720,48" zPosition="1" halign="left" font="Regular; 34" foregroundColor="#00FF00" backgroundColor="black" transparent="1" />
    <widget name="label2" position="75,145" zPosition="1" size="652,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
    <widget name="label3" position="75,473" zPosition="1" size="540,99" font="Regular; 28" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
    <widget name="label4" position="75,210" zPosition="1" size="550,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
    <widget name="label5" position="809,145" zPosition="1" size="340,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />
    <widget name="label6" position="628,210" zPosition="1" size="521,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
    <widget name="label7" position="842,273" zPosition="1" size="308,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
    <widget name="label8" position="75,273" zPosition="1" size="666,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
    <widget name="label9" position="433,77" zPosition="1" size="720,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />    
    <widget name="label10" position="964,336" zPosition="1" size="185,46" font="Regular; 30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
    <widget name="label13" position="75,336" zPosition="1" size="415,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
    <widget name="label14" position="73,77" zPosition="1" size="350,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" transparent="1" />
    <widget name="label15" position="75,408" zPosition="1" size="265,46" font="Regular; 30" halign="left" valign="center" backgroundColor="black" foregroundColor="yellow" transparent="1" />
    <widget name="label17" position="255,12" zPosition="1" size="451,46" font="Regular; 42" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="black" />
    <widget name="label19" position="70,909" zPosition="1" size="462,35" font="Regular; 25" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="black" />
    <widget name="label21" position="75,12" zPosition="1" size="178,46" font="Regular; 42" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="black" />
    <widget source="global.CurrentTime" render="Label" position="1626,35" size="225,37" backgroundColor="black" transparent="1" zPosition="1" font="Regular; 33" valign="center" halign="right">
      <convert type="ClockToText">Format:%-H:%M</convert>
    </widget>
    <widget source="global.CurrentTime" render="Label" position="1404,84" size="450,38" backgroundColor="black" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
      <convert type="ClockToText">Date</convert>
    </widget>
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/key_1_FHD.png" alphatest="blend" position="75,659" size="50,50" zPosition="3" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/key_2_FHD.png" alphatest="blend" position="75,727" size="50,50" zPosition="3" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/key_3_FHD.png" alphatest="blend" position="75,790" size="50,50" zPosition="3" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_menu.png" alphatest="blend" position="70,855" size="58,50" zPosition="3" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/div-h.png" alphatest="blend" position="75,389" size="1095,15" zPosition="3" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/nitro/skin/div-h.png" alphatest="blend" position="75,588" size="1095,15" zPosition="3" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" alphatest="off" position="554,623" size="545,340" zPosition="3" />
    <widget source="session.VideoPicture" render="Pig" position="1196,589" size="679,378" backgroundColor="transparent" zPosition="1" />
    <widget name="key_menu" position="140,848" zPosition="1" size="390,46" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#99ffff" />
</screen>
"""

# skin = ./meoskins/defaul_skin   - gutosie

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
#        green = '#00389416' lub #00389416
#        red = '#00ff2525'
#        yellow = '#00ffe875'
#        orange = '#00ff7f50'
#   seledynowy  =  #00FF00
#   jasny-blue  =  #99FFFF

# Zamiast font=Regular ktory nie rozpoznaje polskich znakow np. na VTi, mozesz zmienic na ponizsze font="*:
    #   font -  genel
    #   font -  baslk
    #   font -  tasat
    #   font -  dugme

#  <widget name="config" position="1177,256" size="703,717" itemHeight="43" font="genel;30" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#00FFFFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />

###____ Skin Ultra HD - ImageChooseFULLHD   ___ mod. gutosie___
ImageChooseFULLHD = """
<screen name="ImageChooseFULLHD" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">
  <eLabel backgroundColor="black" font="dugme; 30" foregroundColor="#99FFFF" position="70,50" size="298,55" valign="center" text="NEOBoot Multi-image" transparent="1" />
  <widget name="config" position="1177,250" size="668,715" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" itemHeight="45" font="dugme;30" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#99FFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
  <widget name="progreso" position="590,600" size="542,10" borderWidth="1" zPosition="3" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/skin.png" position="center,center" zPosition="-7" size="1920,1080" />
  <ePixmap position="54,981" zPosition="-7" size="1809,55" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek.png" />
  <ePixmap position="71,903" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,820" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="71,736" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="70,655" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="64,417" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />
  <ePixmap position="587,631" zPosition="-2" size="545,340" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />
  <ePixmap position="1170,186" size="45,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/updown.png" alphatest="on" />
  <eLabel position="70,155" size="1075,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
  <eLabel position="70,395" size="1075,2" backgroundColor="blue" foregroundColor="blue" name="linia2" />
  <widget name="device_icon" position="131,490" size="176,136" alphatest="on" zPosition="2" />
  <widget name="key_red" position="130,990" zPosition="1" size="507,38" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00ff0d0d" />
  <widget name="key_green" position="690,990" zPosition="1" size="334,38" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" />
  <widget name="key_yellow" position="1085,990" zPosition="1" size="480,38" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="key_blue" position="1620,990" zPosition="1" size="240,38" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#0000cbf6" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red.png" position="80,990" size="34,38" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green.png" position="640,990" size="34,38" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow.png" position="1035,990" size="34,38" zPosition="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue.png" position="1570,990" size="34,38" zPosition="1" alphatest="blend" />
  <widget name="key_menu" position="230,425" zPosition="1" size="300,30" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00ffe875" />
  <ePixmap position="80,426" size="75,31" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/menu.png" transparent="1" alphatest="blend" />
  <ePixmap position="158,427" size="70,31" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/arrowleft.png" alphatest="blend" zPosition="3" />
  <eLabel backgroundColor="black" font="dugme; 30" foregroundColor="#00dddddd" position="85,660" size="59,45" valign="center" text="1 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="dugme; 30" foregroundColor="#00dddddd" position="85,742" size="59,45" valign="center" text="2 &gt;" transparent="1" />
  <eLabel backgroundColor="black" font="dugme; 30" foregroundColor="#00dddddd" position="85,826" size="61,45" valign="center" text="3 &gt;" transparent="1" />
  <widget name="key_1" position="150,660" zPosition="1" size="425,45" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
  <widget name="key_2" position="150,742" zPosition="1" size="423,45" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" />
  <widget name="key_3" position="150,826" zPosition="1" size="425,45" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label1" position="1179,147" size="661,99" zPosition="1" halign="center" font="dugme;33" foregroundColor="red" backgroundColor="black" transparent="1" />
  <widget name="label2" position="70,164" zPosition="1" size="561,66" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label3" position="505,475" zPosition="1" size="625,110" font="dugme;28" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label4" position="70,244" zPosition="1" size="476,66" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label5" position="951,164" zPosition="1" size="191,66" font="dugme;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00ffe875" />
  <widget name="label16" position="1169,50" zPosition="1" size="186,55" font="dugme;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#99FFFF" />
  <widget name="label7" position="1073,323" zPosition="1" size="71,66" font="dugme;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" />
  <widget name="label8" position="70,324" zPosition="1" size="1000,66" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
  <widget name="label10" position="1028,421" zPosition="1" size="102,50" font="dugme;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label13" position="699,421" zPosition="1" size="316,50" font="dugme;30" halign="right" valign="center" backgroundColor="black" transparent="1"/>
  <widget name="label14" position="552,50" zPosition="1" size="281,55" font="dugme;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#99FFFF" />
  <widget name="label15" position="322,586" zPosition="1" size="265,42" font="dugme;30" halign="center" valign="right" backgroundColor="black" transparent="1" />
  <widget name="label6" position="551,235" zPosition="1" size="593,85" font="dugme;30" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label17" position="674,162" size="274,66" font="dugme;30" halign="right" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#00ffe875" />
  <widget name="label9" position="845,47" zPosition="1" size="306,56" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label19" position="80,907" size="502,45" font="dugme;25" halign="left" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="orange" />
  <widget name="label20" position="1368,50" zPosition="1" size="537,55" font="dugme;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
  <widget name="label21" position="371,49" size="179,56" font="dugme;30" halign="center" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="#00ff7f50" />
  <widget name="label22" position="1180,830" size="660,90" font="dugme;45" halign="center" valign="center" zPosition="1" backgroundColor="black" transparent="1" foregroundColor="yellow" />

</screen>
"""


###____ Skin Ultra HD - ImageChooseULTRAHD ___ mod. gutosie___
ImageChooseULTRAHD = """
<screen name="NeoBootImageChoose" position="0,0" size="3840,2160" flags="wfNoBorder" backgroundColor="#ff111111">
  <widget source="Title" render="Label" position="174,108" size="1575,150" font="baslk;102" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" noWrap="1" transparent="1" />
  <widget name="label1" position="210,360" size="2100,90" font="genel;60" foregroundColor="#00DAA520" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <widget name="config" position="210,480" size="2100,510" itemHeight="102" font="genel;60" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#00FFFFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
  <eLabel position="210,1020" size="2100,3" backgroundColor="#0027408B" />
  <widget name="label2" position="252,1050" size="780,90" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />
  <widget name="label4" position="252,1140" size="780,90" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />
  <widget name="label8" position="252,1230" size="780,90" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />
  <widget name="label5" position="1062,1050" size="1230,90" font="genel;60" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <widget name="label6" position="1062,1140" size="1230,90" font="genel;60" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <widget name="label7" position="1062,1230" size="1230,90" font="genel;60" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <eLabel position="210,1350" size="2100,3" backgroundColor="#0027408B" />
  <ePixmap position="210,1410" size="90,90" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/key_1_UHD.png" zPosition="1" alphatest="blend" />
  <ePixmap position="210,1512" size="90,90" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/key_2_UHD.png" zPosition="1" alphatest="blend" />
  <ePixmap position="210,1614" size="90,90" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/key_3_UHD.png" zPosition="1" alphatest="blend" />
  <widget position="330,1410" size="660,78" name="key_1" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <widget position="330,1512" size="660,78" name="key_2" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <widget position="330,1614" size="660,78" name="key_3" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <widget name="device_icon" position="1110,1428" size="216,252" zPosition="1" transparent="1" alphatest="blend" />
  <widget name="label3" position="1410,1428" size="900,90" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <widget name="progreso" position="1416,1536" size="660,33" borderWidth="0" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" zPosition="2" transparent="1" />
  <eLabel position="1416,1551" size="660,3" backgroundColor="#00FFFFFF" zPosition="1" />
  <widget name="label11" position="1410,1578" size="900,90" font="genel;60" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
  <ePixmap position="2850,1800" size="243,120" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_menu_UHD.png" transparent="1" alphatest="blend" />
  <ePixmap position="3135,1800" size="243,120" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_ok_UHD.png" transparent="1" alphatest="blend" />
  <ePixmap position="3420,1800" size="243,120" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_exit_UHD.png" transparent="1" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_red_UHD.png" position="105,1905" size="90,120" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_green_UHD.png" position="654,1905" size="90,120" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_yellow_UHD.png" position="1203,1905" size="90,120" alphatest="blend" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_blue_UHD.png" position="1752,1905" size="90,120" alphatest="blend" />
  <widget name="key_red" position="210,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
  <widget name="key_green" position="759,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
  <widget name="key_yellow" position="1308,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
  <widget name="key_blue" position="1857,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
  <eLabel position="120,75" zPosition="-10" size="2265,1950" backgroundColor="#1A0F0F0F" name="layer1" />
  <eLabel position="2385,180" zPosition="-10" size="1335,1740" backgroundColor="#1A27408B" name="layer2" />
  <ePixmap position="2700,600" size="768,258" zPosition="5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/logo.png" transparent="1" alphatest="blend" />
  <widget source="global.CurrentTime" render="Label" position="1956,90" size="420,180" font="tasat;150" noWrap="1" halign="center" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
  <convert type="ClockToText">Default</convert></widget>
  <widget source="global.CurrentTime" render="Label" position="1536,90" size="420,81" font="tasat;48" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
  <convert type="ClockToText">Format:%A</convert></widget>
  <widget source="global.CurrentTime" render="Label" position="1536,162" size="420,81" font="tasat;48" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
  <convert type="ClockToText">Format:%e. %b.</convert>
  </widget>
</screen>"""


###____ Skin HD - ImageChoose ___mod. gutosie ___
ImageChooseHD = """
<screen name="NeoBootImageChoose" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#ff111111">\n
                <widget source="Title" render="Label" position="58,36" size="712,50" font="baslk;28" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" noWrap="1" transparent="1" />\n
                <widget name="label1" position="70,120" size="700,30" font="genel;20" foregroundColor="#00DAA520" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" /> \n
                <widget name="config" position="70,160" size="700,170" itemHeight="34" font="genel;20" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#00FFFFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />\n
                <eLabel position="70,340" size="700,1" backgroundColor="#0027408B" />\n
                <widget name="label2" position="84,350" size="260,30" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />\n
                <widget name="label4" position="84,380" size="260,30" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />\n
                <widget name="label8" position="84,410" size="260,30" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />\n
                <widget name="label5" position="354,350" size="410,30" font="genel;20" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <widget name="label6" position="354,380" size="410,30" font="genel;20" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <widget name="label7" position="354,410" size="410,30" font="genel;20" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <eLabel position="70,450" size="700,1" backgroundColor="#0027408B" />\n
                <ePixmap position="70,470" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_1.png" zPosition="1" alphatest="blend" />\n
                <ePixmap position="70,504" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_2.png" zPosition="1" alphatest="blend" />\n
                <ePixmap position="70,538" size="30,30" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/key_3.png" zPosition="1" alphatest="blend" />\n
                <widget position="110,470" size="220,26" name="key_1" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <widget position="110,504" size="220,26" name="key_2" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <widget position="110,538" size="220,26" name="key_3" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <widget name="device_icon" position="338,463" size="126,93" zPosition="1" transparent="1" alphatest="blend" />\n
                <widget name="label3" position="470,476" size="300,30" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <widget name="progreso" position="472,512" size="220,11" borderWidth="0" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" zPosition="2" transparent="1" />\n
                <eLabel position="472,517" size="220,1" backgroundColor="#00FFFFFF" zPosition="1" />\n
                <widget name="label11" position="470,526" size="300,30" font="genel;20" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />\n
                <ePixmap position="950,600" size="81,40" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/menu1.png" transparent="1" alphatest="blend" />\n
                <ePixmap position="1045,600" size="81,40" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok1.png" transparent="1" alphatest="blend" />\n
                <ePixmap position="1140,600" size="81,40" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/exit.png" transparent="1" alphatest="blend" />\n
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red.png" position="35,635" size="30,40" alphatest="blend" />\n
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green.png" position="294,633" size="30,40" alphatest="blend" />\n
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow.png" position="431,634" size="30,40" alphatest="blend" />\n
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue.png" position="670,633" size="30,40" alphatest="blend" />\n
                <widget name="key_red" position="71,639" size="225,30" noWrap="1" zPosition="1" valign="center" font="dugme;18" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />\n
                <widget name="key_green" position="331,638" size="108,30" noWrap="1" zPosition="1" valign="center" font="dugme;18" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />\n
                <widget name="key_yellow" position="471,639" size="198,30" noWrap="1" zPosition="1" valign="center" font="dugme;18" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />\n
                <widget name="key_blue" position="710,638" size="104,30" noWrap="1" zPosition="1" valign="center" font="dugme;18" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />\n
                <eLabel position="40,25" zPosition="-10" size="754,650" backgroundColor="#1A0F0F0F" name="layer1" />\n
                <eLabel position="795,60" zPosition="-10" size="445,580" backgroundColor="#1A27408B" name="layer2" />\n
                <ePixmap position="817,335" size="422,229" zPosition="5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" transparent="1" alphatest="blend" />\n
                <ePixmap position="943,179" size="295,60" zPosition="5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ico_neo.png" transparent="1" alphatest="blend" />\n
                <widget source="global.CurrentTime" render="Label" position="1089,73" size="140,60" font="tasat;50" noWrap="1" halign="center" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
                <convert type="ClockToText">Default</convert>
                </widget>\n
                <widget source="global.CurrentTime" render="Label" position="933,73" size="140,27" font="tasat;16" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
                <convert type="ClockToText">Format:%A</convert>
                </widget>\n
                <widget source="global.CurrentTime" render="Label" position="935,105" size="140,27" font="tasat;16" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1"><convert type="ClockToText">Format:%e. %b.</convert>
                </widget>\n
</screen>
"""


###____ Skin FULLHD - MyUpgradeFULLHD ___mod. gutosie ___
MyUpgradeFULLHD = """
<screen name="MyUpgradeFULLHD" position="center,center" size="1380,570" title="Tools Neoboot">
                  <ePixmap position="594,255" zPosition="-2" size="623,313" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />
                  <widget source="list" render="Listbox" position="33,101" size="1328,124" scrollbarMode="showOnDemand">
                  <convert type="TemplatedMultiContent">\
                    {"template": [MultiContentEntryText(pos = (90, 1), size = (1250, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                                  MultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
                                 ],
                                 "fonts": [gFont("dugme", 40)],
                                 "itemHeight": 66
                    }
                  </convert>
                  </widget>
                  <eLabel text="---NeoBoot upgrade new version--- " font="tasat; 40" position="188,21" size="1042,70" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />
                  <eLabel text="Exit -Back" font="tasat; 40" position="27,441" size="389,80" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
                </screen>"""


###____ Skin UltraHD - MyUpgradeUltraHD ___mod. gutosie ___
MyUpgradeUltraHD = """
<screen name="MyUpgradeUltraHD" position="center,center" size="2100,1020" flags="wfNoBorder" backgroundColor="#ff111111">
        <widget name="label1" position="180,210" size="1740,78" font="genel;60" halign="center" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" zPosition="1" transparent="1" />
        <widget source="list" render="Listbox" position="210,390" size="1680,252" itemHeight="132" font="genel;66" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#00FFFFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1">
        <convert type="TemplatedMultiContent">
          {"template": [MultiContentEntryText(pos=(0,0), size=(1680,132), flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER, text=0)], "fonts": [gFont("Regular",66)], "itemHeight":132}\n        </convert>
          </widget>
          <widget name="label2" position="180,600" size="1740,78" font="genel;60" halign="center" foregroundColor="#00DAA520" backgroundColor="#1A0F0F0F" zPosition="1" transparent="1" />
          <ePixmap position="774,840" size="243,120" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/logo.png" transparent="1" alphatest="blend" />
          <ePixmap position="1083,840" size="243,120" zPosition="2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_exit_UHD.png" transparent="1" alphatest="blend" />
          <eLabel position="120,0" zPosition="-2" size="1890,60" backgroundColor="#1A27408B" name="popupUst" />
          <eLabel position="0,60" zPosition="-2" size="2100,900" backgroundColor="#1A0F0F0F" name="popupOrt" />
          <eLabel position="90,900" zPosition="-1" size="1920,120" backgroundColor="#1A27408B" name="popupAlt" />
        </screen>"""


###____ Skin MyUpgradeHD - MyUpgradeHD ___mod. gutosie ___
MyUpgradeHD = """
<screen name="MyUpgradeHD" position="center,center" size="1127,569" title="Tools NeoBoot">
                  <ePixmap position="492,223" zPosition="-2" size="589,298" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />
                  <widget source="list" render="Listbox" position="18,122" size="1085,82" scrollbarMode="showOnDemand">
                    <convert type="TemplatedMultiContent">
                      {"template": [MultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                                    MultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
                                   ],
                                   "fonts": [gFont("Regular", 40)],
                                   "itemHeight": 66
                      }
                    </convert>
                  </widget>
                  <eLabel text="NeoBoot wykry\xc5\x82 nowsz\xc4\x85 wersj\xc4\x99 wtyczki. " font="Regular; 40" position="27,40" size="1042,70" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />
                  <eLabel text="EXIT - Zrezygnuj" font="Regular; 40" position="27,441" size="389,80" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
                </screen>"""


###____ Skin NeoBootInstallationFULLHD - NeoBootInstallationFULLHD ___mod. gutosie ___
NeoBootInstallationFULLHD = """
<screen name="NeoBootInstallationFULLHD" position="410,138" size="1200,850" title="NeoBoot">
        <widget name="label3" position="10,632" size="1178,114" zPosition="1" halign="center" font="dugme;28" backgroundColor="black" transparent="1" foregroundColor="#ffffff" />
        <ePixmap position="643,282" zPosition="-2" size="531,331" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />
        <eLabel position="15,76" size="1177,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
        <eLabel position="10,622" size="1168,3" backgroundColor="blue" foregroundColor="blue" name="linia" />
        <eLabel position="14,752" size="1168,3" backgroundColor="blue" foregroundColor="blue" name="linia" />
        <eLabel position="15,276" size="1183,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
        <widget name="label1" position="14,4" size="1180,62" zPosition="1" halign="center" font="dugme;28" backgroundColor="black" transparent="1" foregroundColor="#ffffff" />
        <widget name="label2" position="15,82" size="1178,190" zPosition="1" halign="center" font="dugme;28" backgroundColor="black" transparent="1" foregroundColor="yellow" />
        <widget name="config" position="15,285" size="641,329" font="dugme; 28" itemHeight="42" scrollbarMode="showOnDemand" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="48,812" size="140,28" alphatest="on" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="311,816" size="185,28" alphatest="on" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="614,815" size="150,28" alphatest="on" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="958,817" size="140,26" alphatest="on" />
        <widget name="key_red" position="19,760" zPosition="1" size="221,47" font="dugme; 28" halign="center" valign="center" backgroundColor="red" transparent="1" foregroundColor="red" />
        <widget name="key_green" position="289,761" zPosition="1" size="227,47" font="dugme; 28" halign="center" valign="center" backgroundColor="green" transparent="1" foregroundColor="green" />
        <widget name="key_yellow" position="583,760" zPosition="1" size="224,51" font="dugme; 28" halign="center" valign="center" backgroundColor="yellow" transparent="1" foregroundColor="yellow" />
        <widget name="key_blue" position="856,761" zPosition="1" size="326,52" font="dugme; 28" halign="center" valign="center" backgroundColor="blue" transparent="1" foregroundColor="blue" />
        </screen>"""

###____ Skin NeoBootInstallationUltraHD - NeoBootInstallationUltraHD ___mod. gutosie ___
NeoBootInstallationUltraHD = """
<screen name="NeoBootInstallationUltraHD" position="0,0" size="3840,2160" flags="wfNoBorder" backgroundColor="#ff111111">
        <widget source="Title" render="Label" position="174,108" size="1575,150" font="baslk;102" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" noWrap="1" transparent="1" />
        <widget name="label1" position="210,360" size="2100,90" font="genel;72" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" zPosition="1" transparent="1" />
        <widget name="label2" position="210,480" size="2100,570" font="genel;60" foregroundColor="#00DAA520" backgroundColor="#1A0F0F0F" zPosition="1" transparent="1" />
        <widget name="config" position="210,690" size="2100,540" itemHeight="108" font="genel;60" zPosition="2" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#00FFFFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
        <eLabel position="210,1470" size="2100,3" backgroundColor="#0027408B" />
        <widget name="label3" position="150,1500" size="2100,90" font="genel;60" halign="center" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" zPosition="1" transparent="1" />
        <eLabel position="210,1620" size="2100,3" backgroundColor="#0027408B" />
        <ePixmap position="3420,1800" size="243,120" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_exit_UHD.png" transparent="1" alphatest="blend" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_red_UHD.png" position="105,1905" size="90,120" alphatest="blend" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_green_UHD.png" position="654,1905" size="90,120" alphatest="blend" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_yellow_UHD.png" position="1203,1905" size="90,120" alphatest="blend" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_blue_UHD.png" position="1752,1905" size="90,120" alphatest="blend" />
        <widget name="key_red" position="210,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
        <widget name="key_green" position="759,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
        <widget name="key_yellow" position="1308,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
        <widget name="key_blue" position="1857,1914" size="510,90" noWrap="1" zPosition="1" valign="center" font="dugme;60" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
        <eLabel position="120,75" zPosition="-10" size="2265,1950" backgroundColor="#1A0F0F0F" name="layer1" />
        <eLabel position="2385,180" zPosition="-10" size="1335,1740" backgroundColor="#1A27408B" name="layer2" />
        <ePixmap position="2700,600" size="768,258" zPosition="5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/logo.png" transparent="1" alphatest="blend" />
        <widget source="global.CurrentTime" render="Label" position="1956,90" size="420,180" font="tasat;150" noWrap="1" halign="center" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1"><convert type="ClockToText">Default</convert>
        </widget>
        <widget source="global.CurrentTime" render="Label" position="1536,90" size="420,81" font="tasat;48" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
        <convert type="ClockToText">Format:%A</convert>
        </widget>
        <widget source="global.CurrentTime" render="Label" position="1536,162" size="420,81" font="tasat;48" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1"><convert type="ClockToText">Format:%e. %b.</convert>
        </widget>
        </screen>"""


###____ Skin NeoBootInstallationHD - NeoBootInstallationHD ___mod. gutosie ___
NeoBootInstallationHD = """
<screen position="center, center" size="835, 500" title="NeoBoot">
  <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />
  <widget name="label1" position="10,15" size="840,30" zPosition="1" halign="center" font="Regular;25" foregroundColor="red" backgroundColor="black" transparent="1" />
  <widget name="label2" position="7,100" size="840,296" zPosition="1" halign="center" font="Regular;20" backgroundColor="black" foregroundColor="#58ccff" transparent="1"/>
  <widget name="config" position="220,200" size="440,207" backgroundColor="black" scrollbarMode="showOnDemand"  />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="48,406" size="140,40" alphatest="on"    />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="246,406" size="140,40" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="474,406" size="150,40" alphatest="on" />
  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="675,406" size="140,40" alphatest="on" />
  <widget name="key_red" position="48,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
  <widget name="key_green" position="248,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
  <widget name="key_yellow" position="474,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="yellow" transparent="1" />
  <widget name="key_blue" position="672,415" zPosition="1" size="145,45" font="Regular;20" halign="center" valign="center" backgroundColor="blue" transparent="1" />
  <widget name="label3" position="20,339" size="816,61" zPosition="1" halign="center" font="Regular;24" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
  </screen>"""


from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os

# skin /neoskins/matrix/matrix_skin.py - mod.gutosie

### ImageChooseFULLHD
ImageChooseFULLHD = """
<screen name="NeoBootImageChoose" position="0,0" size="1920,1080" flags="wfNoBorder" backgroundColor="#ff111111">
<widget source="Title" render="Label" position="97,50" size="1067,72" font="baslk;41" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" noWrap="1" transparent="1" />
<widget name="label1" position="105,180" size="1050,45" font="genel;30" foregroundColor="#00DAA520" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget name="config" position="105,240" size="1050,255" itemHeight="51" font="genel;30" scrollbarMode="showOnDemand" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" foregroundColorSelected="#00FFFFF" backgroundColorSelected="#1A27408B" scrollbarSliderBorderWidth="1" scrollbarWidth="8" scrollbarSliderForegroundColor="#00FFFFFF" scrollbarSliderBorderColor="#0027408B" enableWrapAround="1" transparent="1" />
<eLabel position="105,510" size="1050,2" backgroundColor="#0027408B" />
<widget name="label2" position="108,525" size="590,45" font="genel;30" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget name="label4" position="108,570" size="518,45" font="genel;30" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget name="label8" position="109,615" size="964,45" font="genel;30" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget name="label5" position="944,525" size="212,45" font="genel;30" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />
<widget name="label6" position="633,570" size="522,45" font="genel;30" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />
<widget name="label7" position="1089,615" size="66,45" font="genel;30" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="center" valign="center" zPosition="1" transparent="1" />
<widget name="label17" position="716,525" size="213,45" font="genel;30" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" halign="right" valign="center" zPosition="1" transparent="1" />
<widget name="label19" position="130,879" size="1020,40" font="genel;30" halign="left" valign="center" zPosition="1" foregroundColor="#0058CCFF" backgroundColor="#1A0F0F0F" transparent="1" />
<ePixmap position="1234,261" size="615,262" zPosition="5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/logo.png" transparent="1" alphatest="blend" />
<ePixmap position="1260,583" size="564,262" zPosition="5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/neoAdam.png" transparent="1" alphatest="blend" />
<eLabel position="105,675" size="1050,2" backgroundColor="#0027408B" />
<ePixmap position="105,705" size="45,45" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/key_1_FHD.png" zPosition="1" alphatest="blend" />
<ePixmap position="105,756" size="45,45" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/key_2_FHD.png" zPosition="1" alphatest="blend" />
<ePixmap position="105,807" size="45,45" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/key_3_FHD.png" zPosition="1" alphatest="blend" />
<widget position="165,705" size="330,39" name="key_1" font="genel;30" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget position="165,756" size="330,39" name="key_2" font="genel;30" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget position="165,807" size="330,39" name="key_3" font="genel;30" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget name="device_icon" position="516,707" size="146,138" zPosition="1" transparent="1" alphatest="blend" />
<widget name="label18" position="680,715" size="510,45" font="genel;28" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<widget name="progreso" position="683,766" size="332,15" borderWidth="0" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" zPosition="2" transparent="1" />
<eLabel position="684,774" size="330,2" backgroundColor="#00FFFFFF" zPosition="1" />
<widget name="label11" position="680,790" size="510,45" font="genel;28" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" halign="left" valign="center" zPosition="1" transparent="1" />
<ePixmap position="1425,900" size="122,60" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_menu_FHD.png" transparent="1" alphatest="blend" />
<ePixmap position="1568,900" size="122,60" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_ok_FHD.png" transparent="1" alphatest="blend" />
<ePixmap position="1710,900" size="122,60" zPosition="10" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/bt_exit_FHD.png" transparent="1" alphatest="blend" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_red_FHD.png" position="48,953" size="45,60" alphatest="blend" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_green_FHD.png" position="401,953" size="45,60" alphatest="blend" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_yellow_FHD.png" position="590,953" size="45,60" alphatest="blend" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/metrix/skin/btc_blue_FHD.png" position="967,953" size="45,60" alphatest="blend" />
<widget name="key_red" position="100,957" size="327,45" noWrap="1" zPosition="1" valign="center" font="dugme;30" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
<widget name="key_green" position="455,957" size="166,45" noWrap="1" zPosition="1" valign="center" font="dugme;30" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
<widget name="key_yellow" position="647,957" size="349,45" noWrap="1" zPosition="1" valign="center" font="dugme;30" halign="left" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
<widget name="key_blue" position="1021,959" size="174,45" noWrap="1" zPosition="1" valign="cener" font="dugme;30" halign="feft" backgroundColor="#1A0F0F0F" foregroundColor="#00FFFFFF" transparent="1" />
<eLabel position="39,38" zPosition="-10" size="1155,975" backgroundColor="#1A0F0F0F" name="layer1" />
<eLabel position="1194,90" zPosition="-10" size="668,876" backgroundColor="#1A27408B" name="layer2" />
<widget source="global.CurrentTime" render="Label" position="1636,119" size="210,90" font="tasat;75" noWrap="1" halign="center" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
<convert type="ClockToText">Default</convert>
</widget>
<widget source="global.CurrentTime" render="Label" position="1356,119" size="276,41" font="tasat;24" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
<convert type="ClockToText">Format:%A</convert>
</widget>
<widget source="global.CurrentTime" render="Label" position="1357,167" size="275,41" font="tasat;24" noWrap="1" halign="right" valign="bottom" foregroundColor="#00FFFFFF" backgroundColor="#1A0F0F0F" transparent="1">
<convert type="ClockToText">Format:%e. %b.</convert>
</widget>

</screen>

"""

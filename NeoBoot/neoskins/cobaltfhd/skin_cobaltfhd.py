# skin = ./neoskins/cobaltfhd_skin - mod. gutosie

from Screens.Screen import Screen
from Components.Pixmap import Pixmap
import os

# ImageChooseFULLHD
ImageChooseFULLHD = """
	 <screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title="NeoBoot" flags="wfNoBorder" backgroundColor="background" transparent="0">
	 		  <ePixmap position="0,0" zPosition="-10" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/channel.png" transparent="1" />
          	  <widget source="global.CurrentTime" render="Label" position="980,60" size="920,50" font="Regular;32" valign="center" halign="right" backgroundColor="transpBlack" foregroundColor="#58bcff" transparent="1">
      <convert type="ClockToText">Format:%A  %e  %B  %Y  </convert>
	   </widget>
	      <widget source="global.CurrentTime" render="Label" position="980,20" size="920,50" font="Regular;32" valign="center" halign="right"  backgroundColor="transpBlack" transparent="1" foregroundColor="#58bcff">
      <convert type="ClockToText">Format:%H:%M:%S </convert>
    </widget>
	   	 <ePixmap position="76,133" size="622,364" zPosition="4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/ramka622x364.png" alphatest="blend" />
	 <widget source="session.VideoPicture" render="Pig" position=" 78,135" size="620,362" zPosition="3" backgroundColor="#ff000000"/>
          <eLabel  position="20,20" size="720,50" font="Regular;44" halign="center" foregroundColor="#58bcff" backgroundColor="transpBlack"  text=" NeoMultiBoot "  transparent="1" />
 
		  <widget source="session.CurrentService" render="Label" position="130,90" size="520,38" zPosition="2" font="Regular;34" halign="center" noWrap="1" transparent="1" foregroundColor="white" backgroundColor="background">
		<convert type="ServiceName">Name</convert>
		</widget>
			<widget source="session.Event_Now" render="Label" position="160,570" size="450,60" zPosition="2" halign="center" font="Regular;28" foregroundColor="#58bcff" backgroundColor="transpBlack" transparent="1" >
			<convert type="EventName">Name</convert>
					</widget>		
		<widget source="session.Event_Now" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/chan_p_bar.png" position="185,545" zPosition="1" size="400,10" borderWidth="1"  borderColor="#606060"  transparent="1">	<convert type="EventTime">Progress</convert>
            </widget>
			 <widget source="session.Event_Now" render="Label" position="60,535" size="105,33" halign="right" font="Regular; 28" foregroundColor="ciel" backgroundColor="black" transparent="1" valign="center" zPosition="10">
      <convert type="EventTime">StartTime</convert>
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <widget source="session.Event_Now" render="Label" position="610,535" size="105,33" halign="left" font="Regular; 28" foregroundColor="ciel" backgroundColor="black" transparent="1" valign="center" zPosition="10">
      <convert type="EventTime">EndTime</convert>
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
	<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/red.png" position="800,1040" size="250,20" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/green.png" position="1060,1040" size="250,20" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/yellow.png" position="1320,1040" size="250,20" alphatest="blend" />
    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/blue.png" position="1580,1040" size="250,20" alphatest="blend" />
  <widget name="key_red" position="800,1000" size="250,30" zPosition="1" font="Regular;26" halign="center" backgroundColor="black" transparent="1" />
 <widget name="key_green" position="1060,1000" size="250,30" zPosition="1" font="Regular;26" halign="center" backgroundColor="black" transparent="1" />
 <widget name="key_yellow" position="1320,1000" size="250,30" zPosition="1" font="Regular;26" halign="center" backgroundColor="black" transparent="1" />
 <widget name="key_blue" position="1580,1000" size="250,30" zPosition="1" font="Regular;26" halign="center" backgroundColor="black" transparent="1" />	
   <widget name="config" position="80,640" size="600,330" font="Regular;28"  selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/button600x40.png"  itemHeight="40"  scrollbarMode="showOnDemand" backgroundColor="background" foregroundColor="#bbbbbb" transparent="1" />
	<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/menu.png" position="300,1025" size="100,40" alphatest="blend" />
	<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/exit.png" position="450,1025" size="100,40" alphatest="blend" />
	 <widget name="label9" position="1200,60" zPosition="1" size="292,50" font="Regular;32" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58bcff" />
   
<widget name="label14" position="770,60" zPosition="1" size="350,50" font="Regular;32" halign="right" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58bcff" />
 
   <widget name="device_icon" position="1200,200" size="146,136" alphatest="on" zPosition="2" />   
	     <widget name="progreso" position="970,330" size="530,15" borderWidth="1" zPosition="3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/neoskins/cobaltfhd/progressmovie7.png" />
          <eLabel text="Pamięć Dysku:" position="1100,370" zPosition="1" size="265,42" font="Regular;32" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />
	 <widget name="label3" position="870,400" zPosition="1" size="799,124" font="Regular;30" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
       <ePixmap position="900,520" zPosition="4" size="700,5" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/separator2.png" alphatest="blend" transparent="1" />
	       <widget name="label5" position="1300,548" zPosition="1" size="340,35" font="Regular;28" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />         
            <widget name="label6" position="1300,580" zPosition="1" size="516,35" font="Regular;28" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />          
            <widget name="label7" position="1300,630" zPosition="1" size="308,35" font="Regular;28" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />  
            <widget name="label8" position="800,630" zPosition="1" size="500,35" font="Regular;28" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />
             <widget name="label4" position="800,590" zPosition="1" size="500,35" font="Regular;28" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />  
		    <widget name="label2" position="800,550" zPosition="1" size="500,35" font="Regular;28" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />  
	  <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#58ccff" position="890,700" size="80,46" text="1 &gt;" transparent="1" />  
	    <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#58ccff" position="890,740" size="80,43" text="2 &gt;" transparent="1" />  
	    <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#58ccff" position="890,780" size="80,42" text="3 &gt;" transparent="1" />          
	    <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="#58ccff" position="890,820" size="80,39" text="4 &gt;" transparent="1" />  
	  <widget name="key_1" position="940,700" zPosition="1" size="363,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />          
	    <widget name="key_2" position="940,740" zPosition="1" size="431,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />  
	    <widget name="key_3" position="940,780" zPosition="1" size="367,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />  
	    <widget name="label19" position="940,820" zPosition="1" size="713,40" font="Regular;30" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#bbbbbb" />    
	 <ePixmap position="1440,700" zPosition="4" size="400,225" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />
	</screen>
"""
###

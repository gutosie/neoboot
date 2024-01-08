#!/bin/sh
# script gutosie
# here you can add your own command to perform
# line - Checking internet connection by @j00zek thank you
if [ -f /.control_boot_new_image ] ; then
    passwd -d root
    ln -sf "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot" "/NeoBoot"
fi
if [ ! -f `cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location`ImageBoot/.neonextboot ] ; then
        mkdir `cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location`
        /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh
        echo "_________Start -neo.sh- mount point location NEOBOOT_________"
fi
if [ ! -e /usr/bin/enigma2_pre_start.sh ]; then
        /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh
        echo "_________Start -mountpoint.sh- location NEOBOOT_________"	
fi
if [ -f /.control_boot_new_image ] ; then
    break ;
else
    #if [ -f /usr/lib/python2.7 ] ; then
        echo "_____(Checking internet connection)..."
        ping -c 1 github.com 1>/dev/null 2>%1
        if [ $? -gt 0 ]; then
		        echo -n "_____github server unavailable..."
		        echo -n "_____The network has no connection..."
		        echo -n "_____Network RESTART..."
                        echo "_____restart network connection..."
                                /etc/init.d/vuplus-wifi-init.sh
                                /etc/wpa_supplicant/action_wpa.sh
                                /etc/wpa_supplicant/functions.sh
                                /etc/wpa_supplicant/ifupdown.sh
				ifconfig sys0 up
                                /etc/udhcpc.d/50default restart
                                #/etc/init.d/networking restart
                                echo "_____restart network finish..."
				sleep 1
		else
		        echo "github server available..."
		        echo "_____The network has a connection. It is OK..."		        
		fi
    #else
        #break ;
    
    #fi
fi
if [ -f /zImage ] ; then
    rm -r /zImage
fi
if [ -f /%1 ] ; then
    rm -f /%1
fi
if [ -f /home/root/%1 ] ; then
    rm -f /home/root/%1
fi
if [ -f /STARTUP ] ; then
    rm -r /STARTU*
fi
echo "_____[NEOBOOT] used userscript_____ "
exit 0

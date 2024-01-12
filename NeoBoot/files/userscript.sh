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
            echo "...Start -neo.sh- mount point location NEOBOOT..."
    fi
    if [ ! -e /usr/bin/enigma2_pre_start.sh ]; then
            /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh
            echo "...Start -mountpoint.sh- location NEOBOOT..."
    fi
            echo "....................-NEOBOOT-...................."
            echo "...Checking internet connection..."
            ping -c 1 github.com 1>/dev/null 2>%1
            if [ $? -gt 0 ]; then
		            echo "...github server unavailable..."
		            echo "...The network has no connection..."
		            echo "...Network RESTART..."
                            echo "...restart network connection..."
                            /etc/init.d/avahi-daemon stop
                            ifdown wlan3
                            ip addr flush dev wlan3
                            ifdown eth0
                            ip addr flush dev eth0
                            /etc/init.d/networking stop
                            killall -9 udhcpc
                            rm /var/run/udhcpc*
                            /etc/init.d/networking start
                            /etc/init.d/avahi-daemon start
			    ifup wlan3
                            ip -o addr show dev wlan3
                                    echo "...Restart network finish..."
				    echo ".............................."
				    sleep 1
    		else
    		            echo "...github server available..."
		            echo "...The network has a connection. It is OK..."
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
    echo "...NEOBOOT used user script Finish..."
    echo "....................-NEOBOOT-...................."
    echo "............................................"
    exit 0

    

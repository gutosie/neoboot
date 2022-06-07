#!/bin/sh
#
#skrypt instaluje neoboot-a
#
BOXHOSTNAME=$( cat /etc/hostname)
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi
if [ -f /etc/apt/apt.conf ] ; then
    STATUS='/var/lib/dpkg/status'
    OS='DreamOS'
elif [ -f /etc/opkg/opkg.conf ] ; then
   STATUS='/var/lib/opkg/status'
   OS='Opensource'
fi
if [ ! -e /.multinfo ]; then
    [ -e /tmp/neoboot.zip ] && rm -f /tmp/neoboot.zip
    [ -e /tmp/neoboot-main ] && rm -rf /tmp/neoboot-main
    echo ""
    echo "M U L T I B O O T"
    echo ""
    [ $PL ] && echo "Pobieranie archiwum..." || echo "Downloading archive file..."
    echo "*****************************************************"
    URL='https://github.com/gutosie/neoboot/archive/main.zip'
    curl -kLs $URL  -o /tmp/neoboot.zip
    Cel="/usr/lib/enigma2/python/Plugins/Extensions"
    if [ $BOXHOSTNAME = "dm500hd" ] || [ $BOXHOSTNAME = "dm800se" ] || [ $BOXHOSTNAME = "dm800" ] || [ $BOXHOSTNAME = "dm8000" ]; then
        break;
    else
        if [ -e $Cel/NeoBoot/plugin.py ]; then 
           chattr -i /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/plugin.py
        fi
        if [ -e $Cel/NeoBoot/plugin.pyo ]; then 
           chattr -i /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/plugin.pyo
        fi        
        if [ -e /usr/lib/periodon/.activatedmac ]; then 
           chattr -i /usr/lib/periodon/.activatedmac; rm -f /usr/lib/periodon/.activatedmac
        fi
    fi
    cd /tmp/
    #pobieranie
    if [ ! -e /tmp/neoboot.zip ]; then 
       wget --no-check-certificate $URL  
       mv -f /tmp/main.zip /tmp/neoboot.zip  
    fi
    if [ ! -e /tmp/neoboot.zip ]; then 
       fullwget --no-check-certificate $URL  
       mv -f /tmp/main.zip /tmp/neoboot.zip  
    fi
    unzip -qn ./neoboot.zip
    rm -f /tmp/neoboot.zip
    [ -e /tmp/main.zip ] && rm -rf /tmp/main.zip
    if [ $BOXHOSTNAME = "dm500hd" ] || [ $BOXHOSTNAME = "dm800se" ] || [ $BOXHOSTNAME = "dm800" ] || [ $BOXHOSTNAME = "dm8000" ]; then
        cp -af /tmp/neoboot-main/NeoBoot/tmpfiles/runpy/mips_run.py /tmp/neoboot-main/NeoBoot/run.py; rm -r /tmp/neoboot-main/NeoBoot/ubi_reader*;  rm -r /tmp/neoboot-main/NeoBoot/tmpfiles; rm -r /tmp/neoboot-main/NeoBoot/bin/neoinitar*;  rm -r /tmp/neoboot-main/NeoBoot/bin/nanddump*; rm -r /tmp/neoboot-main/NeoBoot/bin/fbcle*; rm -r /tmp/neoboot-main/NeoBoot/bin/neob*; rm -r /tmp/neoboot-main/NeoBoot/bin/nandwrite; rm -r /tmp/neoboot-main/NeoBoot/bin/neoinitmips_vu
    fi
    #kopiowanie
    if [ -e $Cel/NeoBoot/.location ]; then 
       rm -rf $Cel/NeoBoot/.location   
    fi
    [ $PL ] && echo "Instalowanie..." || echo "Instaling..."
    echo "*****************************************************"
    [ -e $Cel/NeoBoot ] && rm -rf $Cel/NeoBoot/* || mkdir -p $Cel/NeoBoot
    mv -f /tmp/neoboot-main/NeoBoot/files/testinout /usr/lib/enigma2/python/Tools/Testinout.py
    mkdir -p /usr/lib/periodon
    mv -f /tmp/neoboot-main/NeoBoot/* $Cel/NeoBoot
    [ -e /tmp/neoboot-main ] && rm -rf /tmp/neoboot-main
    cd $Cel/NeoBoot
    chmod 755 ./bin/*
    chmod 755 ./ex_init.py
    chmod 755 ./files/*.sh
    if [ -e /usr/lib/enigma2/python/Plugins/Extensions/ImageDownloader ]; then 
       rm -r /usr/lib/enigma2/python/Plugins/Extensions/ImageDownloader   
    fi
    touch /tmp/.testneo
    if [ $BOXHOSTNAME = "dm500hd" ] || [ $BOXHOSTNAME = "dm800se" ] || [ $BOXHOSTNAME = "dm800" ] || [ $BOXHOSTNAME = "dm8000" ]; then
        break;
    else
        chmod -R +x ./ubi_reader_arm/*
        chmod -R +x ./ubi_reader_mips/*
        chattr +i /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/plugin.py    
    fi
    if [ $PL ] ; then
      echo ""
      echo "#####################################################"
      echo "#              NEOBOOT ZAINSTALOWANY                #"
      echo "#####################################################"
      echo ""
    else
      echo ""
      echo "#####################################################"
      echo "#     >>> NEOBOOT INSTALLED SUCCESSFULLY <<<        #"
      echo "#####################################################"
      echo ""
    fi
    echo "*******************************************************"
    echo "                N  E  O  B  O  O  T                    "    
    echo "          ----- Restart Enigma2 GUI -----              "
    echo "*******************************************************"
    sleep 2
    if [ $OS = 'DreamOS' ]; then 
        systemctl restart enigma2
    else
        killall -9 enigma2
    fi
else
    if [ $PL ] ; then
      echo ""
      echo "#####################################################"
      echo ">>>>     Błąd!    To nie jest image flash.       <<<<"
      echo ">>>>     Instaluj neoboot-a tylko z Flash.       <<<<"
      echo "#####################################################"
      echo ""
    else
      echo ""
      echo "#####################################################"
      echo ">>>>     Error!   Go back to image flash.        <<<<"
      echo ">>>>     To install NeoBoot go back to Flash.    <<<<"
      echo "#####################################################"
      echo ""
    fi
fi
exit 0 


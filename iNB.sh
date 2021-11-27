#!/bin/sh
#
#skrypt instaluje neoboot-a
#
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi
[ -e /tmp/neoboot.zip ] && rm -f /tmp/neoboot.zip
[ -e /tmp/neoboot-main ] && rm -rf /tmp/neoboot-main
[ $PL ] && echo "Pobieranie archiwum..." || echo "Downloading archive file..."
URL='https://github.com/gutosie/neoboot/archive/main.zip'
curl -kLs $URL  -o /tmp/neoboot.zip
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
#kopiowanie
Cel="/usr/lib/enigma2/python/Plugins/Extensions"
if [ -e $Cel/NeoBoot/.location ]; then 
   rm -rf $Cel/NeoBoot/.location   
fi
[ $PL ] && echo "Instalowanie..." || echo "Instaling..."
[ -e $Cel/NeoBoot ] && rm -rf $Cel/NeoBoot/* || mkdir -p $Cel/NeoBoot
mv -f /tmp/neoboot-main/NeoBoot/files/testinout /usr/lib/enigma2/python/Tools/Testinout.py
mkdir -p /usr/lib/periodon
/usr/lib/periodon/.activatedmac
mv -f /tmp/neoboot-main/NeoBoot/files/neouser /usr/lib/periodon/.activatedmac
mv -f /tmp/neoboot-main/NeoBoot/* $Cel/NeoBoot
[ -e /tmp/neoboot-main ] && rm -rf /tmp/neoboot-main
cd $Cel/NeoBoot
chmod 755 ./bin/*
chmod 755 ./ex_init.py
chmod 755 ./files/*.sh
chmod -R +x ./ubi_reader_arm/*
chmod -R +x ./ubi_reader_mips/*
if [ $PL ] ; then
  echo ""
  echo "#####################################################"
  echo "#          NEOBOOT ZOSTAL ZAINSTALOWANY             #"
  echo "#                                                   #"
  echo "#               ZRESTARTUJ TUNER                    #"
  echo "#####################################################"
  echo ""
else
  echo ""
  echo "#####################################################"
  echo "#          NEOBOOT INSTALLED SUCCESSFULLY           #"
  echo "#                                                   #"
  echo "#            PLEASE RESTART YOUR STB                #"
  echo "#####################################################"
  echo ""
fi
echo "              ----- Restart GUI... -----               "
sleep 5; killall -9 enigma2
exit 0     

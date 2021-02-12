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
URL='https://github.com/gutosie/neoboot/archive/main1.zip'
curl -kLs $URL  -o /tmp/neoboot.zip
cd /tmp/
if [ ! -e /tmp/main.zip ]; then 
   wget $URL  
   mv -f /tmp/main.zip /tmp/neoboot.zip  
fi
unzip -qn ./neoboot.zip
rm -f /tmp/neoboot.zip
[ -e /tmp/main.zip ] && rm -rf /tmp/main.zip
#kopiowanie
[ $PL ] && echo "Instalowanie..." || echo "Instaling..."
Cel="/usr/lib/enigma2/python/Plugins/Extensions"
[ -e $Cel/NeoBoot ] && rm -rf $Cel/NeoBoot/* || mkdir -p $Cel/NeoBoot
mv -f /tmp/neoboot-main/NeoBoot/files/testinout /usr/lib/enigma2/python/Tools/Testinout.py
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
  echo "#          NEOBOOT NIE ZOSTAL ZAINSTALOWANY         #"
  echo "#####################################################"
  echo "#                WERSJA NIE JEST GOTOWA             #"
  echo "#####################################################"
  echo "#####################################################"
  echo "#             SPROBUJ PONOWNIE W INNYM CZASIE       #"
  echo "#####################################################"
  echo ""
else
  echo ""
  echo "#####################################################"
  echo "#          NEOBOOT NOT INSTALLED SUCCESSFULLY       #"
  echo "#####################################################"
  echo "#             VERSION IS NOT READY                  #"
  echo "#####################################################"
  echo "#            TRY AGAIN ANOTHER TIME                 #"
  echo "#####################################################"
  echo ""
fi
exit 0     

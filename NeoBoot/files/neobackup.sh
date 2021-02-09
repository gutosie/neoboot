#!/bin/sh
#script by gutosie

if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi

IMAGE=ImageBoot
LOCATIONBACKUP=CopyNEOBoot
NEOBOOTMOUNT=$( cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location) 
TiME=$(date +"%Y%m%d_%H%M%S")
UPDATEv=$(cat $NEOBOOTMOUNT/ImageBoot/.updateversion)
NB=_NeoBoot_ 
        
if [ ! -e $NEOBOOTMOUNT$LOCATIONBACKUP  ]; then
    mkdir $NEOBOOTMOUNT$LOCATIONBACKUP > /dev/null 2>&1
    /bin/tar -czf $NEOBOOTMOUNT/CopyNEOBoot/Copy_$UPDATEv$NB$TiME.tar.gz /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot*/
    echo " "
    [ $PL ] && echo "Kopia wtyczki neoboot o nazwie Copy_$UPDATEv$NB$TiME.tar.gz utworzono w:"    $NEOBOOTMOUNT$LOCATIONBACKUP"  "  || echo "Copy named Copy_$UPDATEv$NB$TiME.tar.gz was created at location:"    $NEOBOOTMOUNT$LOCATIONBACKUP"  " 
    echo " "     
else        
    /bin/tar -czf $NEOBOOTMOUNT/CopyNEOBoot/Copy_$UPDATEv$NB$TiME.tar.gz /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot*/
    echo " "
    [ $PL ] && echo "Kopia wtyczki o nazwie Copy_$UPDATEv$NB$TiME.tar.gz utworzono w:"    $NEOBOOTMOUNT$LOCATIONBACKUP"  "  || echo "Copy named Copy_$UPDATEv$NB$TiME.tar.gz was created at location:"    $NEOBOOTMOUNT$LOCATIONBACKUP"  " 
    echo " "      
fi
exit 0 
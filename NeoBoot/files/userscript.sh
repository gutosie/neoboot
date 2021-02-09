#!/bin/sh 
# script gutosie 
# here you can add your own command to perform
# line - Checking internet connection by @j00zek thank you    

IMAGEKATALOG=ImageBoot                

if [ -e /.control_boot_new_image ] ; then
    passwd -d root
    ln -sf "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot" "/NeoBoot"
fi


if [ ! -e `cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location`$IMAGEKATALOG/.neonextboot ] ; then
        mkdir `cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location` 
        /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh  
        echo "_(_________Start mountpoint location NEOBOOT_________)"          
fi

echo "_(Checking internet connection)..."
ping -c 1 github.com 1>/dev/null 2>%1 
if [ $? -gt 0 ]; then 
      echo -n "_(github server unavailable, update impossible)\n!!! network restart...!!! )"       
      /etc/init.d/networking stop; 
	  echo "_____(stopping network connection)_____" 
	  sleep 1; 
	  /etc/init.d/networking start; 
	  echo "_____(start network connection)_____" 	  
	  sleep 5
	  
      if [ $? -gt 0 ]; then
          if [ -e /usr/bin/curl ]; then
              cd /tmp; curl -O --ftp-ssl https://raw.githubusercontent.com/gutosie/NeoBoot8/master/ver.txt; 
              cd /
          elif [ -e /usr/bin/wget ]; then
              wget https://raw.githubusercontent.com/gutosie/NeoBoot8/master/ver.txt -O /tmp/ver.txt
              cd /

          fi
          if [ ! -f /tmp/ver.txt ] ; then
              /etc/init.d/networking stop; 
			  echo "_____(stopping network connection)_____" 
              sleep 2; 
              /etc/init.d/networking start;
			  echo "_____(start network connection)_____"
			  
          fi
      fi
      
#      echo "        dns-nameservers 1.1.1.1 " >> /etc/network/interfaces     
else
    echo "_____!!!(github server available)!!!_____"  
fi

if [ -e /%1 ] ; then
    rm -f /%1
fi
if [ -e /home/root/%1 ] ; then
    rm -f /home/root/%1
fi

echo "!!!_____([NEOBOOT] used userscript)_____!!! "  
echo ok 

exit 0 
                                             
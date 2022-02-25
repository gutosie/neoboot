# neoboot
In version 9.49, tests have been added for the Dreambox MIPS receiver. 
OpenPLi recommended in flash. For dreambox only openpli-based images work.
To install NeoBOOT on a receiver with a small amount of flash memory, such as the DM500HD, you need to free up some space by uninstalling the plugins.

recommended vuplus image for flash openpli

recommended other stb image for flash egami or openpli

only install with the command contained here, do not install from other sources of the ipk file type !

Installation of neoboot.  Run the following command in the terminal of a supported tuner 
 
Instalacja neoboot. Uruchom poniższą komendę w terminalu wspieranego tunera

#

opkg update 

opkg install curl 

curl -kLs https://raw.githubusercontent.com/gutosie/neoboot/master/iNB.sh|sh

#

-jeśli w/w polecenie nie zadział próbujemy polecenia:

-if the command doesn't work, try the command:


cd /tmp; wget --no-check-certificate https://raw.githubusercontent.com/gutosie/neoboot/master/iNB.sh;chmod 755 ./iNB.sh;sh ./iNB.sh; rm ./iNB.sh; cd 

#

-jeśli w/w polecenie nie zadział próbujemy następne polecenia:

-if the command doesn't work, try the command:

cd /tmp; fullwget --no-check-certificate https://raw.githubusercontent.com/gutosie/neoboot/master/iNB.sh;chmod 755 ./iNB.sh; sh ./iNB.sh; rm ./iNB.sh; cd

#

![2AC5694061764352826110151BF37430 (1)](https://user-images.githubusercontent.com/4014580/147877740-0d115fa1-ba09-4527-9dfb-ee6585651a66.jpg)
![nep_skin](https://user-images.githubusercontent.com/4014580/145280636-0491cfa8-691f-4aec-b716-3248d5dfef4b.jpg)
![neoboot](https://user-images.githubusercontent.com/4014580/145025575-966b82bb-d8b5-48ba-84bd-f2fc41ce8758.jpg)
![neoboot_menu](https://user-images.githubusercontent.com/4014580/145025978-4702fab0-853d-4f9c-b1b3-f4a8fb51fcb1.jpg)
![neoboot_install](https://user-images.githubusercontent.com/4014580/145026311-b9a19c79-81af-4ded-b79a-56f73f30b3fb.jpg)


List supported tuners is in stbinfo.cfg file. 

If your stb is not in list, so contact author neoboot and give me the name of device hostname your stb.


UWAGA!!! 
 Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 

Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialności za skutki użytkowania tego programu oraz za wykorzystanie zawartych tu informacji.

Instalację i modyfikacje przeprowadzasz na wlasne ryzyko!!! Przed instalacją lub aktualizacją Neoboot przeczytaj uważnie wszystkie informacje zawarte tu i w wtyczce. !

Dziękuję wszystkim kolegom wpierającym projekt neoboot.

pozdrawiam gutosie

CAUTION!!!
  Redistribution of the program version and making modifications is ALLOWED as long as this copyright notice is preserved.

The author accepts NO responsibility for any consequences of using this program or the use of the information contained herein.

You carry out installation and modification at your own risk !!! Before installing or updating Neoboot, carefully read all the information contained here and in the plugin. !!

Thanks to all colleagues who support the neoboot project.

greetings gutosie

    ----------------Free donate----------------   
                    ¯\_(ツ)_/¯ 
*    Donate to the project
*    Spende
*    Donaco
*    Darowizna
*    Пожертвование    
*    Bağış
*    Donación  
*    Darowizna
*    - Access to the latest version 
*    - Online support 

More information email 
If you want to support the neoboot project, you can do so by contacting us by e-mail:         
krzysztofgutosie@gmail.com    

                    ¯\_(ツ)_/¯ 
    ----------------Free donate----------------   

    We thank you for any help                 
    Have fun !!!


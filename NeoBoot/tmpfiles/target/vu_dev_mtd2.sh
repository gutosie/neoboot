#!/bin/sh
#script - gutosie

PATH=/sbin:/bin:/usr/sbin:/usr/bin

if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi

if [ -f /proc/stb/info/vumodel ];  then  
    VUMODEL=$( cat /proc/stb/info/vumodel )     
fi

if [ -f /proc/stb/info/boxtype ];  then
    BOXTYPE=$( cat /proc/stb/info/boxtype )
fi

if [ -f /proc/stb/info/chipset ];  then
    CHIPSET=$( cat /proc/stb/info/chipset )
fi

if [ -f /tmp/zImage.ipk ];  then
    rm -f /tmp/zImage.ipk
fi

if [ -f /tmp/zImage ];  then
    rm -f /tmp/zImage
fi

KERNEL=`uname -r`
IMAGE=ImageBoot
IMAGENEXTBOOT=/ImageBoot/.neonextboot
NEOBOOTMOUNT=$( cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location)
BOXHOSTNAME=$( cat /etc/hostname)
UPLOAD=ImagesUpload
NandWrite=/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nandwrite

if [ -f /tmp/check_nandwrite ];  then
    CHECK_NANDWRITE=$( cat /tmp/check_nandwrite)
else
    CHECK_NANDWRITE=error
fi

if [ -f $NEOBOOTMOUNT$IMAGENEXTBOOT ]; then
  TARGET=`cat $NEOBOOTMOUNT$IMAGENEXTBOOT`
else
  TARGET=Flash
fi

if  [ $BOXHOSTNAME = "vusolo2" ] || [ $BOXHOSTNAME = "vuduo2" ] || [ $BOXHOSTNAME = "vusolose" ] || [ $BOXHOSTNAME = "vuzero" ]; then
    if [ -f /proc/stb/info/vumodel ] || [ ! -e /proc/stb/info/boxtype ] ; then
        if [ $TARGET = "Flash" ]; then
                if [ -e /.multinfo ]; then
                    if [ -e $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz ] ; then
                        [ $PL ] && echo "Kasowanie kernel z /dev/mtd2..." || echo "Erase kernel from  /dev/mtd2"
                        sleep 2
                        cp -f $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz /tmp/vmlinux.gz 
                        [ $PL ] && echo "Wgrywanie kernel do /dev/mtd2..." || echo "Writing kernel to /dev/mtd2"
                        sleep 2
                        if [ $CHECK_NANDWRITE = "nandwrite" ] ; then
                            set -e
                                if [ "x$D" == "x" ]; then
                                    if [ -f /tmp/vmlinux.gz ] ; then
                                        flash_eraseall /dev/mtd2 > /dev/null 2>&1
                                        nandwrite -p /dev/mtd2 /tmp/vmlinux.gz > /dev/null 2>&1
                                        [ $PL ] && echo "nandwrite - kernel wgrany" || echo "Writing kernel to /dev/mtd2"
                                    else
                                        [ $PL ] && echo "W lokalizacji /tmp/ nie ma pliku vmlinux.gz" || echo "No found vmlinux.gz in  /tmp/"
                                    fi
                                fi
                                true                         
                        else
                            echo "Writing kernel /dev/mtd2 " $TARGET                            
                            set -e
                                if [ "x$D" == "x" ]; then
                                    if [ -f /tmp/vmlinux.gz ] ; then
                                        flash_eraseall /dev/mtd2 > /dev/null 2>&1
                                        $NandWrite -p /dev/mtd2 /tmp/vmlinux.gz > /dev/null 2>&1
                                        [ $PL ] && echo "nandwrite - kernel wgrany" || echo "Writing kernel to /dev/mtd2"
                                    else
                                        [ $PL ] && echo "W lokalizacji /tmp/ nie ma pliku vmlinux.gz" || echo "No found vmlinux.gz in  /tmp/"
                                    fi
                                fi
                                true                              
                        fi
                    fi
                fi
        else
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET
                                else
                                    [ $PL ] && echo "Kasowanie kernel z /dev/mtd2... " || echo "Erase kernel from  /dev/mtd2 "
                                    sleep 2
                                    
                                    cp -f $NEOBOOTMOUNT$IMAGE/$TARGET/boot/$BOXHOSTNAME.vmlinux.gz /tmp/vmlinux.gz
                                    
                                    [ $PL ] && echo "Wgrywanie kernel do /dev/mtd2... " || echo "Writing kernel to from  /dev/mtd2 "
                                    sleep 2
                                    if [ $CHECK_NANDWRITE = "nandwrite" ] ; then
                                        echo "writing kernel flash - BOOT IMAGE "
                                        set -e
                                            if [ "x$D" == "x" ]; then
                                                if [ -f /tmp/vmlinux.gz ] ; then
                                                    flash_eraseall /dev/mtd2 > /dev/null 2>&1
                                                    nandwrite -p /dev/mtd2 /tmp/vmlinux.gz > /dev/null 2>&1
                                                    [ $PL ] && echo "nandwrite - kernel zmieniony " || echo "Writing kernel to /dev/mtd2 "
                                                else
                                                    [ $PL ] && echo "W lokalizacji /tmp/ nie ma pliku vmlinux.gz" || echo "No found vmlinux.gz in  /tmp/"
                                                fi
                                            fi
                                            true           
                                    else
                                        echo "writing kernel mtd1 " $TARGET
                                        set -e
                                            if [ "x$D" == "x" ]; then
                                                if [ -f /tmp/vmlinux.gz ] ; then
                                                    flash_eraseall /dev/mtd2 > /dev/null 2>&1
                                                    $NandWrite -p /dev/mtd2 /tmp/vmlinux.gz > /dev/null 2>&1
                                                    [ $PL ] && echo "nandwrite kernel wczytany" || echo "Writing kernel to /dev/mtd2"
                                                else
                                                    [ $PL ] && echo "W lokalizacji /tmp/ nie ma pliku vmlinux.gz " || echo "No found vmlinux.gz in  /tmp/ "
                                                fi
                                            fi
                                            true
                                    fi
                                fi
                        else
                                    [ $PL ] && echo "Kasowanie kernel z /dev/mtd2... " || echo "Erase kernel from  /dev/mtd2 "
                                    sleep 2
                                    cp -f $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz /tmp/vmlinux.gz
                                    [ $PL ] && echo "Zapis kernel do /dev/mtd2... " || echo "Writing kernel to from  /dev/mtd2 "
                                    sleep 2
                                    if [ $CHECK_NANDWRITE = "nandwrite" ] ; then
                                        echo "writing kernel flash - IMAGE BOOT "
                                        set -e
                                            if [ "x$D" == "x" ]; then
                                                if [ -f /tmp/vmlinux.gz ] ; then
                                                    flash_eraseall /dev/mtd2 > /dev/null 2>&1
                                                    nandwrite -p /dev/mtd2 /tmp/vmlinux.gz > /dev/null 2>&1
                                                    [ $PL ] && echo "Kernel zmieniony " || echo "Writing kernel to /dev/mtd2 "
                                                else
                                                    [ $PL ] && echo "W lokalizacji /tmp/ nie ma pliku vmlinux.gz " || echo "No found vmlinux.gz in  /tmp/ "
                                                fi
                                            fi
                                            true
                                    else
                                        echo "writing kernel mtd1 " $TARGET
                                        set -e
                                            if [ "x$D" == "x" ]; then
                                                if [ -f /tmp/vmlinux.gz ] ; then
                                                    flash_eraseall /dev/mtd2 > /dev/null 2>&1
                                                    $NandWrite -p /dev/mtd2 /tmp/vmlinux.gz > /dev/null 2>&1
                                                    [ $PL ] && echo "/dev/mtd2 kernel wgrany " || echo "Writing kernel to /dev/mtd2 "
                                                else
                                                    [ $PL ] && echo "W lokalizacji /tmp/ nie ma pliku vmlinux.gz " || echo "No found vmlinux.gz in  /tmp/ "
                                                fi
                                            fi
                                            true
                                    fi
                        fi
        fi        
    fi
    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
    echo "NEOBOOT is booting image " $TARGET
    echo "Used Kernel: " $TARGET   > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel
    echo "CHIPSET: " $CHIPSET " BOX NAME: "$BOXHOSTNAME" MODEL: "$BOXHOSTNAME" "
    echo "$TARGET "  > $NEOBOOTMOUNT/ImageBoot/.neonextboot
    echo "...............Shutdown Now..............."
    sleep 5
    reboot -d -f 
else
                    ln -sfn /sbin/init.sysvinit /sbin/init
                    echo "CHIPSET: " $CHIPSET " BOX NAME: "$BOXHOSTNAME" MODEL: "$BOXHOSTNAME" "
                    echo "$TARGET "  > $NEOBOOTMOUNT/ImageBoot/.neonextboot
                    [ $PL ] && echo "Ten model stb nie jest wpierany" || echo "This stb model is not supported."
                    [ $PL ] && echo "Wspierane modele: vusolo2, vuduo2, vusolose, vuzero " || echo "Supported model: vusolo2, vuduo2, vusolose, vuzero "              
                    exit 0
fi
exit 0

#!/bin/sh
#script - gutosie
#Clarke-Tech & Xtrend

PATH=/sbin:/bin:/usr/sbin:/usr/bin 
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
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

if [ -f /usr/sbin/nandwrite ];  then
    NandWrite=/usr/sbin/nandwrite
else  
    NandWrite=/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nandwrite   
fi

#dd if=/media/hdd/ImagesUpload/.kernel/kernel.bin of=/dev/mtdblock1
#/usr/sbin/nandwrite -p /dev/mtd1 /media/hdd/ImagesUpload/.kernel/kernel.bin
#/usr/sbin/nandwrite -p /dev/mtd1 /media/hdd/ImagesUpload/.kernel/et5x00.vmlinux.gz

if [ -f $NEOBOOTMOUNT$IMAGENEXTBOOT ]; then
  TARGET=`cat $NEOBOOTMOUNT$IMAGENEXTBOOT`
else
  TARGET=Flash              
fi
                   
if [ $BOXHOSTNAME = "et5x00" ] ; then
    if [ ! -e /proc/stb/info/vumodel ] || [ -f /proc/stb/info/boxtype ] ; then
        if [ $TARGET = "Flash" ]; then                    
                if [ -e /.multinfo ]; then                                                
                    if [ -e $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz ] ; then
                        [ $PL ] && echo "Kasowanie kernel z /dev/mtd1..." || echo "Erase kernel from  /dev/mtd1"
                        sleep 2                                
                        flash_eraseall /dev/mtd1 > /dev/null 2>&1
                        [ $PL ] && echo "Wgrywanie kernel do /dev/mtd1..." || echo "Writing kernel to from  /dev/mtd1"  
                        sleep 2
                                    
                        if [ -e /dev/mtdblock1 ] ; then
                            echo "writing kernel flash " $TARGET
                            dd if=$NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz of=/dev/mtdblock1 
                        else
                            $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1 
                            $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$UPLOAD/.kernel/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1 
                        fi
                                    
                    fi 
                fi
                update-alternatives --remove vmlinux vmlinux-`uname -r` || true                                          
                echo "NEOBOOT is booting image " $TARGET
                echo "...............Shutdown Now..............."
                sleep 5                                
                echo "Used Kernel: " $TARGET > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel
                reboot -d -f                
        else                  	    
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image from " $TARGET                                    
                                else                                    
                                    [ $PL ] && echo "Kasowanie kernel z /dev/mtd1..." || echo "Erase kernel from  /dev/mtd1"                                   
                                    sleep 2
                                    flash_eraseall /dev/mtd1 > /dev/null 2>&1
                                    [ $PL ] && echo "Wgrywanie kernel do /dev/mtd1..." || echo "Writing kernel to from  /dev/mtd1"                                                                      
                                    sleep 2
                                    if [ -e /dev/mtdblock1 ] ; then
                                        echo "writing kernel mtd1 " $TARGET 
                                        dd if=/media/hdd/ImageBoot/$TARGET/boot/$BOXHOSTNAME.vmlinux.gz of=/dev/mtdblock1
                                    else
                                        $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$IMAGE/$TARGET/boot/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1
                                    fi
                                      
                                    update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                                    echo "NEOBOOT is booting image" $TARGET
                                    echo "Used Kernel: " $TARGET   > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel
                                fi
                        else
                                    [ $PL ] && echo "Kasowanie kernel z /dev/mtd1..." || echo "Erase kernel from  /dev/mtd1"                                   
                                    sleep 2
                                    flash_eraseall /dev/mtd1 > /dev/null 2>&1 
                                    [ $PL ] && echo "SRANIE W BANIE " || echo "Writing kernel to from  /dev/mtd1"
                                    sleep 2
                                    if [ -f /dev/mtdblock1 ]; then
                                        echo "writing kernel mtdblock1 " $TARGET
                                        dd if=$NEOBOOTMOUNT$IMAGE/$TARGET/boot/$BOXHOSTNAME.vmlinux.gz of=/dev/mtdblock1
                                    else
                                        $NandWrite -p /dev/mtd1 $NEOBOOTMOUNT$IMAGE/$TARGET/boot/$BOXHOSTNAME.vmlinux.gz > /dev/null 2>&1
                                    fi                                      
                        fi
                        update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                        echo "NEOBOOT is booting image " $TARGET
                        echo "Used Kernel: " $TARGET   > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel                                         
                        echo "...............Shutdown Now..............." 
                        sleep 5
                        reboot -d -f
        fi
    fi                        
else
                    ln -sfn /sbin/init.sysvinit /sbin/init
                    echo "CHIPSET: " $CHIPSET " BOX NAME: "$BOXHOSTNAME" MODEL: "$BOXHOSTNAME" "
                    echo "$TARGET "  > $NEOBOOTMOUNT/ImageBoot/.neonextboot
                    [ $PL ] && echo "Ten model stb nie jest wpierany" || echo "This stb model is not supported." 
                    [ $PL ] && echo "Wspierane modele: vuduo, vusolo, vuuno, vuultimo" || echo "Supported model: vuduo, vusolo, vuuno, vuultimo "                     
                    exit 0
fi
exit 0

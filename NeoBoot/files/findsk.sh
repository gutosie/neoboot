args=`cat /proc/cmdline`
for line in ${args};
do
     key=${line%%=*}
     value=${line#*=}
     if [ "$key" == "root" ]; then
          ln -sf "$value" /media/root
     fi
done
sleep 2
for line in ${args};
do
     key=${line%%=*}
     value=${line#*=}
     if [ "$key" == "kernel" ]; then
          ln -sf "$value" /dev/kernel
     fi
done
sleep 2
  
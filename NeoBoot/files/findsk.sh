args=`cat /proc/cmdline`
for line in ${args};
do
     key=${line%%=*}
     value=${line#*=}
     if [ "$key" == "root" ]; then
          ln -sf "$value" /tmp/root
     fi
     if [ "$key" == "kernel" ]; then
          ln -sf "$value" /dev/kernel
     fi
done
sleep 2
  

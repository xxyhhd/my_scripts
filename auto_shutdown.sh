for vm in `virsh list --name`;do virsh shutdown $vm; done
sleep 60
init 0

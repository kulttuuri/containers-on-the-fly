

### Using custom port for file sharing because we have confligt with other ports:
sudo nano /etc/default/nfs-kernel-server

RPCNFSDARGS="-p 20490"
# Custom NFS server port
RPCMOUNTDOPTS="-p 20491"
# Custom mountd port
STATDARGS="--port 20492 --outgoing-port 20493"
# Custom statd ports
RPCMOUNTDOPTS="--manage-gids"

## Also change from file: 
sudo nano /etc/services
change 2049 => 20490, in both tcp and udp
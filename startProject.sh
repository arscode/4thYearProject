

#start sflow first, then either pox or mininet first
#need to run mininet as root


#sudo -u james gnome-terminal -e /home/james/mininet/sflow-rt/start.sh
#make sure these components are in pox/ext
/home/james/pox/pox.py Main Monitor forwarding.l3_learning spanning_tree log.level --ERROR


#sudo -u james gnome-terminal -e /home/james/project/version2/startNetwork.py #also registers sflow agents. make this a tree

 


#!/usr/bin/python
'''
SDN-based-QoS-Enhanced-Virtualization-in-Service-Provider-Networks
EE-297B project, code by Sohail Virani, Goutham Prasanna, Nitish Gupta. 

'''
 
#Custom service provider backbone Topolgy
import subprocess
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.node import Host
from mininet.node import OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

def my_network():
    net= Mininet(topo=None, build=False, controller=RemoteController, link=TCLink)

    #Add Controller
    info( '***Adding Controller\n' )
    poxController1 = net.addController('c0', controller=RemoteController, ip="127.0.0.1", port=6633)

    # Create switch nodes
    for i in range(4):
	sconfig = {'dpid': "%016x" % (i+1)}
	net.addSwitch('s%d' % (i+1), **sconfig)
	for j in range(3):
		sconfig = {'dpid': "%016x" % ((i+1)*10+(j+1))}
		net.addSwitch('s%d%d' % (i+1, j+1), **sconfig)
    net.addSwitch('scc1',dpid="%016x" % 17)
    net.addSwitch('scc2',dpid="%016x" % 18)
    net.addSwitch('sdc1',dpid="%016x" % 19)
    
    
    # Create host nodes
    hconfig = {'inNamespace':True}
    for i in range(24):
	net.addHost('h%d' % (i+1), **hconfig)
    net.addHost('cc51', **hconfig)
    net.addHost('cc52', **hconfig)
    net.addHost('dc50', **hconfig)
	

    # Add switch links
    net.addLink('s1', 's11', cls=TCLink, use_htb=True)
    net.addLink('s1', 's12', cls=TCLink, use_htb=True)
    net.addLink('s1', 's13', cls=TCLink, use_htb=True)
    net.addLink('s11', 's12', cls=TCLink, use_htb=True)
    net.addLink('s12', 's13', cls=TCLink, use_htb=True)

    net.addLink('s2', 's21', cls=TCLink, use_htb=True)
    net.addLink('s2', 's22', cls=TCLink, use_htb=True)
    net.addLink('s2', 's23', cls=TCLink, use_htb=True)
    net.addLink('s21', 's22', cls=TCLink, use_htb=True)
    net.addLink('s22', 's23', cls=TCLink, use_htb=True)

    net.addLink('s3', 's31', cls=TCLink, use_htb=True)
    net.addLink('s3', 's32', cls=TCLink, use_htb=True)
    net.addLink('s3', 's33', cls=TCLink, use_htb=True)
    net.addLink('s31', 's32', cls=TCLink, use_htb=True)
    net.addLink('s32', 's33', cls=TCLink, use_htb=True)

    net.addLink('s4', 's41', cls=TCLink, use_htb=True)
    net.addLink('s4', 's42', cls=TCLink, use_htb=True)
    net.addLink('s4', 's43', cls=TCLink, use_htb=True)
    net.addLink('s41', 's42', cls=TCLink, use_htb=True)
    net.addLink('s42', 's43', cls=TCLink, use_htb=True)

    net.addLink('s1', 'sdc1', cls=TCLink, use_htb=True)
    net.addLink('s1', 'scc1', cls=TCLink, use_htb=True)
    net.addLink('s2', 'sdc1', cls=TCLink, use_htb=True)
    net.addLink('s2', 'scc1', cls=TCLink, use_htb=True)
    net.addLink('s3', 'sdc1', cls=TCLink, use_htb=True)
    net.addLink('s3', 'scc2', cls=TCLink, use_htb=True)
    net.addLink('s4', 'sdc1', cls=TCLink, use_htb=True)
    net.addLink('s4', 'scc2', cls=TCLink, use_htb=True)
   
    net.addLink('scc1', 'sdc1', cls=TCLink, use_htb=True)
    net.addLink('scc2', 'sdc1', cls=TCLink, use_htb=True)
	

    # Add host links
    net.addLink('h1', 's11', cls=TCLink, use_htb=True)
    net.addLink('h2', 's11', cls=TCLink, use_htb=True)
    net.addLink('h3', 's12', cls=TCLink, use_htb=True)
    net.addLink('h4', 's12', cls=TCLink, use_htb=True)
    net.addLink('h5', 's13', cls=TCLink, use_htb=True)
    net.addLink('h6', 's13', cls=TCLink, use_htb=True)

    net.addLink('h7', 's21', cls=TCLink, use_htb=True)
    net.addLink('h8', 's21', cls=TCLink, use_htb=True)
    net.addLink('h9', 's22', cls=TCLink, use_htb=True)
    net.addLink('h10', 's22', cls=TCLink, use_htb=True)
    net.addLink('h11', 's23', cls=TCLink, use_htb=True)
    net.addLink('h12', 's23', cls=TCLink, use_htb=True)

    net.addLink('h13', 's31', cls=TCLink, use_htb=True)
    net.addLink('h14', 's31', cls=TCLink, use_htb=True)
    net.addLink('h15', 's32', cls=TCLink, use_htb=True)
    net.addLink('h16', 's32', cls=TCLink, use_htb=True)
    net.addLink('h17', 's33', cls=TCLink, use_htb=True)
    net.addLink('h18', 's33', cls=TCLink, use_htb=True)

    net.addLink('h19', 's41', cls=TCLink, use_htb=True)
    net.addLink('h20', 's41', cls=TCLink, use_htb=True)
    net.addLink('h21', 's42', cls=TCLink, use_htb=True)
    net.addLink('h22', 's42', cls=TCLink, use_htb=True)
    net.addLink('h23', 's43', cls=TCLink, use_htb=True)
    net.addLink('h24', 's43', cls=TCLink, use_htb=True)

    net.addLink('cc51', 'scc1', cls=TCLink, use_htb=True)
    net.addLink('dc50', 'sdc1', cls=TCLink, use_htb=True)
    net.addLink('cc52', 'scc2', cls=TCLink, use_htb=True)

    net.build()

    info( '***Starting network\n' )
    net.start()

    info( '***Configuring the links\n' )
    cli_obj = CLI(net,script='/home/mininet/new_folder/mproject/mod_qos.py')

    info( '***Entering command prompt\n' )
    CLI(net)
    
    info( '***Stopping network\n' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    my_network()
'''
SDN-based-QoS-Enhanced-Virtualization-in-Service-Provider-Networks
EE-297B project, code by Sohail Virani, Goutham Prasanna, Nitish Gupta. 

'''

#Slicing with Spanning Tree Protocol to prevent loops
from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str, str_to_bool, str_to_dpid
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.recoco import Timer
from collections import namedtuple
import os, time

log = core.getLogger()


class SlicedNet (object):
    def __init__(self):
	core.openflow.addListeners(self)
	core.openflow_discovery.addListeners(self)

        # Adjacency map to navigate through a route.  [sw1][sw2] -> port from sw1 to sw2
        self.adjacency = defaultdict(lambda:defaultdict(lambda:None))
	
	# Layer2 lookup. MAC table entries for all switches.
	self._macToPort = defaultdict(dict)
	
	# Layer1 lookup. Active Port entries for all switches.
	self._portTable = defaultdict(list)


    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
	ports = []
	for port in event.ofp.ports:
		self._macToPort[dpid][port.hw_addr] = port.port_no
		ports.append(port.port_no)
	self._portTable[dpid] = sorted(ports)
	log.debug("Switch {} has come up.".format(dpid))

    def _handle_ConnectionDown(self, event):
	dpid = dpidToStr(event.dpid)
	del self._macToPort[dpid]
        log.debug("Switch {} is going down.".format(dpid))

    def _handle_LinkEvent(self, event):
        l = event.link
        sw1 = dpid_to_str(l.dpid1)
        sw2 = dpid_to_str(l.dpid2)

        log.debug ("link added: %s[%d] <-> %s[%d]",
                   sw1, l.port1,
                   sw2, l.port2) 

        self.adjacency[sw1][sw2] = l.port1
        self.adjacency[sw2][sw1] = l.port2

    def macTable(self, dpid= None):
        try:
	    return self._macToPort[dpid]
	except:
	    return None
    
    def portTable(self, dpid=None):
	try:
	    return self._portTable[dpid]
	except:
	    return None
    

def launch(stp=False):
    pox.openflow.discovery.launch()

    # Run spanning tree so that we can deal with topologies with loops
    if str_to_bool(stp):
	pox.openflow.spanning_tree.launch(no_flood = True, hold_down = True)

    '''
    Starting the Network Slicing module
    '''
    core.registerNew(SlicedNet)
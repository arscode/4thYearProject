"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class DiamondTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        oneSwitch = self.addSwitch( 's1' )
        twoSwitch = self.addSwitch( 's2' )
        threeSwitch = self.addSwitch('s3')
        fourSwitch = self.addSwitch('s4')

        # Add links
        self.addLink( leftHost, fourSwitch )
        self.addLink( fourSwitch, oneSwitch )
        self.addLink(fourSwitch, twoSwitch )
        self.addLink(oneSwitch, threeSwitch)
        self.addLink(twoSwitch, threeSwitch)
        self.addLink(threeSwitch, rightHost)

topos = { 'mytopo': ( lambda: DiamondTopo() ) }

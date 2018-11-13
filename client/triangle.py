"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        leftSwitch = self.addSwitch( 's3' )
        rightSwitch = self.addSwitch( 's4' )

        # Add links
        self.addLink( leftHost, leftSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( rightSwitch, rightHost )

class Triangle(Topo):
    def __init__(self):
        Topo.__init__( self )
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        Switch = self.addSwitch( 's1' )

        self.addLink( leftHost, Switch )
        self.addLink( leftHost, rightHost )
        self.addLink( Switch, rightHost )

class Square(Topo):
    def __init__(self):
        Topo.__init__( self )
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        upSwitch = self.addSwitch( 's1' )
        downSwitch = self.addSwitch( 's2' )

        self.addLink( leftHost, upSwitch )
        self.addLink( leftHost, downSwitch )
        self.addLink( rightHost, upSwitch )
        self.addLink( rightHost, downSwitch )

class Proper_Triangle(Topo):
    def __init__(self):
        Topo.__init__( self )
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        upHost = self.addHost( 'h3' )
        upSwitch = self.addSwitch( 's1' )
        downSwitch = self.addSwitch( 's2' )

        self.addLink( leftHost, upSwitch )
        self.addLink( leftHost, downSwitch )
        self.addLink( rightHost, upSwitch )
        self.addLink( rightHost, downSwitch )
        self.addLink( upHost, downSwitch )

class Last_Hope(Topo):
    def __init__(self):
        Topo.__init__( self )
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        upHost = self.addHost( 'h3' )
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )

        self.addLink( leftHost, leftSwitch )
        self.addLink( rightHost, rightSwitch )
        self.addLink( leftSwitch, rightSwitch )
        self.addLink( upHost, leftSwitch )
        self.addLink( upHost, rightSwitch )

class Really_Last_Hope(Topo):
    def __init__(self):
        Topo.__init__( self )
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        upHost = self.addHost( 'h3' )
        leftSwitch = self.addSwitch( 's1' )
        rightSwitch = self.addSwitch( 's2' )
        downSwitch = self.addSwitch( 's3' )

        self.addLink( leftHost, leftSwitch )
        self.addLink( rightHost, rightSwitch )
        self.addLink( upHost, leftSwitch )
        self.addLink( upHost, rightSwitch )
        self.addLink( leftHost, downSwitch )
        self.addLink( rightHost, downSwitch )  
        #py h3.intf('h3-eth1').setIP('10.0.0.4/24')   

topos = { 'mytopo': ( lambda: MyTopo() ) , 'triangle': ( lambda: Triangle() ), 'square': ( lambda: Square() ), 'proper_triangle': ( lambda: Proper_Triangle() ), 'last_hope': ( lambda: Last_Hope() ), 'really_last_hope': ( lambda: Really_Last_Hope() )}


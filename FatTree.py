

from mininet.topo import Topo

class FatTree(Topo):

    def __init__(self):
        Topo.__init__(self)

        #add core switches
        CoreSwitchOne = self.addSwitch('s1')
        CoreSwitchTwo = self.addSwitch('s2')
        CoreSwitchThree = self.addSwitch('s3')
        CoreSwitchFour = self.addSwitch('s4')

        #add aggregate switches
        AggregateSwitchOne = self.addSwitch('s5')
        AggregateSwitchTwo = self.addSwitch('s6')
        AggregateSwitchThree = self.addSwitch('s7')
        AggregateSwitchFour = self.addSwitch('s8')
        AggregateSwitchFive = self.addSwitch('s9')
        AggregateSwitchSix = self.addSwitch('s10')
        AggregateSwitchSeven = self.addSwitch('s11')
        AggregateSwitchEight = self.addSwitch('s12')

        #add edge switches
        EdgeSwitchOne = self.addSwitch('s13')
        EdgeSwitchTwo = self.addSwitch('s14')
        EdgeSwitchThree = self.addSwitch('s15')
        EdgeSwitchFour = self.addSwitch('s16')
        EdgeSwitchFive = self.addSwitch('s17')
        EdgeSwitchSix = self.addSwitch('s18')
        EdgeSwitchSeven = self.addSwitch('s19')
        EdgeSwitchEight = self.addSwitch('s20')

        #add hosts
        HostOne = self.addHost('h1')
        HostTwo = self.addHost('h2')
        HostThree = self.addHost('h3')
        HostFour = self.addHost('h4')
        HostFive = self.addHost('h5')
        HostSix = self.addHost('h6')
        HostSeven = self.addHost('h7')
        HostEight = self.addHost('h8')

        #add core - aggregate links
        self.addLink(CoreSwitchOne,AggregateSwitchOne)
        self.addLink(CoreSwitchOne,AggregateSwitchThree)
        self.addLink(CoreSwitchOne,AggregateSwitchFive)
        self.addLink(CoreSwitchOne,AggregateSwitchSeven)

        self.addLink(CoreSwitchTwo,AggregateSwitchTwo)
        self.addLink(CoreSwitchTwo,AggregateSwitchFour)
        self.addLink(CoreSwitchTwo,AggregateSwitchSix)
        self.addLink(CoreSwitchTwo,AggregateSwitchEight)

        self.addLink(CoreSwitchThree,AggregateSwitchOne)
        self.addLink(CoreSwitchThree,AggregateSwitchThree)
        self.addLink(CoreSwitchThree,AggregateSwitchFive)
        self.addLink(CoreSwitchThree,AggregateSwitchSeven)

        self.addLink(CoreSwitchFour,AggregateSwitchTwo)
        self.addLink(CoreSwitchFour,AggregateSwitchFour)
        self.addLink(CoreSwitchFour,AggregateSwitchSix)
        self.addLink(CoreSwitchFour,AggregateSwitchEight)
        self.addLink(AggregateSwitchOne,EdgeSwitchOne)
        self.addLink(AggregateSwitchOne,EdgeSwitchTwo)
        self.addLink(AggregateSwitchTwo,EdgeSwitchOne)
        self.addLink(AggregateSwitchTwo,EdgeSwitchTwo)
        

        self.addLink(AggregateSwitchThree,EdgeSwitchThree)
        self.addLink(AggregateSwitchThree,EdgeSwitchFour)
        self.addLink(AggregateSwitchFour,EdgeSwitchThree)
        self.addLink(AggregateSwitchFour,EdgeSwitchFour)

        self.addLink(AggregateSwitchFive,EdgeSwitchFive)
        self.addLink(AggregateSwitchFive,EdgeSwitchSix)
        self.addLink(AggregateSwitchSix,EdgeSwitchFive)
        self.addLink(AggregateSwitchSix,EdgeSwitchSix)

        self.addLink(AggregateSwitchSeven,EdgeSwitchSeven)
        self.addLink(AggregateSwitchSeven,EdgeSwitchEight)
        self.addLink(AggregateSwitchEight,EdgeSwitchSeven)
        self.addLink(AggregateSwitchEight,EdgeSwitchEight)

        #add edge-host links
        self.addLink(EdgeSwitchOne,HostOne)
        self.addLink(EdgeSwitchTwo,HostTwo)
        self.addLink(EdgeSwitchThree,HostThree)
        self.addLink(EdgeSwitchFour,HostFour)
        self.addLink(EdgeSwitchFive,HostFive)
        self.addLink(EdgeSwitchSix,HostSix)
        self.addLink(EdgeSwitchSeven,HostSeven)
        self.addLink(EdgeSwitchEight,HostEight)
        


topos = { 'mytopo': ( lambda: FatTree() ) }
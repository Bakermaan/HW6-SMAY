# region imports
import numpy as np
import math
from scipy.optimize import fsolve
import random as rnd
# endregion

# region class definitions
class Fluid():
    #region constructor
    def __init__(self, mu=0.00089, rho=1000):
        '''
        default properties are for water
        :param mu: dynamic viscosity in Pa*s -> (kg*m/s^2)*(s/m^2) -> kg/(m*s)
        :param rho: density in kg/m^3
        '''
        self.mu= # $JES MISSING CODE$  # simply make a copy of the value in the argument as a class property
        self.rho= # $JES MISSING CODE$  # simply make a copy of the value in the argument as a class property
        self.nu= #JES MISSING CODE$ # calculate the kinematic viscosity in units of m^2/s
    #endregion
class Node():
    #region constructor
    def __init__(self, Name='a', Pipes=[], ExtFlow=0):
        '''
        A node in a pipe network.
        :param Name: name of the node
        :param Pipes: a list of pipes connected to this node
        :param ExtFlow: any external flow into (+) or out (-) of this node in L/s
        '''
        self.name=Name
        self.pipes=Pipes
        self.extFlow=ExtFlow
    #endregion

    #region methods/functions
    def getNetFlowRate(self):
        '''
        Calculates the net flow rate into this node in L/s
        # :return:
        '''
        Qtot=#$JES MISSING CODE$  #count the external flow first
        for p in self.pipes:
            #retrieves the pipe flow rate (+) if into node (-) if out of node.  see class for pipe.
            Qtot+=p.getFlowIntoNode(self.name)
        return Qtot
    #endregion
class Loop():
    #region constructor
    def __init__(self, Name='A', Pipes=[]):
        '''
        Defines a loop in a pipe network.  Note: the pipes must be listed in order.  The traversal of a pipe loop
        will begin at the start node of Pipe[0] and move in the positive direction of that pipe.  Hence, loops
        can be either CW or CCW traversed, depending on which pipe you start with.  Should work fine either way.
        :param Name: name of the loop
        :param Pipes: a list/array of pipes in this loop
        '''
        self.name=Name
        self.pipes=Pipes
    #endregion

    #region methods/functions
    def getLoopHeadLoss(self):
        '''
        Calculates the net head loss as I traverse around the loop, in m of fluid.
        :return:
        '''
        deltaP=0 #initialize to zero
        startNode=self.pipes[0].startNode #begin at the start node of the first pipe
        for p in self.pipes:
            # calculates the head loss in the pipe considering loop traversal and flow directions
            phl=p.getFlowHeadLoss(startNode)
            deltaP+=phl
            startNode=p.endNode if startNode!=p.endNode else p.startNode #move to the next node
        return deltaP
    #endregion
class Pipe():
    #region constructor
    def __init__(self, Start='A', End='B',L=100, D=200, r=0.00025, fluid=Fluid()):
        '''
        Defines a generic pipe with orientation from lowest letter to highest, alphabetically.
        :param Start: the start node (string)
        :param End: the end node (string)
        :param L: the pipe length in m (float)
        :param D: the pipe diameter in mm (float)
        :param r: the pipe roughness in m  (float)
        :param fluid:  a Fluid object (typically water)
        '''
        # from arguments given in constructor
        self.startNode=min(Start,End) #makes sure to use the lowest letter for startNode
        self.endNode=max(Start,End) #makes sure to use the highest letter for the endNode
        self.length=L
        self.r=r
        self.fluid=fluid #the fluid in the pipe

        # other calculated properties
        self.d=D/1000.0 #diameter in m
        self.relrough = self.r/self.d #calculate relative roughness for easy use later
        self.A=math.pi/4.0*self.d**2 #calculate pipe cross sectional area for easy use later
        self.Q=10 #working in units of L/s, just an initial guess
        self.vel=self.V()  #calculate the initial velocity of the fluid
        self.reynolds=self.Re() #calculate the initial reynolds number
    #endregion

    #region methods/functions
    def V(self):
        '''
        Calculate average velocity in the pipe for volumetric flow self.Q
        :return:the average velocity in m/s
        '''
        self.vel= #$JES MISSING CODE$  # the average velocity is Q/A (be mindful of units)
        return self.vel

    def Re(self):
        '''
        Calculate the reynolds number under current conditions.
        :return:
        '''
        self.reynolds= #$JES MISSING CODE$ # Re=rho*V*d/mu, be sure to use V() so velocity is updated.
        return self.reynolds

    def FrictionFactor(self):
        """
        This function calculates the friction factor for a pipe based on the
        notion of laminar, turbulent and transitional flow.
        :return: the (Darcy) friction factor
        """
        # update the Reynolds number and make a local variable Re
        Re=self.Re()
        rr=self.relrough
        # to be used for turbulent flow
        def CB():
            # note:  in numpy log is for natural log.  log10 is log base 10.
            cb = lambda f: 1 / (f ** 0.5) + 2.0 * np.log10(rr / 3.7 + 2.51 / (Re * f ** 0.5))
            result = fsolve(cb, (0.01))
            val = cb(result[0])
            return result[0]
        # to be used for laminar flow
        def lam():
            return 64 / Re

        if Re >= 4000:  # true for turbulent flow
            return CB()
        if Re <= 2000:  # true for laminar flow
            return lam()

        # transition flow is ambiguous, so use normal variate weighted by Re
        CBff = CB()
        Lamff = lam()
        # I assume laminar is more accurate when just above 2000 and CB more accurate when just below Re 4000.
        # I will weight the mean appropriately using a linear interpolation.
        mean = Lamff+((Re-2000)/(4000-2000))*(CBff - Lamff)
        sig = 0.2 * mean
        # Now, use normalvariate to put some randomness in the choice
        return rnd.normalvariate(mean, sig)

    def frictionHeadLoss(self):  # calculate headloss through a section of pipe in m of fluid
        '''
        Use the Darcy-Weisbach equation to find the head loss through a section of pipe.
        '''
        g = 9.81  # m/s^2
        ff = self.FrictionFactor()
        hl = #$JES MISSING CODE$ # calculate the head loss in m of water
        return hl

    def getFlowHeadLoss(self, s):
        '''
        Calculate the head loss for the pipe.
        :param s: the node i'm starting with in a traversal of the pipe
        :return: the signed headloss through the pipe in m of fluid
        '''
        #while traversing a loop, if s = startNode I'm traversing in same direction as positive pipe
        nTraverse= 1 if s==self.startNode else -1
        #if flow is positive sense, scalar =1 else =-1
        nFlow=1 if self.Q >= 0 else -1
        return nTraverse*nFlow*self.frictionHeadLoss()

    def Name(self):
        '''
        Gets the pipe name.
        :return:
        '''
        return self.startNode+'-'+self.endNode

    def oContainsNode(self, node):
        #does the pipe connect to the node?
        return self.startNode==node or self.endNode==node

    def printPipeFlowRate(self):
        print('The flow in segment {} is {:0.2f} L/s'.format(self.Name(),self.Q))

    def getFlowIntoNode(self, n):
        '''
        determines the flow rate into node n
        :param n: a node object
        :return: +/-Q
        '''
        if n==self.startNode:
            return -self.Q
        return self.Q
    #endregion

class PipeNetwork():
    #region constructor
    def __init__(self, Pipes=[], Loops=[], Nodes=[], fluid=Fluid()):
        '''
        The pipe network is built from pipe, node, loop, and fluid objects.
        :param Pipes: a list of pipe objects
        :param Loops: a list of loop objects
        :param Nodes: a list of node objects
        :param fluid: a fluid object
        '''
        self.loops=Loops
        self.nodes=Nodes
        self.Fluid=fluid
        self.pipes=Pipes
    #endregion

    #region methods/functions
    def findFlowRates(self):
        '''
        a method to analyze the pipe network and find the flow rates in each pipe
        given the constraints of: i) no net flow into a node and ii) no net pressure drops in the loops.
        :return: a list of flow rates in the pipes
        '''
        #see how many nodes and loops there are, this is how many equation results I will return
        N=len(self.nodes)+len(self.loops)
        # build an initial guess for flow rates in the pipes.
        # note that I only have 10 pipes, but need 11 variables because of the degenerate node equation at b.
        Q0=np.full(N,10)
        def fn(q):
            """
            This is used as a callback for fsolve.  The mass continuity equations at the nodes and the loop equations
            are functions of the flow rates in the pipes.  Hence, fsolve will search for the roots of these equations
            by varying the flow rates in each pipe.
            :param q: an array of flowrates in the pipes + 1 extra value b/c of node b
            :return: L an array containing flow rates at the nodes and  pressure losses for the loops
            """
            #update the flow rate in each pipe object
            for i in range(len(self.pipes)):
                self.pipes[i].Q= #$JES MISSING CODE$  # set volumetric flow rate from input argument q
            #calculate the net flow rate for the node objects
            # note:  when flow rates in pipes are correct, the net flow into each node should be zero.
            L= #$JES MISSING CODE$  # call the getNodeFlowRates function of this class
            #calculate the net head loss for the loop objects
            # note: when the flow rates in pipes are correct, the net head loss for each loop should be zero.
            L+= #$JES MISSING CODE$  # call the getLoopHeadLosses function of this class
            return L
        #using fsolve to find the flow rates
        FR=fsolve(fn,Q0)
        return FR

    def getNodeFlowRates(self):
        #each node object is responsible for calculating its own net flow rate
        qNet=[n.getNetFlowRate() for n in self.nodes]
        return qNet

    def getLoopHeadLosses(self):
        #each loop object is responsible for calculating its own net head loss
        lhl=[l.getLoopHeadLoss() for l in self.loops]
        return lhl

    def getPipe(self, name):
        #returns a pipe object by its name
        for p in self.pipes:
            if name == p.Name():
                return p

    def getNodePipes(self, node):
        #returns a list of pipe objects that are connected to the node object
        l=[]
        for p in self.pipes:
            if p.oContainsNode(node):
                l.append(p)
        return l

    def nodeBuilt(self, node):
        #determines if I have already constructed this node object (by name)
        for n in self.nodes:
            if n.name==node:
                return True
        return False

    def getNode(self, name):
        #returns one of the node objects by name
        for n in self.nodes:
            if n.name==name:
                return n

    def buildNodes(self):
        #automatically create the node objects by looking at the pipe ends
        for p in self.pipes:
            if self.nodeBuilt(p.startNode)==False:
                #instantiate a node object and append it to the list of nodes
                self.nodes.append(Node(p.startNode,self.getNodePipes(p.startNode)))
            if self.nodeBuilt(p.endNode)==False:
                #instantiate a node object and append it to the list of nodes
                self.nodes.append(Node(p.endNode,self.getNodePipes(p.endNode)))

    def printPipeFlowRates(self):
        for p in self.pipes:
            p.printPipeFlowRate()

    def printNetNodeFlows(self):
        for n in self.nodes:
            print('net flow into node {} is {:0.2f}'.format(n.name, n.getNetFlowRate()))

    def printLoopHeadLoss(self):
        for l in self.loops:
            print('head loss for loop {} is {:0.2f}'.format(l.name, l.getLoopHeadLoss()))
    #endregion
# endregion

# region function definitions
def main():
    '''
    This program analyzes flows in a given pipe network based on the following:
    1. The pipe segments are named by their endpoint node names:  e.g., a-b, b-e, etc.
    2. Flow from the lower letter to the higher letter of a pipe is considered positive.
    3. Pressure decreases in the direction of flow through a pipe.
    4. At each node in the pipe network, mass is conserved.
    5. For any loop in the pipe network, the pressure loss is zero
    Approach to analyzing the pipe network:
    Step 1: build a pipe network object that contains pipe, node, loop and fluid objects
    Step 2: calculate the flow rates in each pipe using fsolve
    Step 3: output results
    Step 4: check results against expected properties of zero head loss around a loop and mass conservation at nodes.
    :return:
    '''
    #instantiate a Fluid object to define the working fluid as water
    water=#$JES MISSING CODE$  #
    roughness = 0.00025  # in meters

    #instantiate a new PipeNetwork object
    PN=#$JES MISSING CODE$  #
    #add Pipe objects to the pipe network (see constructor for Pipe class)
    PN.pipes.append(Pipe('a','b',250, 300, roughness, water))
    PN.pipes.append(Pipe('a','c',100, 200, roughness, water))
    PN.pipes.append(Pipe('b','e',100, 200, roughness, water))
    PN.pipes.append(Pipe('c','d',125, 200, roughness, water))
    PN.pipes.append(Pipe('c','f',100, 150, roughness, water))
    PN.pipes.append(Pipe('d','e',125, 200, roughness, water))
    PN.pipes.append(Pipe('d','g',100, 150, roughness, water))
    PN.pipes.append(Pipe('e','h',100, 150, roughness, water))
    PN.pipes.append(Pipe('f','g',125, 250, roughness, water))
    PN.pipes.append(Pipe('g','h',125, 250, roughness, water))
    #add Node objects to the pipe network by calling buildNodes method of PN object
    PN.buildNodes()

    #update the external flow of certain nodes
    PN.getNode('a').extFlow=60
    PN.getNode('d').extFlow=-30
    PN.getNode('f').extFlow=-15
    PN.getNode('h').extFlow=-15

    #add Loop objects to the pipe network
    PN.loops.append(Loop('A',[PN.getPipe('a-b'), PN.getPipe('b-e'),PN.getPipe('d-e'), PN.getPipe('c-d'), PN.getPipe('a-c')]))
    PN.loops.append(Loop('B',[PN.getPipe('c-d'), PN.getPipe('d-g'),PN.getPipe('f-g'), PN.getPipe('c-f')]))
    PN.loops.append(Loop('C',[PN.getPipe('d-e'), PN.getPipe('e-h'),PN.getPipe('g-h'), PN.getPipe('d-g')]))

    #call the findFlowRates method of the PN (a PipeNetwork object)
    PN.findFlowRates()

    #get output
    PN.printPipeFlowRates()
    print()
    print('Check node flows:')
    PN.printNetNodeFlows()
    print()
    print('Check loop head loss:')
    PN.printLoopHeadLoss()
    #PN.printPipeHeadLosses()
# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion

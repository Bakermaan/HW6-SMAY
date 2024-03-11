import numpy as np
import math
from scipy.optimize import fsolve

class Fluid:
    def __init__(self, mu=0.00089, rho=1000):
        self.mu = mu
        self.rho = rho
        self.nu = self.mu / self.rho

class Node:
    def __init__(self, Name='a', Pipes=None, ExtFlow=0):
        self.name = Name
        self.pipes = Pipes if Pipes else []
        self.extFlow = ExtFlow

    def getNetFlowRate(self):
        Qtot = self.extFlow  # Include external flow in L/s
        for p in self.pipes:
            Qtot += p.getFlowIntoNode(self.name)
        return Qtot

class Loop:
    def __init__(self, Name='A', Pipes=None):
        self.name = Name
        self.pipes = Pipes if Pipes else []

    def getLoopHeadLoss(self):
        deltaP = 0  # initialize to zero
        startNode = self.pipes[0].startNode
        for p in self.pipes:
            phl = p.getFlowHeadLoss(startNode)
            deltaP += phl
            startNode = p.endNode if startNode != p.endNode else p.startNode
        return deltaP

class Pipe:
    def __init__(self, Start='A', End='B', L=100, D=200, r=0.00025, fluid=Fluid()):
        self.startNode = min(Start, End)
        self.endNode = max(Start, End)
        self.length = L
        self.diameter_m = D / 1000.0
        self.r = r
        self.fluid = fluid
        self.area = math.pi / 4.0 * self.diameter_m ** 2
        self.flow_rate_Lps = 10
        self.update_calculations()

    def update_calculations(self):
        self.velocity = self.calculate_velocity()
        self.reynolds_number = self.calculate_reynolds_number()
        self.friction_factor = self.calculate_friction_factor()

    def calculate_velocity(self):
        return (self.flow_rate_Lps / 1000) / self.area

    def calculate_reynolds_number(self):
        return (self.fluid.rho * self.velocity * self.diameter_m) / self.fluid.mu

    def calculate_friction_factor(self):
        if self.reynolds_number >= 4000:
            return self.turbulent_flow_friction_factor()
        elif self.reynolds_number <= 2000:
            return self.laminar_flow_friction_factor()
        else:
            return self.transition_flow_friction_factor()

    # ... (Methods for turbulent, laminar, and transitional friction factors would be here) ...

    def frictionHeadLoss(self):
        g = 9.81
        hl = (self.friction_factor * self.length / self.diameter_m) * (self.velocity ** 2) / (2 * g)
        return hl

    def getFlowHeadLoss(self, s):
        nTraverse = 1 if s == self.startNode else -1
        nFlow = 1 if self.flow_rate_Lps >= 0 else -1
        return nTraverse * nFlow * self.frictionHeadLoss()

    def Name(self):
        return self.startNode + '-' + self.endNode

    def getFlowIntoNode(self, n):
        if n == self.startNode:
            return -self.flow_rate_Lps
        return self.flow_rate_Lps


    def laminar_flow_friction_factor(self):
        # Laminar flow: f = 64 / Re
        return 64.0 / self.reynolds_number

    def turbulent_flow_friction_factor(self):
        # Turbulent flow: using the Haaland equation for demonstration
        # Note: This is a simplification and may not be accurate for all turbulent flow calculations.
       return (1. / (1.8 * math.log10((self.r / (3.7 * self.diameter_m))**1.11 + 6.9 / self.reynolds_number)))**2

    def transition_flow_friction_factor(self):
        # Transitional flow: not clearly defined, so we interpolate between laminar and turbulent
        # Note: This is a simplification and a proper transition flow calculation may be more complex.
        laminar_ff = self.laminar_flow_friction_factor()
        turbulent_ff = self.turbulent_flow_friction_factor()
        return laminar_ff + (turbulent_ff - laminar_ff) * ((self.reynolds_number - 2000) / (4000 - 2000))

class PipeNetwork:
    def __init__(self, pipes=None, loops=None, nodes=None, fluid=Fluid()):
        self.pipes = {} if pipes is None else pipes
        self.loops = [] if loops is None else loops
        self.nodes = {} if nodes is None else nodes
        self.fluid = fluid

    def add_pipe(self, pipe):
        self.pipes[pipe.Name()] = pipe
        self.add_nodes_from_pipe(pipe)

    def add_nodes_from_pipe(self, pipe):
        for node_name in [pipe.startNode, pipe.endNode]:
            if node_name not in self.nodes:
                self.nodes[node_name] = Node(node_name)

    def add_external_flow(self, node_name, flow):
        self.nodes[node_name].extFlow += flow

    def add_loop(self, loop):
        self.loops.append(loop)

    def findFlowRates(self):
        N = len(self.nodes) + len(self.loops)
        Q0 = np.full(N, 10)

        def equations(Q):
            for i, pipe in enumerate(self.pipes.values()):
                pipe.flow_rate_Lps = Q[i]
                pipe.update_calculations()
            return self.getNodeFlowRates() + self.getLoopHeadLosses()

        flow_rates = fsolve(equations, Q0)
        return flow_rates

    def getNodeFlowRates(self):
        return [node.getNetFlowRate() for node in self.nodes.values()]

    def getLoopHeadLosses(self):
        return [loop.getLoopHeadLoss() for loop in self.loops]

    def print_results(self):
        for pipe in self.pipes.values():
            print(f'The flow in segment {pipe.Name()} is {pipe.flow_rate_Lps:.2f} L/s')

        print('\nCheck node flows:')
        for node in self.nodes.values():
            print(f'Net flow into node {node.name} is {node.getNetFlowRate():.2f} L/s')

        print('\nCheck loop head loss:')
        for loop in self.loops:
            print(f'Head loss for loop {loop.name} is {loop.getLoopHeadLoss():.2f} m')

def main():
    water = Fluid()
    roughness = 0.00025  # in meters

    PN = PipeNetwork(fluid=water)

    # Add pipes
    PN.add_pipe(Pipe('a', 'b', 250, 300, roughness, water))
    PN.add_pipe(Pipe('a', 'c', 100, 200, roughness, water))
    PN.add_pipe(Pipe('b', 'e', 100, 200, roughness, water))
    PN.add_pipe(Pipe('c', 'd', 125, 200, roughness, water))
    PN.add_pipe(Pipe('c', 'f', 100, 150, roughness, water))
    PN.add_pipe(Pipe('d', 'e', 125, 200, roughness, water))
    PN.add_pipe(Pipe('d', 'g', 100, 150, roughness, water))
    PN.add_pipe(Pipe('e', 'h', 100, 150, roughness, water))
    PN.add_pipe(Pipe('f', 'g', 125, 250, roughness, water))
    PN.add_pipe(Pipe('g', 'h', 125, 250, roughness, water))

    # Update external flows to nodes
    PN.add_external_flow('a', 60)
    PN.add_external_flow('d', -30)
    PN.add_external_flow('f', -15)
    PN.add_external_flow('h', -15)

    # Define loops with their pipes
    loop_A_pipes = [PN.pipes['a-b'], PN.pipes['b-e'], PN.pipes['d-e'], PN.pipes['c-d'], PN.pipes['a-c']]
    loop_B_pipes = [PN.pipes['c-d'], PN.pipes['d-g'], PN.pipes['f-g'], PN.pipes['c-f']]
    loop_C_pipes = [PN.pipes['d-e'], PN.pipes['e-h'], PN.pipes['g-h'], PN.pipes['d-g']]

    # Add loops to the network
    PN.add_loop(Loop('A', loop_A_pipes))
    PN.add_loop(Loop('B', loop_B_pipes))
    PN.add_loop(Loop('C', loop_C_pipes))

    # Find flow rates and print results
    PN.findFlowRates()
    PN.print_results()

if __name__ == "__main__":
    main()


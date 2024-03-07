from HW6_1_OOP import ResistorNetwork
from scipy.optimize import fsolve
import numpy as np

class ResistorNetwork_2(ResistorNetwork):
    def __init__(self):
        # Call the constructor of the base class if it initializes any data.
        super().__init__()  # This might need arguments based on your base class constructor.

    def GetKirchoffVals(self, currents):
        """
        Overridden method to calculate the values for Kirchhoff's laws for the new circuit.
        This must be customized based on the circuit configuration.
        """
        I1, I2, I3, I4, I5 = currents
        # KVL for loop abcdea
        eq1 = 2*I1 - I3 + 4*I5 - 16
        # KVL for loop cdefc
        eq2 = I3 + 4*I4 - 2*I2 - 32
        # KVL for loop abdefa (outer loop)
        eq3 = 2*I1 + 2*I2 - 48
        # Currents at node d: I3 (incoming) = I4 + I2 (outgoing)
        eq4 = I3 - I4 - I2
        # Node b (additional equation if needed): I1 (incoming) = I5 (outgoing)
        eq5 = I1 - I5
        return np.array([eq1, eq2, eq3, eq4, eq5])

    def AnalyzeCircuit(self):
        """
        Overridden method from ResistorNetwork to analyze the new circuit.
        """
        # Define an initial guess for the currents.
        # This should be based on the number of currents you are solving for.
        initial_guess = [0.1] * 5  # Adjust the number based on how many currents there are.

        # Solve the circuit using fsolve and the GetKirchoffVals method
        solved_currents = fsolve(self.GetKirchoffVals, initial_guess)

        # Print or return the solved currents
        print("Solved Currents:", solved_currents)
        return solved_currents

# Assuming the following usage
if __name__ == "__main__":
    # Create an instance of the new ResistorNetwork_2 class
    network = ResistorNetwork_2()
    
    # Build the network from the file (assuming the method name and usage are correct)
    network.BuildNetworkFromFile('ResistorNetwork_2.txt')
    
    # Analyze the new circuit
    currents = network.AnalyzeCircuit()
    
    # Output the results
    print("Currents in the circuit: I1 = {:.2f}, I2 = {:.2f}, I3 = {:.2f}, I4 = {:.2f}, I5 = {:.2f}".format(*currents))

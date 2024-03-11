from HW6_1_OOP import ResistorNetwork
from scipy.optimize import fsolve


class ResistorNetwork_2(ResistorNetwork):
        def __init__(self):
            # Call the constructor of the base class if it initializes any data.
            super().__init__()  # This might need arguments based on your base class constructor.

    def GetKirchoffVals(self, i):
        """
        Overridden method to calculate the values for Kirchhoff's laws for the new circuit.
        This must be customized based on the circuit configuration.
        """
        """
        This function uses Kirchoff Voltage and Current laws to analyze this specific circuit
        KVL:  The net voltage drop for a closed loop in a circuit should be zero
        KCL:  The net current flow into a node in a circuit should be zero
        :param i: a list of currents relevant to the circuit
        :return: a list of loop voltage drops and node currents
        """
        """
        pulled from a diffrent program i made to skip needing to call back the function
        but still works 
        """
        # set current in resistors in the top loop.
        '''after 12 hours of work, irvin has it! '''
        self.GetResistorByName('ad').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('bc').Current = i[0]  # I_1 in diagram
        self.GetResistorByName('cd').Current = i[2]  # I_3 in diagram
        # set current in resistor in bottom loops.
        self.GetResistorByName('df').Current = i[1]  # I_2 in diagram
        self.GetResistorByName('ed').Current = i[3]  # I_4 in diagram
        self.GetResistorByName('ec').Current = i[4]  # I_5 in diagram
        # calculate net current into node c

        Node_c_Current = sum([i[0], i[4], -i[2]])
        # calculate net current into node d
        Node_d_Current = sum([i[2], i[3], -i[0], -i[1]])

        KVL = self.GetLoopVoltageDrops()  # two equations here

        KVL.append(Node_c_Current)  # one equation here
        KVL.append(Node_d_Current)  # one equation here
    
        # Ensure KVL has 5 elements
        while len(KVL) < 5:
            KVL.append(0.0)  # Fill with zeros if necessary
        return [KVL[0], KVL[1], KVL[2], KVL[3], KVL[4]]
        '''this is remement of debugging, left here for later as irvin is going to come back at a later date and find out
        why it doesn't match with the sim he made'''

    

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
    
        # Output the results in a better manner with units
    print("Currents in the circuit:")
    print("I1 = {:.2f} ohms".format(currents[0]))
    print("I2 = {:.2f} ohms".format(currents[1]))
    print("I3 = {:.2f} ohms".format(currents[2]))
    print("I4 = {:.2f} ohms".format(currents[3]))
    print("I5 = {:.2f} ohms".format(currents[4]))

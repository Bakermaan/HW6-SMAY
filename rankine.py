from steam import steam

class rankine:
    """
    A class representing a Rankine cycle.

    This class models a Rankine cycle, which is a thermodynamic cycle commonly used in steam power plants.
    It calculates and stores the properties and efficiency of the Rankine cycle based on specified parameters.

    Attributes:
        p_low (float): The low-pressure value of the Rankine cycle.
        p_high (float): The high-pressure value of the Rankine cycle.
        t_high (float, optional): The high-temperature value of the Rankine cycle (if superheated).
            Defaults to None.
        name (str, optional): A useful identifier for the Rankine cycle instance. Defaults to 'Rankine Cycle'.
        efficiency (float): The efficiency of the Rankine cycle.
        turbine_work (float): The work done by the turbine in the Rankine cycle.
        pump_work (float): The work done by the pump in the Rankine cycle.
        heat_added (float): The heat added to the Rankine cycle.

    Methods:
        __init__: Initializes a Rankine cycle instance with specified parameters.
        calc_states: Calculates the steam properties at various states of the Rankine cycle.
        calc_efficiency: Calculates the efficiency of the Rankine cycle.
        print_summary: Prints a summary of the Rankine cycle.
    """

    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        """
        Initializes a Rankine cycle instance with specified parameters.

        Args:
            p_low (float, optional): The low-pressure value of the Rankine cycle. Defaults to 8.
            p_high (float, optional): The high-pressure value of the Rankine cycle. Defaults to 8000.
            t_high (float, optional): The high-temperature value of the Rankine cycle (if superheated).
                Defaults to None.
            name (str, optional): A useful identifier for the Rankine cycle instance. Defaults to 'Rankine Cycle'.
        """
        # Initialize the cycle with specified pressures, optional temperature, and name.
        self.p_low = p_low  # Low pressure of the cycle, in kPa.
        self.p_high = p_high  # High pressure of the cycle, in kPa.
        self.t_high = t_high  # Optional high temperature for superheat, in °C.
        self.name = name  # Name of the cycle for identification.
        # Properties that will be calculated later.
        self.efficiency = None
        self.turbine_work = None
        self.pump_work = None
        self.heat_added = None
        self.calc_states()  # Start calculations of the cycle states upon initialization.

    def calc_states(self):
        """
        Calculates the steam properties at various states of the Rankine cycle.
        """
        # Determine the state of steam at the turbine inlet, considering if it's superheated or not.
        if self.t_high is None:
            # Saturated steam at high pressure if t_high is not specified.
            self.state1 = steam(self.p_high, x=1, name='Turbine Inlet')
        else:
            # Superheated steam if t_high is provided.
            self.state1 = steam(self.p_high, T=self.t_high, name='Turbine Inlet')
        # Calculate properties for state 1.
        self.state1.calc()

        # Calculate state 2 properties assuming isentropic expansion to low pressure.
        self.state2 = steam(self.p_low, s=self.state1.s, name='Turbine Exit')
        self.state2.calc()

        # State 3 is the saturated liquid at the pump inlet.
        self.state3 = steam(self.p_low, x=0, name='Pump Inlet')
        self.state3.calc()

        # Assume isentropic compression for state 4 calculations.
        self.state4 = steam(self.p_high, s=self.state3.s, name='Pump Exit')
        self.state4.calc()

        # Correct pump work using specific volume and pressure difference.
        self.state4.h = self.state3.h + (self.state3.v * (self.p_high - self.p_low) * 1e3)  # Pump work, in kJ/kg.

        # With states defined, calculate cycle efficiency.
        self.calc_efficiency()

    def calc_efficiency(self):
        """
        Calculates the efficiency of the Rankine cycle.
        """
        # Heat added in the boiler from state 4 to state 1.
        self.heat_added = self.state1.h - self.state4.h
        # Turbine work is the enthalpy drop across the turbine, from state 1 to state 2.
        self.turbine_work = self.state1.h - self.state2.h
        # Pump work required to pump the fluid to high pressure, from state 3 to state 4.
        self.pump_work = self.state4.h - self.state3.h
        # Efficiency calculation, based on net work output divided by heat input.
        self.efficiency = ((self.turbine_work - self.pump_work) / self.heat_added) * 100

    def print_summary(self):
        """
        Prints a summary of the Rankine cycle.
        """
        # Ensure efficiency is calculated before printing.
        if self.efficiency is None:
            self.calc_efficiency()

        # Print cycle summary including efficiency and work terms.
        print(f'Cycle Summary for: {self.name}')
        print(f'\tEfficiency: {self.efficiency:.2f}%')
        print(f'\tTurbine Work: {self.turbine_work:.2f} kJ/kg')
        print(f'\tPump Work: {self.pump_work:.2f} kJ/kg')
        print(f'\tHeat Added: {self.heat_added:.2f} kJ/kg')
        # Print detailed state properties for each major state in the cycle.
        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()

def main():
    """
    Main function to demonstrate Rankine cycle usage.
    """
    # Instantiate a Rankine cycle with default parameters for a saturated cycle.
    saturated_rankine_cycle = rankine(name="Saturated Rankine Cycle")
    saturated_rankine_cycle.print_summary()

    # Instantiate a Rankine cycle with specified parameters for a superheated cycle.
    superheated_temperature = 500  # Example superheated temperature for demonstration.
    superheated_rankine_cycle = rankine(p_low=8, p_high=8000, t_high=superheated_temperature, name="Superheated Rankine Cycle")
    superheated_rankine_cycle.print_summary()

if __name__ == "__main__":
    main()

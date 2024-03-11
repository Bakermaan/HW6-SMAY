from steam import steam

class rankine:
    def __init__(self, p_low=8, p_high=8000, t_high=None, name='Rankine Cycle'):
        self.p_low = p_low
        self.p_high = p_high
        self.t_high = t_high
        self.name = name
        self.efficiency = None
        self.turbine_work = None
        self.pump_work = None
        self.heat_added = None
        self.calc_states()

    def calc_states(self):
        if self.t_high is None:
            self.state1 = steam(self.p_high, x=1, name='Turbine Inlet')  # Saturated vapor at high pressure
        else:
            self.state1 = steam(self.p_high, T=self.t_high, name='Turbine Inlet')  # Superheated vapor at high pressure
        self.state1.calc()

        self.state2 = steam(self.p_low, s=self.state1.s, name='Turbine Exit')  # Isentropic expansion to low pressure
        self.state2.calc()

        self.state3 = steam(self.p_low, x=0, name='Pump Inlet')  # Saturated liquid at low pressure
        self.state3.calc()

        self.state4 = steam(self.p_high, s=self.state3.s, name='Pump Exit')  # Isentropic compression to high pressure
        self.state4.calc()
        # Pump work calculation (assuming no change in specific volume)
        self.state4.h = self.state3.h + self.state3.v * (self.p_high - self.p_low) * 1e3  # Pump work in kJ/kg

        self.calc_efficiency()

    def calc_efficiency(self):
        # Heat added (in the boiler)
        self.heat_added = self.state1.h - self.state4.h  # Heat added should be based on state 1 and state 4 enthalpy difference

        # Turbine work (expansion)
        self.turbine_work = self.state1.h - self.state2.h  # Turbine work in kJ/kg

        # Pump work (compression)
        self.pump_work = self.state4.h - self.state3.h  # Pump work in kJ/kg

        # Efficiency calculation
        self.efficiency = (self.turbine_work - self.pump_work) / self.heat_added * 100

    def print_summary(self):
        if self.efficiency is None:
            self.calc_efficiency()

        print(f'Cycle Summary for: {self.name}')
        print(f'\tEfficiency: {self.efficiency:.2f}%')
        print(f'\tTurbine Work: {self.turbine_work:.2f} kJ/kg')
        print(f'\tPump Work: {self.pump_work:.2f} kJ/kg')
        print(f'\tHeat Added: {self.heat_added:.2f} kJ/kg')

        self.state1.print()
        self.state2.print()
        self.state3.print()
        self.state4.print()

def main():
    # Creating a Rankine cycle object with saturated vapor at the turbine inlet
    saturated_rankine_cycle = rankine(name="Saturated Rankine Cycle")
    saturated_rankine_cycle.print_summary()

    # Creating a Rankine cycle object with superheated steam at the turbine inlet
    superheated_temperature = 500  # Replace with actual superheated temperature
    superheated_rankine_cycle = rankine(p_low=8, p_high=8000, t_high=superheated_temperature, name="Superheated Rankine Cycle")
    superheated_rankine_cycle.print_summary()

if __name__ == "__main__":
    main()

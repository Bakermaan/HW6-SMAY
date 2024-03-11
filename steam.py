# region imports
import numpy as np
from scipy.interpolate import griddata


# endregion

# region class definitions
class steam:
    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        self.p = pressure  # pressure in kPa
        self.T = T  # Temperature in degrees C
        self.x = x  # quality
        self.v = v  # specific volume in m^3/kg
        self.h = h  # specific enthalpy in kJ/kg
        self.s = s  # specific entropy in kJ/(kg*K)
        self.name = name  # a useful identifier
        self.region = None  # 'superheated' or 'saturated' or 'two-phase'
        if T is None and x is None and v is None and h is None and s is None:
            return
        else:
            self.calc()

    def calc(self):
        # Load saturated steam properties from text file
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('sat_water_table.txt', skiprows=1, unpack=True)

        # Load superheated steam properties from text file
        tcol, hcol, scol, pcol = np.loadtxt('superheated_water_table.txt', skiprows=1, unpack=True)

        R = 8.314 / (18 / 1000)  # Ideal gas constant for water [J/(mol K)]/[kg/mol]
        Pbar = self.p / 100  # Pressure in bar - 1 bar = 100 kPa roughly

        # Get saturated properties using interpolation
        Tsat = float(griddata(ps, ts, (Pbar), method='linear'))
        hf = float(griddata(ps, hfs, (Pbar), method='linear'))
        hg = float(griddata(ps, hgs, (Pbar), method='linear'))
        sf = float(griddata(ps, sfs, (Pbar), method='linear'))
        sg = float(griddata(ps, sgs, (Pbar), method='linear'))
        vf = float(griddata(ps, vfs, (Pbar), method='linear'))
        vg = float(griddata(ps, vgs, (Pbar), method='linear'))

        self.hf = hf  # Save saturated liquid enthalpy for the object

        if self.T is not None and self.T > Tsat:
            self.region = 'Superheated'
            superheated_properties = griddata((pcol, tcol), (hcol, scol), (Pbar, self.T), method='linear')
            self.h, self.s = superheated_properties
            self.x = None  # x is not defined in the superheated region
            TK = self.T + 273.15  # Convert temperature to Kelvin
            self.v = R * TK / (self.p * 1000)  # Ideal gas approximation for specific volume
        elif self.x is not None:
            self.region = 'Saturated'
            self.T = Tsat
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)
        elif self.h is not None:
            self.x = (self.h - hf) / (hg - hf)
            if 0 <= self.x <= 1:
                self.region = 'Saturated'
                self.T = Tsat
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                # Code needed for superheated interpolation based on enthalpy
        elif self.s is not None:
            self.x = (self.s - sf) / (sg - sf)
            if 0 <= self.x <= 1:
                self.region = 'Saturated'
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
                # Code needed for superheated interpolation based on entropy

    def print(self):
        print('Name:', self.name)
        print('Region:', self.region)
        print(f'Pressure: {self.p:.2f} kPa')
        if self.T is not None:
            print(f'Temperature: {self.T:.2f} °C')
        if self.h is not None:
            print(f'Enthalpy: {self.h:.2f} kJ/kg')
        if self.s is not None:
            print(f'Entropy: {self.s:.4f} kJ/(kg K)')
        if self.v is not None:
            print(f'Specific Volume: {self.v:.6f} m^3/kg')
        if self.x is not None:
            print(f'Quality: {self.x:.4f}')
        print()


# endregion

# region function definitions
def main():
    inlet = steam(pressure=7350, name='Turbine Inlet')
    inlet.x = 0.9  # 90 percent quality
    inlet.calc()
    inlet.print()

    h1 = inlet.h
    s1 = inlet.s
    print(f'h1: {h1:.2f} kJ/kg, s1: {s1:.4f} kJ/(kg K)\n')

    outlet = steam(pressure=100, s=s1, name='Turbine Exit')
    outlet.calc()
    outlet.print()

    another = steam(pressure=8575, h=2050, name='State 3')
    another.calc()
    another.print()

    yet_another = steam(pressure=8575, h=3125, name='State 4')
    yet_another.calc()
    yet_another.print()


# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion

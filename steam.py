import numpy as np
from scipy.interpolate import griddata

class steam:
    """
    A class representing steam properties.

    This class models the properties of steam, including pressure, temperature, quality, specific volume,
    specific enthalpy, specific entropy, and a useful identifier for reference. It provides methods for
    calculating steam properties based on provided data and printing the properties.

    Attributes:
        p (float): The pressure of the steam in kilopascals (kPa).
        T (float): The temperature of the steam in degrees Celsius (°C).
        x (float): The quality of the steam.
        v (float): The specific volume of the steam in cubic meters per kilogram (m^3/kg).
        h (float): The specific enthalpy of the steam in kilojoules per kilogram (kJ/kg).
        s (float): The specific entropy of the steam in kilojoules per kilogram per Kelvin (kJ/(kg*K)).
        name (str): A useful identifier for the steam instance.
        region (str): The region of the steam, which can be 'superheated', 'saturated', or 'two-phase'.

    Methods:
        __init__: Initializes a steam object with specified properties.
        calc: Calculates the steam properties based on provided data.
        print: Prints the steam properties.
    """
    def __init__(self, pressure, T=None, x=None, v=None, h=None, s=None, name=None):
        """
        Initializes a steam object with specified properties.

        Args:
            pressure (float): The pressure of the steam in kilopascals (kPa).
            T (float, optional): The temperature of the steam in degrees Celsius (°C). Defaults to None.
            x (float, optional): The quality of the steam. Defaults to None.
            v (float, optional): The specific volume of the steam in cubic meters per kilogram (m^3/kg).
                Defaults to None.
            h (float, optional): The specific enthalpy of the steam in kilojoules per kilogram (kJ/kg).
                Defaults to None.
            s (float, optional): The specific entropy of the steam in kilojoules per kilogram per Kelvin
                (kJ/(kg*K)). Defaults to None.
            name (str, optional): A useful identifier for the steam instance. Defaults to None.
        """
        # Initialize steam object with given properties and default values. Calculation is deferred to `calc` method if any property is provided.
        self.p = pressure  # Pressure in kilopascals
        self.T = T  # Temperature in degrees Celsius
        self.x = x  # Quality (dimensionless)
        self.v = v  # Specific volume in cubic meters per kilogram
        self.h = h  # Specific enthalpy in kilojoules per kilogram
        self.s = s  # Specific entropy in kilojoules per kilogram per Kelvin
        self.name = name  # Identifier for the steam instance
        self.region = None  # The region will be determined based on property values
        if T is None and x is None and v is None and h is None and s is None:
            return  # Early return if no properties other than pressure are specified
        else:
            self.calc()  # Calculate properties if any are specified

    def calc(self):
        """
        Calculates the steam properties based on provided data.

        This method calculates the steam properties based on the provided data such as pressure, temperature,
        quality, specific volume, specific enthalpy, and specific entropy. It utilizes interpolation techniques
        to determine the properties depending on the region of the steam (superheated or saturated).
        """
        # Load steam tables and calculate properties based on the given state or input parameters.
        # Load saturated steam properties from a text file
        ts, ps, hfs, hgs, sfs, sgs, vfs, vgs = np.loadtxt('sat_water_table.txt', skiprows=1, unpack=True)
        # Load superheated steam properties from a text file
        tcol, hcol, scol, pcol = np.loadtxt('superheated_water_table.txt', skiprows=1, unpack=True)

        R = 8.314 / (18 / 1000)  # Specific gas constant for steam
        Pbar = self.p / 100  # Convert pressure from kPa to bar for table lookup

        # Interpolate to find saturated properties at the given pressure
        Tsat = float(griddata(ps, ts, (Pbar), method='linear'))
        hf = float(griddata(ps, hfs, (Pbar), method='linear'))
        hg = float(griddata(ps, hgs, (Pbar), method='linear'))
        sf = float(griddata(ps, sfs, (Pbar), method='linear'))
        sg = float(griddata(ps, sgs, (Pbar), method='linear'))
        vf = float(griddata(ps, vfs, (Pbar), method='linear'))
        vg = float(griddata(ps, vgs, (Pbar), method='linear'))

        self.hf = hf  # Store saturated liquid enthalpy for potential future use

        # Determine region and calculate properties based on temperature, quality, enthalpy, or entropy
        if self.T is not None and self.T > Tsat:
            # If temperature is specified and above saturation, treat as superheated steam
            self.region = 'Superheated'
            # Interpolate superheated properties from table
            superheated_properties = griddata((pcol, tcol), hcol, (Pbar, self.T), method='linear')
            self.h = superheated_properties
            self.s = float(griddata((pcol, tcol), scol, (Pbar, self.T), method='linear'))
            self.x = None  # Quality is not defined for superheated steam
            TK = self.T + 273.15  # Convert to Kelvin for specific volume calculation
            self.v = R * TK / (self.p * 1000)  # Calculate specific volume using ideal gas law approximation
        elif self.x is not None:
            # If quality is specified, treat as saturated mixture
            self.region = 'Saturated'
            self.T = Tsat  # Set temperature to saturation temperature
            # Calculate properties based on quality
            self.h = hf + self.x * (hg - hf)
            self.s = sf + self.x * (sg - sf)
            self.v = vf + self.x * (vg - vf)
        elif self.h is not None:
            # If specific enthalpy is specified, determine region and calculate quality
            self.x = (self.h - hf) / (hg - hf)
            if 0 <= self.x <= 1:
                self.region = 'Saturated'
                self.T = Tsat
                self.s = sf + self.x * (sg - sf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'
        elif self.s is not None:
            # If specific entropy is specified, determine region and calculate quality
            self.x = (self.s - sf) / (sg - sf)
            if 0 <= self.x <= 1:
                self.region = 'Saturated'
                self.T = Tsat
                self.h = hf + self.x * (hg - hf)
                self.v = vf + self.x * (vg - vf)
            else:
                self.region = 'Superheated'

    def print(self):
        """
        Prints the steam properties.

        This method prints the steam properties including the steam's name, region, pressure, temperature,
        specific enthalpy, specific entropy, specific volume, and quality (if available).
        """
        # Print steam properties including name, region, and calculated values.
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

def main():
    """
    Main function to demonstrate steam class usage.

    This function demonstrates the usage of the steam class by creating instances of steam objects with
    different properties, calculating their properties, and printing them.
    """
    # Demonstration of using the steam class for various steam conditions
    inlet = steam(pressure=7350, name='Turbine Inlet')  # Create instance for turbine inlet
    inlet.x = 0.9  # Set quality
    inlet.calc()  # Calculate and update properties
    inlet.print()  # Display properties

    h1 = inlet.h  # Store enthalpy
    s1 = inlet.s  # Store entropy
    print(f'h1: {h1:.2f} kJ/kg, s1: {s1:.4f} kJ/(kg K)\n')

    outlet = steam(pressure=100, s=s1, name='Turbine Exit')  # Create instance for turbine exit using inlet entropy
    outlet.calc()  # Calculate and update properties
    outlet.print()  # Display properties

    another = steam(pressure=8575, h=2050, name='State 3')  # Create another instance with specific enthalpy
    another.calc()  # Calculate and update properties
    another.print()  # Display properties

    yet_another = steam(pressure=8575, h=3125, name='State 4')  # Create yet another instance with specific enthalpy
    yet_another.calc()  # Calculate and update properties
    yet_another.print()  # Display properties

if __name__ == "__main__":
    main()

from rankine import rankine

def test_rankine_cycle():
    # Test the Rankine cycle with saturated vapor entering the turbine
    print("Testing Rankine Cycle with Saturated Vapor at Turbine Inlet")
    saturated_rankine = rankine(p_low=8, p_high=8000, t_high=None, name="Saturated Rankine Cycle")
    saturated_rankine.print_summary()
    print("\n")  # Add a newline for better readability in the output

    # Test the Rankine cycle with superheated vapor entering the turbine
    # Assuming the superheat temperature is 500 degrees Celsius above the saturation temperature
    print("Testing Rankine Cycle with Superheated Vapor at Turbine Inlet")
    superheated_temp = saturated_rankine.state1.T + 500  # Example of how to set superheat temperature
    superheated_rankine = rankine(p_low=8, p_high=8000, t_high=superheated_temp, name="Superheated Rankine Cycle")
    superheated_rankine.print_summary()

if __name__ == "__main__":
    test_rankine_cycle()

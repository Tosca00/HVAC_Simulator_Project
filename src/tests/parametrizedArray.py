import numpy as np

'''
This test use case objective is to use a parametrized array [Timestamp, Temperature, Setpoint, Mode]
to  test the hvac class methods CoolingOrHeating and calculate_consumption.
An element with a "No_Mode" value interrupts the simulation.
Starting from a predefined TimeStamp (GMT format) [exe: 2025-01-01 00:00:00]
'''

# Define the parameterized array
parametrized_array = np.array([
    ['2025-01-01 00:00:00', 28.0, 'HEATING',"ON"],
    ['2025-01-01 01:00:00', 19.0, 'COOLING',"ON"],
    ['2025-01-01 02:00:00', 22.0, 'HEATING',"ON"],
    ['2025-01-01 03:00:00', 21.0, 'HEATING',"OFF"],
    ['2025-01-01 04:00:00', 30.0, 'COOLING',"OFF"],
    #['2025-01-01 02:30:00', 21.0, 'HEATING',"OFF"]
], dtype=object)


def check_array_params(parametrized_array):
    previous_date = "0000-00-00 00:00:00"

    for i in range(len(parametrized_array)):
        if len(parametrized_array[i]) != 4:
            raise ValueError("The array must have 4 values/columns")
        if not isinstance(parametrized_array[i][0], str):
            raise ValueError("The first column must be a date string in valid iso format")
        if not isinstance(parametrized_array[i][1], (int, float)):
            raise ValueError("The second column must be a number, either int or float, representing the setpoint")
        if not isinstance(parametrized_array[i][2], str):
            if parametrized_array[i][2] != "NO_MODE" and parametrized_array[i][2] != "HEATING" and parametrized_array[i][2] != "COOLING":
                raise ValueError("The third column must be a string, representing the mode[COOLING/HEATING]")
        if not isinstance(parametrized_array[i][3], str):
            if parametrized_array[i][3] != "ON" and parametrized_array[i][3] != "OFF":
                raise ValueError("The fourth column must be a string, representing the state[ON/OFF]")
        if parametrized_array[i][0] <= previous_date: #possibile perchè le date (str) sono in formato iso
            print(f"previous_date: {previous_date} --- current_date: {parametrized_array[i][0]}")
            raise ValueError("Dates are in wrong order, all dates must be in ascending order")
        previous_date = parametrized_array[i][0]
        
        
import numpy as np
import json

'''
This test use case objective is to use a parametrized array [Timestamp, Temperature, Setpoint, Mode]
to  test the hvac class methods CoolingOrHeating and calculate_consumption.
An element with a "No_Mode" value interrupts the simulation.
Starting from a predefined TimeStamp (GMT format) [exe: 2025-01-01 00:00:00]
'''

# manually define the parameterized array, used for testing
parametrized_array_test = np.array([
    ['2025-01-01 00:00:00', 19.0, 'COOLING',"ON"],
    ['2025-01-01 01:00:00', 22.0, 'COOLING',"ON"],
    ['2025-01-01 02:00:00', 20.0, 'COOLING',"ON"],
    ['2025-01-01 03:00:00', 27.0, 'HEATING',"ON"],
    ['2025-01-01 04:00:00', 30.0, 'COOLING',"OFF"],
    ['2025-01-01 02:30:00', 21.0, 'HEATING',"OFF"]
], dtype=object)




def check_array_params(parametrized_array):
    previous_date = "0000-00-00 00:00:00"

    for i in range(len(parametrized_array)):
        if len(parametrized_array[i]) != 4:
            raise ValueError("The array must have 4 values/columns")
        if not isinstance(parametrized_array[i][0], str):
            raise ValueError("The first column must be a date string in valid iso format")
        if not isinstance(parametrized_array[i][1], (int, float)):
            print(f"Element type: {type(parametrized_array[i][1])}")
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
        

def printArr(parameterized_array: np.array):
    for array in parameterized_array:
        print(array)


#costruisce e restituisce un array paramettrizzato a partire da un file JSON
def setupArrFromJSON(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    responses = data["responses"]
    parametrized_array = []
    for response in responses:
        date = response["date"]
        temperature = int(response["temperature"])
        selectedMode = response["selectedMode"]
        isOn = response["isOn"]
        parametrized_array.append([date, temperature, selectedMode, isOn])

    with open('res.txt', 'w'):
        np.savetxt('parametrized_array.txt', parametrized_array, fmt='%s', delimiter=',')
    
    return parametrized_array
    
        
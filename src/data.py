# %% [markdown]
# imports
import datetime
import pandas as pd

# %%

def create_dataframe(temperatures,setpoints,watts,timestamps,mode):
    data = {'Temperature': temperatures, 'Setpoint': setpoints, 'Watts': watts, 'Timestamp': timestamps, 'mode': mode}
    df = pd.DataFrame(data)
    return df

# %%
def addRow(hvac,df,timer,clock_tz):
    if hvac.getHVACMode() == hvac.HVAC_Mode.COOLING:
        mode = "COOLING"
    elif hvac.getHVACMode() == hvac.HVAC_Mode.HEATING:
        mode = "HEATING"
    else:
        mode = "NO MODE"
    df = pd.concat([df, pd.DataFrame([[hvac.getTemperature_Internal(), hvac.getSetpoint(), hvac.calculate_consumption(timer), datetime.datetime.now(clock_tz).strftime('%Y-%m-%d %H:%M:%S'), hvac.getHVACMode().name]], columns=['Temperature', 'Setpoint', 'Watts', 'Timestamp','Mode'])], ignore_index=True)


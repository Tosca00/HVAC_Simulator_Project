import { Injectable, signal } from '@angular/core';
import axios from 'axios';
import { Mode } from 'fs';

export const httpService = axios.create({
  baseURL: 'http://localhost:8001'
});

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor() { }

  async createFormResponse(formResponses: {
    responses: {
        date: string;
        temperature: number;
        selectedMode: Mode;
        isOn: string;
    }[];
  }) {
    return await httpService.post('/setupParameterized', formResponses);
  }

  async createFormUpdateRealTime(FormResponce: 
    {hvac_settings: 
      {setpoint : number, 
      isOn : string, 
      selectedMode : Mode
      },
    room: {
      height: number,
      width: number,
      length: number
    },
    weatherTemperature: number,
    simulationType: number
  }) {
    return await httpService.post('/changeHVACsettings', FormResponce);
  }

  async sendEffAnomaly() 
  {
    return await httpService.post('/efficiencyAnomaly');
  }

  async restoreEffAnomaly()
  {
    return await httpService.post('/restoreEffAnomaly');
  }

  async sendThreshAnomaly()
  {
    return await httpService.post('/thresholdAnomaly');
  }

  async restoreThreshAnomaly()
  {
    return await httpService.post('/restoreThreshAnomaly');
  }

  async lossOfPowerAnomaly()
  {
    return await httpService.post('/lossOfPowerAnomaly');
  }

  async restoreFaultAnomaly()
  {
    return await httpService.post('/restoreFaultAnomaly');
  }

  async sendFaultAnomaly()
  {
    return await httpService.post('/faultAnomaly');
  }

  async createFormResponseRealTime(FormResponce: 
    {hvac_settings: 
      {setpoint : number, 
      isOn : string, 
      selectedMode : Mode
      },
    room: {
      height: number,
      width: number,
      length: number
    },
    weatherTemperature: number,
    simulationType: number
  }) {
    return await httpService.post('/setupRealTime', FormResponce);
  }


  async interruptSimulation(stop: boolean)
  {
    return await httpService.post('/interrupt', {stop_signal: stop});
  }

  async callSimulationParameterized() {
    return await httpService.post('/simulateParameterized');
  }
  async callSimulationRealTime() {
    return await httpService.post('/simulateRealTime');
  }
}

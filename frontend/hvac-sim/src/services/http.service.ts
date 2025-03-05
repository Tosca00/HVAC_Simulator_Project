import { Injectable, signal } from '@angular/core';
import axios from 'axios';
import { Mode } from 'fs';
import { RemoteComponent } from '../app/remote/remote.component';

export const httpService = axios.create({
  baseURL: 'http://localhost:8001'
});

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor() {
    this.resultPar.id = 'result';
   }

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
      selectedMode : Mode,
      selectedFanMode: string
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

  async sendEffAnomalyProg(dateFrom: string, dateTo:string)
  {
    await httpService.post('/sendEffAnomalyProg', {dateFrom, dateTo});
  }
  async sendthresholdAnomalyProg(dateFrom: string, dateTo:string)
  {
    await httpService.post('/sendthresholdAnomalyProg', {dateFrom, dateTo});
  }
  async sendLOPAnomalyProg(dateFrom: string)
  {
    await httpService.post('/sendLOPAnomalyProg', {dateFrom});
  }
  async sendFaultAnomalyProg(dateFrom: string, dateTo:string)
  {
    await httpService.post('/sendFaultAnomalyProg', {dateFrom, dateTo});
  }

  async createFormResponseRealTime(FormResponce: 
    {hvac_settings: 
      {setpoint : number, 
      isOn : string, 
      selectedMode : Mode,
      selectedFanMode: string
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


  private socket!: WebSocket;
  private resultPar: HTMLElement = document.createElement('p');
  connectWebSocket(url: string) {
    this.socket = new WebSocket(url);

    this.socket.onopen = (event) => {
      console.log('WebSocket is open:', event);
      return event;
    };

    this.socket.onmessage = (event) => {
      console.log('WebSocket message:', event.data);
      this.resultPar.id = 'result';
      this.resultPar.style.border = '1px solid #ccc';
      this.resultPar.style.backgroundColor = '#f9f9f9';
      this.resultPar.style.borderRadius = '5px';
      this.resultPar.style.padding = '10px';
      this.resultPar.innerHTML = '';
      const resultDiv = document.getElementById('resultContainer');
      if (resultDiv) 
      {
        const parsedData = event.data.split(',');
        console.log(parsedData);
        let tagArr = ['<b>Temperature: </b>', 'C <b> Setpoint: </b> ', 'C <b> Consuption: </b> ', ' W<b> Time: </b> ','<b> Mode: </b> ','<b> Ambient Temperature: </b> ','<b> Status: </b>', '<b> Fan Mode: </b>'];
        let i = 0;
        parsedData.forEach((data: string) => {
          if(i == 4)
          {
            data = data.split('.')[1];
          }
          if(i == 6)
          {
            data = data.split('.')[1];
          }
          this.resultPar.innerHTML += tagArr[i] + data;
          i++;
        });
        resultDiv.appendChild(this.resultPar);
      }
      return event;
    };

    this.socket.onclose = (event) => {
      console.log('WebSocket is closed:', event);
      return event;
    };

    this.socket.onerror = (event) => {
      console.error('WebSocket error:', event);
      return event;
    };

    return this.socket;
  }

  sendMessage(message: string) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    } else {
      console.error('WebSocket is not open. Ready state:', this.socket.readyState);
    }
  }

  closeWebSocket() {
    if (this.socket) {
      this.socket.close();
    }
  }
}

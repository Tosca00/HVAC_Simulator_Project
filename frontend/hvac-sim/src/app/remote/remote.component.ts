import { Component,Inject, ViewContainerRef, ViewChild, Renderer2, InjectionToken } from '@angular/core';
import { UserFormComponent } from '../user-form/user-form.component';
import { WeatherRoomComponent } from '../weather-room/weather-room.component';
import { ChartComponentComponent } from '../chart-component/chart-component.component';
import { OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';
import { HvacRealtimeFormComponent } from '../hvac-realtime-form/hvac-realtime-form.component';
import { AnomalyComponent } from '../anomaly/anomaly.component';

export const SIM_TYPE = new InjectionToken<number>('sim_type');

@Component({
  selector: 'app-remote',
  standalone: false,
  templateUrl: './remote.component.html',
  styleUrl: './remote.component.css'
})
export class RemoteComponent implements OnInit {

  title = 'remote-component';
  sim_type : number = 0;
  isRealTimeSimStarted : boolean = false;
  isOfflineSimEnded : boolean = false;

  simulationResultDownloadData: Array<any> = [];

  

  ngOnInit(): void {
  }
  userFormComponents : Array<UserFormComponent> = [];

  @ViewChild(ChartComponentComponent) chartComponent!: ChartComponentComponent

  @ViewChild(WeatherRoomComponent) weatherRoom!: WeatherRoomComponent;

  @ViewChild(HvacRealtimeFormComponent) hvacRealtimeForm!: HvacRealtimeFormComponent

  @ViewChild(AnomalyComponent) anomalyForm!: AnomalyComponent

  ngAfterViewInit() {
    console.log('WeatherRoomComponent ngAfterViewInit');
  }

  constructor(@Inject(SIM_TYPE) sim_type: number, private vrc_userForm : ViewContainerRef, private http: HttpService, private renderer: Renderer2)
  {
    this.sim_type = sim_type;
    if(this.sim_type == 0) 
    { 
      this.title = 'Parameterized Simulation';
      this.interruptSim();
    }
    else { this.title = 'Real Time Simulation'; }
  }

  AddFormRow() {
    const userComponent = this.vrc_userForm.createComponent(UserFormComponent);
    const formButtonsAndManagement = document.getElementById('formButtonsAndManagement');
    if (formButtonsAndManagement) {
      formButtonsAndManagement.appendChild(userComponent.location.nativeElement);
    }
    this.userFormComponents.push(userComponent.instance);
    this.p.style.display = 'none';
    this.p.textContent = '';
  }
  RemoveFormRow() {
    this.vrc_userForm.remove();
    this.userFormComponents.pop();
    this.p.style.display = 'none';
    this.p.textContent = '';
  }

  AddRealTimeResultRow(message: MessageEvent<any>)
  {
    const resParagraph = this.renderer.createElement('p');
    const resText = this.renderer.createText(message.data);
    this.renderer.appendChild(resParagraph, resText);
    const containerForm = document.getElementById('formContainer');
    if (containerForm) {
      this.renderer.appendChild(containerForm, resParagraph);
    }
  }

  showGraph() {
    console.log('Show Graph is still under construction');
    this.p.textContent = 'Show Graph is still under construction.';
    this.p.style.display = 'initial';
    const formButtonsAndManagement = document.getElementById('graph');
    if (formButtonsAndManagement) {
      formButtonsAndManagement.style.display = 'initial';
      formButtonsAndManagement.appendChild(this.p);
    }
  }

  DownloadResults() 
  {
    const csvContent = this.simulationResultDownloadData.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'simulation_results.csv';
    a.click();
  }

  simulation_status :HTMLElement = document.createElement('p');
  async interruptSim()
  {
    const result = await this.http.interruptSimulation(true);
    this.isRealTimeSimStarted = false;
    this.simulation_status.textContent = 'Simulation: Interrupted';
    const divToAppend = document.getElementById('resultContainer');
    if(divToAppend)
    {
      divToAppend.appendChild(this.simulation_status);
    }
    console.log(result.data);
  }
  
  getSimType() {
    return this.sim_type;
  }

  setSimType(sim_type: number) {
    this.sim_type = sim_type;
  }

  p : HTMLElement = document.createElement('p');
  downloadButton : HTMLElement = document.createElement('button');
  async createFormResponse() 
  {
    const formResponses = {
      responses: this.userFormComponents.map(component => ({
      date: component.date.slice(0, 19).replace('T', ' '),
      temperature: component.temperature,
      selectedMode: component.modes,
      isOn: component.isOn? "ON" : "OFF"
      })),
      weatherTemperature: this.weatherRoom.weatherTemperature,
      room: {
        height: this.weatherRoom.height,
        width: this.weatherRoom.width,
        length: this.weatherRoom.length
      },
      simulationType: this.sim_type
    };

    try {
      let offlineSimLoading_p = document.createElement('p');
      const downloadDiv = document.getElementById('submitAndDownloadDiv');
      offlineSimLoading_p.textContent = 'Loading...';
      if(downloadDiv)
      {
        downloadDiv.appendChild(offlineSimLoading_p);
      }
      const result = await this.http.createFormResponse(formResponses);
      const simulationResult = await this.http.callSimulationParameterized();
      console.log(simulationResult);
      console.log(typeof simulationResult.data.csv_content);
      this.simulationResultDownloadData = simulationResult.data.csv_content;
      console.log(this.simulationResultDownloadData);
      this.isOfflineSimEnded = true;

      
      this.p.textContent = simulationResult.data.message;
      document.body.appendChild(this.p);
      if(simulationResult.data.isResCorrect)
      {
        if(downloadDiv)
        {
          downloadDiv.removeChild(offlineSimLoading_p);
          this.downloadButton.textContent = 'Download Results';
          this.downloadButton.onclick = this.DownloadResults.bind(this);
          downloadDiv.appendChild(this.downloadButton);
        }
      }
      
    } catch (error) {
      console.error('Error in form response:', error);
    }
  }

  async manageSubmit() {
    console.log('Manage Submit'+ this.isRealTimeSimStarted);
    if(this.sim_type == 0) 
      {
        await this.createFormResponse();
      }
      else if(this.sim_type == 1 && !this.isRealTimeSimStarted) 
      {
        this.simulation_status.textContent = 'Simulation : Active';
        const divToAppend = document.getElementById('resultContainer');
        if(divToAppend)
        {
          divToAppend.appendChild(this.simulation_status);
        }
        await this.createFormResponceRealTime();
      }
      else
      {
        console.log('Real Time Simulation is already running');
        await this.createFormUpdateRealTime();
    }
  }

  async createFormUpdateRealTime()
  {
    const FormUpdate = {hvac_settings: 
    {setpoint : this.hvacRealtimeForm.setpoint, 
    isOn : this.hvacRealtimeForm.isOn? "ON" : "OFF", 
    selectedMode : this.hvacRealtimeForm.modes,
    selectedFanMode : this.hvacRealtimeForm.fanModes
    },
    room: {
      height: this.weatherRoom.height,
      width: this.weatherRoom.width,
      length: this.weatherRoom.length
    },
    weatherTemperature: this.weatherRoom.weatherTemperature,
    simulationType: this.sim_type
  };
    try {
      console.log('FormUpdate:');
      const result = await this.http.createFormUpdateRealTime(FormUpdate);
      console.log(result);
    } catch (error) {
      console.error('Error in form response:', error);
    }
  }


  private streamData: WebSocket | null = null;
  async createFormResponceRealTime() 
  {
    const FormResponce = {hvac_settings: 
    {setpoint : this.hvacRealtimeForm.setpoint, 
    isOn : this.hvacRealtimeForm.isOn? "ON" : "OFF", 
    selectedMode : this.hvacRealtimeForm.modes,
    selectedFanMode : this.hvacRealtimeForm.fanModes
    },
    room: {
      height: this.weatherRoom.height,
      width: this.weatherRoom.width,
      length: this.weatherRoom.length
    },
    weatherTemperature: this.weatherRoom.weatherTemperature,
    simulationType: this.sim_type
  };
    try {
      const websocketUrl = 'http://localhost:8001/ws';
      this.streamData = this.http.connectWebSocket(websocketUrl);
      this.isRealTimeSimStarted = true;
      const result = await this.http.createFormResponseRealTime(FormResponce);
      const simulationResult = await this.http.callSimulationRealTime();
      console.log(simulationResult);
    } catch (error) {
      console.error('Error in form response:', error);
    }
  }
}

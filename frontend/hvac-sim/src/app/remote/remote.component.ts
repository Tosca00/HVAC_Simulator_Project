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
    this.userFormComponents.push(userComponent.instance);
  }
  RemoveFormRow() {
    this.vrc_userForm.remove();
    this.userFormComponents.pop();
  }

  showGraph() {
    console.log('Show Graph is still under construction');
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

  async interruptSim()
  {
    const result = await this.http.interruptSimulation(true);
    this.isRealTimeSimStarted = false;
    console.log(result.data);
  }
  
  getSimType() {
    return this.sim_type;
  }

  setSimType(sim_type: number) {
    this.sim_type = sim_type;
  }

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
      const result = await this.http.createFormResponse(formResponses);
      const simulationResult = await this.http.callSimulationParameterized();
      //const simulationResult_CSV = simulationResult.data.csv_content.map((row: any) => row.join(',')).join('\n');
      //this.chartComponent.dataForGraph(simulationResult_CSV);
      console.log(simulationResult);
      console.log(typeof simulationResult.data.csv_content);
      this.simulationResultDownloadData = simulationResult.data.csv_content;
      console.log(this.simulationResultDownloadData);
      this.isOfflineSimEnded = true;
      const downloadButton = document.getElementById('downloadButton');
      if(downloadButton) {
        downloadButton.style.visibility = 'visible';
      }
    } catch (error) {
      console.error('Error in form response:', error);
    }

    //console.log(formResponses);
  }

  async manageSubmit() {
    if(this.sim_type == 0) 
      {
        await this.createFormResponse();
      }
      else if(this.sim_type == 1 && !this.isRealTimeSimStarted) 
      {
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
    selectedMode : this.hvacRealtimeForm.modes
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
      const result = await this.http.createFormUpdateRealTime(FormUpdate);
      console.log(result);
    } catch (error) {
      console.error('Error in form response:', error);
    }
  }

  async createFormResponceRealTime() 
  {
    const FormResponce = {hvac_settings: 
    {setpoint : this.hvacRealtimeForm.setpoint, 
    isOn : this.hvacRealtimeForm.isOn? "ON" : "OFF", 
    selectedMode : this.hvacRealtimeForm.modes
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
      this.isRealTimeSimStarted = true;
      const result = await this.http.createFormResponseRealTime(FormResponce);
      const simulationResult = await this.http.callSimulationRealTime();
      console.log(simulationResult);
      this.isRealTimeSimStarted = false;
    } catch (error) {
      console.error('Error in form response:', error);
    }
  }
}

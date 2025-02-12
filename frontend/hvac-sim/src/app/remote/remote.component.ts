import { Component,Inject, ViewContainerRef, ViewChild, AfterViewInit, InjectionToken } from '@angular/core';
import { UserFormComponent } from '../user-form/user-form.component';
import { WeatherRoomComponent } from '../weather-room/weather-room.component';
import { ChartComponentComponent } from '../chart-component/chart-component.component';
import { OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';

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

  ngOnInit(): void {
  }
  userFormComponents : Array<UserFormComponent> = [];

  @ViewChild(ChartComponentComponent) chartComponent!: ChartComponentComponent

  @ViewChild(WeatherRoomComponent) weatherRoom!: WeatherRoomComponent;

  ngAfterViewInit() {
    console.log('WeatherRoomComponent ngAfterViewInit');
  }

  constructor(@Inject(SIM_TYPE) sim_type: number, private vrc_userForm : ViewContainerRef, private http: HttpService) 
  {
    this.sim_type = sim_type;
    if(this.sim_type == 0) { this.title = 'Parameterized Simulation'; }
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

  }
  
  getSimType() {
    return this.sim_type;
  }

  setSimType(sim_type: number) {
    this.sim_type = sim_type;
  }

  async createFormResponse() {
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
      const simulationResult = await this.http.callSimulation();
      //const simulationResult_CSV = simulationResult.data.csv_content.map((row: any) => row.join(',')).join('\n');
      //this.chartComponent.dataForGraph(simulationResult_CSV);
      console.log(simulationResult);
      
    } catch (error) {
      console.error('Error in form response:', error);
    }

    console.log(formResponses);
  }
}

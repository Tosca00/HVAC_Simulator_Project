import { Component, ViewContainerRef, ViewChild } from '@angular/core';
import { UserFormComponent } from './user-form/user-form.component';
import { WeatherRoomComponent } from './weather-room/weather-room.component';
import { OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';
import { Mode } from './user-form/user-form.component';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit{
  title = 'hvac-sim';
  userFormComponents : Array<UserFormComponent> = [];

  @ViewChild(WeatherRoomComponent) weatherRoom!: WeatherRoomComponent;

  ngAfterViewInit() {
    console.log('WeatherRoomComponent ngAfterViewInit');
  }

  constructor(private vrc_userForm : ViewContainerRef, private vrc_weatherRoom: ViewContainerRef, private http: HttpService) {}

  ngOnInit() {
    console.log('AppComponent ngOnInit');
  }

  AddFormRow() {
    const userComponent = this.vrc_userForm.createComponent(UserFormComponent);
    this.userFormComponents.push(userComponent.instance);
  }
  RemoveFormRow() {
    this.vrc_userForm.remove();
    this.userFormComponents.pop();
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
      }
    };

    try {
      const result = await this.http.createFormResponse(formResponses);
      console.log(result.data);
      const simulationResult = await this.http.callSimulation();
      console.log(simulationResult.data);
    } catch (error) {
      console.error('Error submitting form response:', error);
    }

    console.log(formResponses);
  }
}

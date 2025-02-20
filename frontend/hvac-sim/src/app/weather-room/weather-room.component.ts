import { Component } from '@angular/core';

@Component({
  selector: 'app-weather-room',
  standalone: false,
  
  templateUrl: './weather-room.component.html',
  styleUrl: './weather-room.component.css'
})
export class WeatherRoomComponent {
    height: number = 1;
    width: number = 1;
    length: number = 1;
    weatherTemperature: number = 20;

    isIntegerOrFloat(value: number): boolean {
      return Number.isInteger(value)
    }

    constructor() {
      console.log('WeatherRoomComponent constructor');
    }
}

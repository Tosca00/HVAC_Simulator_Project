import { Component } from '@angular/core';

@Component({
  selector: 'app-weather-room',
  standalone: false,
  
  templateUrl: './weather-room.component.html',
  styleUrl: './weather-room.component.css'
})
export class WeatherRoomComponent {
    height: number = 0;
    width: number = 0;
    length: number = 0;
    weatherTemperature: number = 0;

    isIntegerOrFloat(value: number): boolean {
      return Number.isInteger(value)
    }

    constructor() {
      console.log('WeatherRoomComponent constructor');
    }
}

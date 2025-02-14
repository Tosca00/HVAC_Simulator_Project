import { Component } from '@angular/core';
import { Mode } from '../user-form/user-form.component';

@Component({
  selector: 'app-hvac-realtime-form',
  standalone: false,
  
  templateUrl: './hvac-realtime-form.component.html',
  styleUrl: './hvac-realtime-form.component.css'
})
export class HvacRealtimeFormComponent {

  constructor() { }

  title = 'hvac-realtime-form';
  
  setpoint: number = 0;

  isOn = false;
  public modes:Mode = Mode.NO_MODE;
  selectedMode = Object.values(Mode);
  


  onFormSubmit() {
    console.log('Form submitted');
  }
}

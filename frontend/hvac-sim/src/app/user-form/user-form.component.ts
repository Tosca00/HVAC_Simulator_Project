import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';
import { Data } from '@angular/router';
import { DatePipe } from '@angular/common';
export enum Mode {
  COOL = 'COOLING',
  HEAT = 'HEATING',
  NO_MODE = 'NO_MODE'
}

@Component({
  selector: 'app-user-form',
  standalone: false,
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.css']
})
export class UserFormComponent implements OnInit {
  
  temperature: number = 0;
  date: string = new Date().toISOString().substring(0, 16);
  

  isOn = false;
  public modes:Mode = Mode.NO_MODE;
  selectedMode = Object.values(Mode);

  constructor(private http: HttpService) {
    console.log('UserFormComponent constructor');
  }

  async ngOnInit() 
  {
    console.log('UserFormComponent ngOnInit');
  }
  

  isInteger(value: number): boolean {
    return Number.isInteger(value);
  }
}

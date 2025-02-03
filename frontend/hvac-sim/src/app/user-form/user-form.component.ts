import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';
enum Mode {
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
  date: string = new Date().toISOString().slice(0, 19).replace('T', ' ');

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

  async createFormResponse()
  {
    const formResponse = {
      date: this.date.replace('T',' '),
      temperature: this.temperature,
      selectedMode: this.selectedMode,
      isOn: this.isOn
    };

    const result = await this.http.createFormResponse(formResponse);
    console.log(result.data);
  }

  isInteger(value: number): boolean {
    return Number.isInteger(value);
  }

  writeTemp()
  {
    console.log(this.date);
    console.log(this.temperature);
    console.log(this.selectedMode);
    console.log(this.isOn);
  }
}

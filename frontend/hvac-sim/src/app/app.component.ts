import { Component, ViewContainerRef } from '@angular/core';
import { UserFormComponent } from './user-form/user-form.component';
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
  
  constructor(private vrc : ViewContainerRef, private http: HttpService) {}

  ngOnInit() {
    console.log('AppComponent ngOnInit');
  }

  AddFormRow() {
    const userComponent = this.vrc.createComponent(UserFormComponent);
    this.userFormComponents.push(userComponent.instance);
  }
  RemoveFormRow() {
    this.vrc.remove();
    this.userFormComponents.pop();
  }

  async createFormResponse() {
    const formResponses = {
      responses: this.userFormComponents.map(component => ({
      date: component.date,
      temperature: component.temperature,
      selectedMode: component.modes,
      isOn: component.isOn? "ON" : "OFF"
      }))
    };

    try {
      const result = await this.http.createFormResponse(formResponses);
      console.log(result.data);
    } catch (error) {
      console.error('Error submitting form response:', error);
    }

    console.log(formResponses);
  }
}

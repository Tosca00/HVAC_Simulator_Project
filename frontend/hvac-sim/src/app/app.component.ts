import { Component, ViewContainerRef } from '@angular/core';
import $ from 'jquery';
import { Renderer2 } from '@angular/core';
import { UserFormComponent } from './user-form/user-form.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'hvac-sim';
  constructor(private vrc : ViewContainerRef) {}

  AddFormRow() {
    this.vrc.createComponent(UserFormComponent);
  }
  RemoveFormRow() {
    this.vrc.remove();
  }
}

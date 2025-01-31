import { Component } from '@angular/core';

@Component({
  selector: 'app-user-form',
  standalone: false,
  
  templateUrl: './user-form.component.html',
  styleUrl: './user-form.component.css'
})
export class UserFormComponent {
  temperature: number = 0;

  isInteger(value: number): boolean {
    return Number.isInteger(value);
  }

  writeTemp()
  {
    console.log(this.temperature);
  }
}

import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit {
  title = 'hvac-sim';
 

  constructor(private http: HttpService) {
    console.log('AppComponent constructor');
  }

  async ngOnInit() {
    const FormResponce = await this.http.getForm();
    console.log(FormResponce);
  }
}

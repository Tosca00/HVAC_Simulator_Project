import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';

@Component({
  selector: 'app-anomaly',
  standalone: false,
  
  templateUrl: './anomaly.component.html',
  styleUrl: './anomaly.component.css'
})
export class AnomalyComponent implements OnInit {

  isEffset: boolean = false;
  isThreshset: boolean = false;
  isFaultset: boolean = false;

  ngOnInit(): void {
    console.log('AnomalyComponent ngOnInit');
  }

  constructor(private http: HttpService) { }

  async efficiency()
  {
    if(!this.isEffset) 
    {
    const response = await this.http.sendEffAnomaly();
    this.isEffset = true;
    console.log(response.data.message);
    }
    else
    {
      const response = await this.http.restoreEffAnomaly();
      this.isEffset = false;
      console.log(response.data.message);
    }
  }

  async threshold()
  {
    if(!this.isThreshset) 
    {
    const response = await this.http.sendThreshAnomaly();
    this.isThreshset = true;
    console.log(response.data.message);
    }
    else
    {
      const response = await this.http.restoreThreshAnomaly();
      this.isThreshset = false;
      console.log(response.data.message);
    }

  }

  async lossOfPower()
  {
    const response = await this.http.lossOfPowerAnomaly();
    console.log(response.data.message);
  }

  async fault()
  {
    if(!this.isFaultset) 
    {
    const response = await this.http.sendFaultAnomaly();
    this.isFaultset = true;
    console.log(response.data.message);
    }
    else
    {
      const response = await this.http.restoreFaultAnomaly();
      this.isFaultset = false;
      console.log(response.data.message);
    }
  }

}

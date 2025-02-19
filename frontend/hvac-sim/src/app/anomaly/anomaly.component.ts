import { Component, Input,Renderer2 } from '@angular/core';
import { OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';
import { response } from 'express';

@Component({
  selector: 'app-anomaly',
  standalone: false,
  
  templateUrl: './anomaly.component.html',
  styleUrl: './anomaly.component.css'
})
export class AnomalyComponent implements OnInit {

  @Input() sim_type:number = 0;

  isEffset: boolean = false;
  isThreshset: boolean = false;
  isFaultset: boolean = false;
  dateFrom: string = new Date().toISOString().substring(0, 16);
  dateTo: string = new Date().toISOString().substring(0, 16);
  progAnomalyType: string = '';

  ngOnInit(): void {
    console.log('AnomalyComponent ngOnInit');
    console.log('sim_type: ' + this.sim_type);
  }

  constructor(private http: HttpService,private rend: Renderer2) { }

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

  async efficiency_prog()
  {
    console.log('efficiency_prog');
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

  async threshold_prog()
  {
    console.log('threshold_prog');
  }

  async lossOfPower()
  {
    const response = await this.http.lossOfPowerAnomaly();
    console.log(response.data.message);
  }

  async lossOfPower_prog()
  {
    console.log('lossOfPower_prog');
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

  async fault_prog()
  {
    console.log('fault_prog');
  }

  showDateDiv(event: Event)
  {
    this.progAnomalyType = (event.target as HTMLElement).id;
    const dateDiv = document.getElementById('dateDiv');
    if(dateDiv) {
      dateDiv.style.visibility = 'visible';
      console.log(this.progAnomalyType);
      if(this.progAnomalyType === 'lOP')
      {
        const dateToButton = document.getElementById('dateTo');
        if(dateToButton)  {dateToButton.style.visibility = 'hidden';}
      }
      else
      {
        const dateToButton = document.getElementById('dateTo');
      if(dateToButton)  {dateToButton.style.visibility = 'visible';}
      }
    }
  }
  async sendProgAnomaly()
  {
    
    switch (this.progAnomalyType) {
      case 'efficiency':
        this.http.sendEffAnomalyProg(this.dateFrom.slice(0, 19).replace('T', ' '), this.dateTo.slice(0, 19).replace('T', ' '));
        break;
      case 'threshold':
        this.http.sendthresholdAnomalyProg(this.dateFrom.slice(0, 19).replace('T', ' '), this.dateTo.slice(0, 19).replace('T', ' '));
        break;
      case 'lOP':
        this.http.sendLOPAnomalyProg(this.dateFrom.slice(0, 19).replace('T', ' '));
        break;
      case 'fault':
        this.http.sendFaultAnomalyProg(this.dateFrom.slice(0, 19).replace('T', ' '), this.dateTo.slice(0, 19).replace('T', ' '));
        break;
      default:
        console.log('error');
        break;
    }
  }

  hideDateDiv()
  {
    const dateDiv = document.getElementById('dateDiv');
    if(dateDiv) {
      dateDiv.style.visibility = 'hidden';
    }
  }

}

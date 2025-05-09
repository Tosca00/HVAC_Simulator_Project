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


  dateFrom: string = new Date().toISOString().substring(0, 16);
  dateTo: string = new Date().toISOString().substring(0, 16);
  progAnomalyType: string = '';

  //per anomalie
  isEffset: boolean = false;
  isThreshset: boolean = false;
  isFaultset: boolean = false;

  ngOnInit(): void {
    console.log('AnomalyComponent ngOnInit');
    console.log('sim_type: ' + this.sim_type);
  }

  constructor(private http: HttpService,private rend: Renderer2) 
  { 
    this.effAnomalyText.style.display = 'none';
    this.thresholdAnomalyText.style.display = 'none';
    this.faultAnomalyText.style.display = 'none';
    this.lossOfPowerAnomalyText.style.display = 'none';
  }

  //efficiency anomaly
  effAnomalyText : HTMLElement = document.createElement('p');
  async efficiency()
  {
    if(!this.isEffset) 
    {
    const response = await this.http.sendEffAnomaly();
    this.isEffset = true;
    console.log(response.data.message);
    this.effAnomalyText.textContent = response.data.message;   
    }
    else
    {
      const response = await this.http.restoreEffAnomaly();
      this.isEffset = false;
      console.log(response.data.message);
      this.effAnomalyText.textContent = response.data.message;   
    }
    this.effAnomalyText.innerHTML += '<br>';
    const anomalyDiv = document.getElementById('efficiencyText');
    if(anomalyDiv) 
    {
      const anomaliesLogText = document.getElementById('anomaliesLogText');
      if(anomaliesLogText) {anomaliesLogText.style.display = 'initial';}
      this.effAnomalyText.style.display = 'initial';
      anomalyDiv.appendChild(this.effAnomalyText);
    }
  }

  async efficiency_prog()
  {
    console.log('efficiency_prog');
  }


  //threshold anomaly
  thresholdAnomalyText : HTMLElement = document.createElement('p');
  async threshold()
  {
    if(!this.isThreshset) 
    {
    const response = await this.http.sendThreshAnomaly();
    this.isThreshset = true;
    console.log(response.data.message);
    this.thresholdAnomalyText.textContent = response.data.message;
    }
    else
    {
      const response = await this.http.restoreThreshAnomaly();
      this.isThreshset = false;
      console.log(response.data.message);
      this.thresholdAnomalyText.textContent = response.data.message;
    }
    this.thresholdAnomalyText.innerHTML += '<br>';
    const anomalyDiv = document.getElementById('thresholdText');
    if(anomalyDiv) 
    {
      const anomaliesLogText = document.getElementById('anomaliesLogText');
      if(anomaliesLogText) {anomaliesLogText.style.display = 'initial';}
      this.thresholdAnomalyText.style.display = 'initial';
      anomalyDiv.appendChild(this.thresholdAnomalyText);
    }
  }

  async threshold_prog()
  {
    console.log('threshold_prog');
  }

  //LOP anomaly
  lossOfPowerAnomalyText : HTMLElement = document.createElement('p');
  async lossOfPower()
  {
    this.lossOfPowerAnomalyText.textContent = 'Loss of Power Anomaly is active, it will end automatically in 30 seconds.';
    this.lossOfPowerAnomalyText.innerHTML += '<br>';
    const anomalyDiv = document.getElementById('LOPText');
    if(anomalyDiv) 
    {
      const anomaliesLogText = document.getElementById('anomaliesLogText');
      if(anomaliesLogText) {anomaliesLogText.style.display = 'initial';}
      this.lossOfPowerAnomalyText.style.display = 'initial';
      anomalyDiv.appendChild(this.lossOfPowerAnomalyText);
    }
    const response = await this.http.lossOfPowerAnomaly();
    console.log(response.data.message);
    this.lossOfPowerAnomalyText.textContent = response.data.message;
    this.lossOfPowerAnomalyText.innerHTML += '<br>';
  }

  async lossOfPower_prog()
  {
    console.log('lossOfPower_prog');
  }

  //fault anomaly
  faultAnomalyText : HTMLElement = document.createElement('p');
  async fault()
  {
    if(!this.isFaultset) 
    {
      const response = await this.http.sendFaultAnomaly();
      this.isFaultset = true;
      console.log(response.data.message);
      this.faultAnomalyText.textContent = response.data.message;
    }
    else
    {
      const response = await this.http.restoreFaultAnomaly();
      this.isFaultset = false;
      console.log(response.data.message);
      this.faultAnomalyText.textContent = response.data.message;
    }
    this.faultAnomalyText.innerHTML += '<br>';
    const anomalyDiv = document.getElementById('FaultText');
    if(anomalyDiv) 
    {
      const anomaliesLogText = document.getElementById('anomaliesLogText');
      if(anomaliesLogText) {anomaliesLogText.style.display = 'initial';}
      this.faultAnomalyText.style.display = 'initial';
      anomalyDiv.appendChild(this.faultAnomalyText);
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
      dateDiv.style.display = 'flex';
      console.log(this.progAnomalyType);
      if(this.progAnomalyType === 'lOP')
      {
        const dateToButton = document.getElementById('dateTo');
        if(dateToButton)  {dateToButton.style.display = 'none';}
      }
      else
      {
        const dateToButton = document.getElementById('dateTo');
        if(dateToButton)  {dateToButton.style.display = 'inline-block';}
      }
    }
    const submitButton = document.getElementById('submitButton');
    if(submitButton) {
      submitButton.style.display = 'inline-block';
    }
  }

  //sends the anomaly to the backend in programmed mode
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

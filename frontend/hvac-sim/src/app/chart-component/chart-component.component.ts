import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { HttpService } from '../../services/http.service';
//import * as Papa from 'papaparse';

@Component({
  selector: 'app-chart-component',
  standalone: false,
  
  templateUrl: './chart-component.component.html',
  styleUrl: './chart-component.component.css'
})
export class ChartComponentComponent implements OnInit {

  csvData: any[] = [];
  chartLabels: string[] = [];
  chartData: number[] = [];

  ngOnInit(): void {
    console.log('ChartComponentComponent ngOnInit');
  }

  constructor(private http: HttpService ) { console.log('ChartComponentComponent constructor'); }

  onFileSelect(event: any) {
    const file = event.target.files[0];
    if(file)
    {
      console.log(file);
    }

  }

}

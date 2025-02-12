import { Injectable } from '@angular/core';
import axios from 'axios';
import { Mode } from 'fs';

export const httpService = axios.create({
  baseURL: 'http://localhost:8001'
});

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor() { }

  async createFormResponse(formResponses: {
    responses: {
        date: string;
        temperature: number;
        selectedMode: Mode;
        isOn: string;
    }[];
  }) {
    return await httpService.post('/', formResponses);
  }

  async callSimulation() {
    return await httpService.post('/simulate');
  }
}

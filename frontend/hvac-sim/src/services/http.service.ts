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

  async createFormResponse(formResponse: {date: string, temperature: number, selectedMode: Mode[], isOn: boolean}) {
    return await httpService.post('/', formResponse);
  }
}

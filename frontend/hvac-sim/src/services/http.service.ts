import { Injectable } from '@angular/core';
import axios from 'axios';

export const httpService = axios.create({
  baseURL: 'http://localhost:8001'
});

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor() { }

  async getForm() {
    const httpResponce = await httpService.get<any>('/');
    return httpResponce.data;
  }
}

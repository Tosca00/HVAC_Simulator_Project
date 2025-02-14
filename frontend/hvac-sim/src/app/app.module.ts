import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule,ReactiveFormsModule } from '@angular/forms';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UserFormComponent } from './user-form/user-form.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatOptionModule } from '@angular/material/core';
import { WeatherRoomComponent } from './weather-room/weather-room.component';
import { ChartComponentComponent } from './chart-component/chart-component.component';
import { RemoteComponent } from './remote/remote.component';
import { HvacRealtimeFormComponent } from './hvac-realtime-form/hvac-realtime-form.component';
import { AnomalyComponent } from './anomaly/anomaly.component';


@NgModule({
  declarations: [
    AppComponent,
    UserFormComponent,
    WeatherRoomComponent,
    ChartComponentComponent,
    RemoteComponent,
    HvacRealtimeFormComponent,
    AnomalyComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatOptionModule,
    MatSelectModule,
    MatCheckboxModule,
    ReactiveFormsModule 
  ],
  providers: [
    provideClientHydration(withEventReplay()),
    provideAnimationsAsync()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

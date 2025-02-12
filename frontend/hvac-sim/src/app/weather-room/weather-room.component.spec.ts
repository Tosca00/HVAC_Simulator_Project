import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WeatherRoomComponent } from './weather-room.component';

describe('WeatherRoomComponent', () => {
  let component: WeatherRoomComponent;
  let fixture: ComponentFixture<WeatherRoomComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [WeatherRoomComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WeatherRoomComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

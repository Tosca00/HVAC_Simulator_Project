import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HvacRealtimeFormComponent } from './hvac-realtime-form.component';

describe('HvacRealtimeFormComponent', () => {
  let component: HvacRealtimeFormComponent;
  let fixture: ComponentFixture<HvacRealtimeFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HvacRealtimeFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HvacRealtimeFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

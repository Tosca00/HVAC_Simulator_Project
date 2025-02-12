import { Component, ViewChild, ViewContainerRef,ComponentFactoryResolver, OnInit} from '@angular/core';
import { RemoteComponent, SIM_TYPE } from './remote/remote.component';
import { Injector } from '@angular/core';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: false,
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit{
  title = 'hvac-sim';
  
  @ViewChild(RemoteComponent) remote!: RemoteComponent;
  
  constructor(private vrc_remote : ViewContainerRef,private resolver: ComponentFactoryResolver, private injector: Injector) 
  {}

  ngOnInit() {
    console.log('AppComponent ngOnInit');
  }

  showParamSim() {
    if(this.vrc_remote.length > 0) {
      this.vrc_remote.clear();
    }
    const factory = this.resolver.resolveComponentFactory(RemoteComponent);
    const injector = Injector.create({providers: [{provide: SIM_TYPE, useValue: 0}]});
    this.vrc_remote.createComponent(factory, 0, injector);

    const otherButton = document.getElementById('pr_sim');
    if(otherButton) {
      if (otherButton.style.visibility === 'visible') {
        otherButton.style.visibility = 'hidden';
      } else {
        otherButton.style.display = 'visible';
      }
    }
  }

  showRealTimeSim() {
    if(this.vrc_remote.length > 0) {
      this.vrc_remote.clear();
    }
    const factory = this.resolver.resolveComponentFactory(RemoteComponent);
    const injector = Injector.create({providers: [{provide: SIM_TYPE, useValue: 1}]});
    this.vrc_remote.createComponent(factory, 0, injector);
    const otherButton = document.getElementById('rt_sim');
    if(otherButton) {
      if (otherButton.style.visibility === 'visible') {
        otherButton.style.visibility = 'hidden';
      } else {
        otherButton.style.display = 'visible';
      }
    }
  }
}

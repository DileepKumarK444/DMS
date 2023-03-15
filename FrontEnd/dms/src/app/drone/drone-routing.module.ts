import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DroneDetailsComponent } from '../drone-details/drone-details.component';
import { LogsComponent } from '../logs/logs.component';
import { ReportsComponent } from '../reports/reports.component';
import { MoreInfoComponent } from '../more-info/more-info.component';

const routes: Routes = [

{ path: 'drone-details/:id', component: DroneDetailsComponent},
{ path: 'drone-details/:id/logs', component: LogsComponent},
{ path: 'drone-details/:id/reports', component: ReportsComponent},
{ path: 'drone-details/:id/more', component: MoreInfoComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DroneRoutingModule { }

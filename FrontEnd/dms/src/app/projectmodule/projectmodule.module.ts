import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ProjectmoduleRoutingModule } from './projectmodule-routing.module';
import { ProjectmoduleComponent } from './components/projectmodule/projectmodule.component';


@NgModule({
  declarations: [
    ProjectmoduleComponent
  ],
  imports: [
    CommonModule,
    ProjectmoduleRoutingModule
  ]
})
export class ProjectmoduleModule { }

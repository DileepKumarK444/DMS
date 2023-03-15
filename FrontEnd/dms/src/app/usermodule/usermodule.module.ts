import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { UsermoduleRoutingModule } from './usermodule-routing.module';
import { UsermoduleComponent } from './components/usermodule/usermodule.component';


@NgModule({
  declarations: [
    UsermoduleComponent
  ],
  imports: [
    CommonModule,
    UsermoduleRoutingModule
  ]
})
export class UsermoduleModule { }

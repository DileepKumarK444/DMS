import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';

// import { DashboardComponent } from './dashboard/dashboard.component';
// import { CustomerComponent } from './customer/customer.component';
// import { ProfileComponent } from './profile/profile.component';
// import { DroneDetailsComponent } from './drone-details/drone-details.component';
// import { SubUsersComponent } from './sub-users/sub-users.component';
// import { ProjectComponent } from './project/project.component';
// import { PilotComponent } from './pilot/pilot.component';
// import { SubUserListComponent } from './sub-user-list/sub-user-list.component';
// import { ProjectListComponent } from './project-list/project-list.component';
// import { SubUserEditComponent } from './sub-user-edit/sub-user-edit.component';
// import { ProjectEditComponent } from './project-edit/project-edit.component';
// import { ProfileEditComponent } from './profile-edit/profile-edit.component';
// import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
// import { LogsComponent } from './logs/logs.component';
// import { ReportsComponent } from './reports/reports.component';
// import { MoreInfoComponent } from './more-info/more-info.component';


const routes: Routes = [
  { path: 'login', component: LoginComponent},
  { path: '', component: LoginComponent},
  { path: 'forgot-password', component: ForgotPasswordComponent},
  {
    path: 'avm',
    // loadChildren: "./first/first.module#FirstModule"
    loadChildren: () => import('./first/first.module').then(m => m.FirstModule)
  },
  {
    path: 'avmproject',
    loadChildren: () => import('./projectmodule/projectmodule.module').then(m => m.ProjectmoduleModule)
  },
  {
    path: 'avmuser',
    loadChildren: () => import('./usermodule/usermodule.module').then(m => m.UsermoduleModule)
  },
  {
    path: 'drone',
    loadChildren: () => import('./drone/drone.module').then(m => m.DroneModule)
  },
  { path: '**', component: LoginComponent }

];

// const routes: Routes = [{ path: 'login', component: LoginComponent},
// { path: '', component: LoginComponent},
// { path: 'dashboard', component: DashboardComponent},
// { path: 'customer', component: CustomerComponent},
// { path: 'profile', component: ProfileComponent},
// { path: 'drone-details/:id', component: DroneDetailsComponent},
// { path: 'sub-users', component: SubUsersComponent},
// { path: 'pilot', component: PilotComponent},
// { path: 'project', component: ProjectComponent},
// { path: 'sub-user-list', component: SubUserListComponent},
// { path: 'project-list', component: ProjectListComponent},
// { path: 'update-user/:id', component: SubUserEditComponent},
// { path: 'update-project/:id', component: ProjectEditComponent},
// { path: 'update-profile/:id', component: ProfileEditComponent},
// { path: 'forgot-password', component: ForgotPasswordComponent},
// { path: 'drone-details/:id/logs', component: LogsComponent},
// { path: 'drone-details/:id/reports', component: ReportsComponent},
// { path: 'drone-details/:id/more', component: MoreInfoComponent},
// { path: '**', component: LoginComponent }];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

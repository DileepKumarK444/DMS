import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { AuthInterceptor } from './services/auth-interceptor';
import { FooterComponent } from './pages/footer/footer.component';
import { HeaderComponent } from './pages/header/header.component';
import { CustomerComponent } from './customer/customer.component';
import { ProfileComponent } from './profile/profile.component';
import { DroneDetailsComponent } from './drone-details/drone-details.component';
import { SubUsersComponent } from './sub-users/sub-users.component';
import { ProjectComponent } from './project/project.component';
import { PilotComponent } from './pilot/pilot.component';
import { SubUserListComponent } from './sub-user-list/sub-user-list.component';
import { ProjectListComponent } from './project-list/project-list.component';
import { SubUserEditComponent } from './sub-user-edit/sub-user-edit.component';
import { ProjectEditComponent } from './project-edit/project-edit.component';
import { ProfileEditComponent } from './profile-edit/profile-edit.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { LogsComponent } from './logs/logs.component';
import { ReportsComponent } from './reports/reports.component';
import { MoreInfoComponent } from './more-info/more-info.component';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatTableModule } from '@angular/material/table'  
import { MatFormFieldModule } from '@angular/material/form-field';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatInputModule} from '@angular/material/input';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatSortModule } from '@angular/material/sort'; 
// import { MatDatepickerModule } from '@angular/material/datepicker';
// import { MatNativeDateModule } from '@angular/material/core';
import { MomentDateModule } from '@angular/material-moment-adapter';
import { MatToolbarModule } from '@angular/material/toolbar'; 
import { MatCardModule } from '@angular/material/card';
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    DashboardComponent,
    FooterComponent,
    HeaderComponent,
    CustomerComponent,
    ProfileComponent,
    DroneDetailsComponent,
    SubUsersComponent,
    ProjectComponent,
    PilotComponent,
    SubUserListComponent,
    ProjectListComponent,
    SubUserEditComponent,
    ProjectEditComponent,
    ProfileEditComponent,
    ForgotPasswordComponent,
    LogsComponent,
    ReportsComponent,
    MoreInfoComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    NoopAnimationsModule,
    MatTableModule,
    MatFormFieldModule,
    MatPaginatorModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MomentDateModule,
    MatSortModule,
    MatToolbarModule,
    MatCardModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

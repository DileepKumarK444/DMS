import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SubUsersComponent } from '../sub-users/sub-users.component';
import { SubUserListComponent } from '../sub-user-list/sub-user-list.component';
import { SubUserEditComponent } from '../sub-user-edit/sub-user-edit.component';

const routes: Routes = [

  { path: 'sub-users', component: SubUsersComponent},
  { path: 'sub-user-list', component: SubUserListComponent},
  { path: 'update-user/:id', component: SubUserEditComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsermoduleRoutingModule { }

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProjectComponent } from '../project/project.component';
import { ProjectListComponent } from '../project-list/project-list.component';
import { ProjectEditComponent } from '../project-edit/project-edit.component';

const routes: Routes = [

{ path: 'project', component: ProjectComponent},
{ path: 'project-list', component: ProjectListComponent},
{ path: 'update-project/:id', component: ProjectEditComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProjectmoduleRoutingModule { }

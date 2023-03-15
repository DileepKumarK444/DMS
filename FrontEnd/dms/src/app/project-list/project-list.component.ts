import { AfterViewInit, Component, ViewChild, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import { environment } from '../../environments/environment';
@Component({
  selector: 'app-project-list',
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.scss']
})
export class ProjectListComponent implements OnInit {
  dataSource:any;
  constructor(private AuthService:AuthService, 
    private router: Router) { }
    displayedColumns: string[] = ['id', 'project_name', 'mission_commander_id__first_name', 'start_date','end_date','action'];
    @ViewChild(MatPaginator) paginator: MatPaginator;
    @ViewChild(MatSort) sort: MatSort;

    
    applyFilter(event: Event) {
      const filterValue = (event.target as HTMLInputElement).value;
      this.dataSource.filter = filterValue.trim().toLowerCase();
  
      if (this.dataSource.paginator) {
        this.dataSource.paginator.firstPage();
      }
    }
  custid: any = '';
  projectlist: any = '';
  error: string = '';
  del_id:any;
  displayStyle = "none";
  pageSize = environment.TABLE_ROW_LIMIT;
  permission: any;
  projectadd_permission: boolean= false;
  projectedit_permission: boolean= false;
  projectdelete_permission: boolean= false;


  ngOnInit(): void {
    // let query = {
    //   customer_id: this.custid,
    // }
    this.AuthService.logincheck();
    // this.custid = this.AuthService.getCustomerid();

    this.permission = localStorage.getItem("permissions");
    this.projectadd_permission = this.permission.includes('project-add');
    this.projectedit_permission = this.permission.includes('project-edit');
    this.projectdelete_permission = this.permission.includes('project-delete');


    this.AuthService.getProjectList().subscribe((data: any)=>{
      if(data){
        this.projectlist = data;
        console.log('list', this.projectlist)

        this.dataSource = new MatTableDataSource(data);

        // this.dataSource.paginator = this.paginator;
        // this.dataSource.sort = this.sort;

        // setTimeout(()=>{                           // <<<---using ()=> syntax
          this.dataSource.paginator = this.paginator;
          this.dataSource.sort = this.sort;
      // }, 300);
        // let table_headers = Object.keys(this.userlist[0]) 

      }

    });
  }
  
  openPopup(id:any) {
    this.del_id = id
    this.displayStyle = "block";
  }
  closePopup() {
    this.displayStyle = "none";
  }

  ProjectAdd(){
    this.router.navigate(['/avmproject/project']);
  }
  EditProject(id:any){
    console.log(id);
    this.router.navigate(['/avmproject/update-project', id]);
  }

  DeleteProject(){
    // console.log(id);
    let query_id = {
      id: this.del_id
    }
    this.AuthService.deleteProject(query_id).subscribe((data: any)=>{
      if(data){  
        console.log(data.msg);   
        this.error = 'Project Deleted successfully!';
        this.displayStyle = "none";

        this.AuthService.getProjectList().subscribe((data: any)=>{
          if(data){
            this.projectlist = data;
            this.dataSource = new MatTableDataSource(data);

        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
            // console.log('list', this.projectlist)
            // let table_headers = Object.keys(this.userlist[0]) 
    
          }
    
        });


      }

    });
  }

}

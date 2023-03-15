import { AfterViewInit, Component, ViewChild, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import {MatTableModule} from '@angular/material/table'; 
import {MatPaginator} from '@angular/material/paginator';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-sub-user-list',
  templateUrl: './sub-user-list.component.html',
  styleUrls: ['./sub-user-list.component.scss']
})
export class SubUserListComponent implements OnInit  {
  dataSource:any;
  constructor(private AuthService:AuthService, 
    private router: Router) { }
    displayedColumns: string[] = ['id', 'first_name', 'last_name', 'email','pilot','phone','action'];
    

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
  userlist: any = '';
  msg: string = '';
  del_st: boolean = false;
  id : any;
  del_id:any;
  pageSize = environment.TABLE_ROW_LIMIT;
  permission: any;
  useradd_permission: boolean= false;
  useredit_permission: boolean= false;
  userdelete_permission: boolean= false;

  ngOnInit(): void {
    
    let query = {
      customer_id: this.custid,
    }
    this.AuthService.logincheck();
    this.permission = localStorage.getItem("permissions");
    this.useradd_permission = this.permission.includes('user-add');
    this.useredit_permission = this.permission.includes('user-edit');
    this.userdelete_permission = this.permission.includes('user-delete');
    this.custid = this.AuthService.getCustomerid();

    this.AuthService.getUserList(query).subscribe((data: any)=>{
      if(data){
        this.userlist = data;
        this.dataSource = new MatTableDataSource(data);
          this.dataSource.paginator = this.paginator;
          this.dataSource.sort = this.sort;

        

      }

    });
  }

  displayStyle = "none";
  
  openPopup(id:any) {
    this.del_id = id
    this.displayStyle = "block";
  }
  closePopup() {
    this.displayStyle = "none";
  }
  SubUsers(){
    this.router.navigate(['/avmuser/sub-users']);
  }
  EditUser(id:any){
    // console.log(id);
    this.router.navigate(['/avmuser/update-user', id]);
  }

  DeleteUser(){
    // console.log(id);
    let query_id = {
      id: this.del_id
    }
    // console.log(this.del_id)
    this.AuthService.deleteUser(query_id).subscribe((data: any)=>{
      if(data.success=='true'){  
        console.log(data);   
        this.msg = data.msg;
        this.displayStyle = "none";
        this.del_st = true
        // this.router.navigate(['/sub-user-list']);
        // this.router.navigate(['/sub-user-list'])
        // .then(() => {
        //   window.location.reload();
        // });

        let query = {
          customer_id: this.custid,
        }
        this.AuthService.getUserList(query).subscribe((data: any)=>{
          if(data){
            this.userlist = data;
            this.dataSource = new MatTableDataSource(data);

            this.dataSource.paginator = this.paginator;
            this.dataSource.sort = this.sort;
          }
    
        });

      }
      else if(data.success=='false'){
        this.msg = data.msg;
        this.displayStyle = "none";
        this.del_st = false
      }

    });
  }

}

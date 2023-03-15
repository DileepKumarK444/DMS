import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';



@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  dronelist:any = '';
  dronelen: boolean = false;
  count:any;
  N:any;
  M:any;
  H:any;
  constructor(private AuthService:AuthService, 
    private router: Router
    ) { }

  ngOnInit(): void {
    this.AuthService.logincheck();
    // this.count = 0;
    // this.N = 5;
    // this.M = 10;
    // this.H = 15;
    // location.reload();
    const authToken = localStorage.getItem('token');
    if(authToken){
    this.AuthService.getDroneList().subscribe((data: any)=>{
      console.log('DATA',data)
      this.count = data.data[0].error_count
      this.N = data.N[0].conf_value
      this.M = data.M[0].conf_value
      if(data){
        this.dronelist = data.data;
        console.log(this.dronelist);
        console.log(this.dronelist.length);
        console.log('dronelen_dashboard', this.dronelen);
        if(this.dronelist.length == 0)
        {
          this.dronelen = true;
        }
        else{
          this.dronelen = false;

        }
        // console.log(data[0].pilot);
        // let table_headers = Object.keys(this.userlist[0]) 

      }

    });
  }
    // location.reload();
  }

  DroneDetail(id:any){
    console.log('id', id);
    this.router.navigate(['drone/drone-details', id]);
  }

  /*Logout(){
    this.AuthService.clearAuthData();
    this.AuthService.clearPermissions();
    this.router.navigate(['/login']);
  }*/
  
}

import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-customer',
  templateUrl: './customer.component.html',
  styleUrls: ['./customer.component.scss']
})
export class CustomerComponent implements OnInit {
  first_name:any = '';
  last_name:any = '';
  email:any = '';
  phone:any = '';  
  activation_date:any = '';
  address:any = '';
  company_id__name:any = '';
  state_id__name:any = '';  
  country_id__name:any = '';
  designation_id__name:any = '';
  description:any = '';
  status:any = '';

  constructor(private AuthService:AuthService, 
    private router: Router
    ) { }

  ngOnInit(): void {
    this.AuthService.logincheck();
    this.AuthService.getProfile().subscribe((data: any)=>{
      if(data)
      {
        
        this.first_name = data[0].first_name;
        this.last_name = data[0].last_name;
        this.email = data[0].email;
        this.phone = data[0].phone;
        this.activation_date = data[0].activation_date;
        this.address = data[0].address;
        this.company_id__name = data[0].company_id__name;
        this.state_id__name = data[0].state_id__name;
        this.country_id__name = data[0].country_id__name;
        this.designation_id__name = data[0].designation_id__name;
        this.description = data[0].description;
        if(data[0].status == true){
          this.status = 'active';
        }
        else{
          this.status = 'inactive';
        }
      }
      else{
        //error page
        console.log(data[0].detail);             
        }

       });
  }
  
  error: string = '';

  Permission() {  
    // let d ={
    //   username:'sisira@actionfi.com',
    //   password:'password'
    // }
    this.AuthService.permissionCheck().subscribe((data: any)=> {
      if(data.permissions[0] == 'add-role'){
      //this.AuthService.saveAuth(data.token);
          //redirect to dashboard
          console.log(data.permissions);
          this.router.navigate(['/dashboard']);
      
      }
      else{
      this.error = 'Invalid Permission!';
      console.log('Invalid Permission!');
      //this.router.navigate(['/template-error/404']);

      //console.log(data.permissions);

      }
    });
  }
}

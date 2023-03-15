import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-profile-edit',
  templateUrl: './profile-edit.component.html',
  styleUrls: ['./profile-edit.component.scss']
})
export class ProfileEditComponent implements OnInit {
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
  pilot :any ='';
  error : any = '';
  id :any = '';
  profiledetails :any = '';

  constructor(private AuthService:AuthService, 
    private router: Router) { }

  ngOnInit(): void {
    this.AuthService.logincheck();
    this.AuthService.getProfile().subscribe((data: any)=>{
      if(data)
      {
        if(data){
          this.profiledetails = data;
          this.id = this.profiledetails[0].id
          this.first_name = this.profiledetails[0].first_name
          this.last_name = this.profiledetails[0].last_name
          this.pilot = this.profiledetails[0].pilot
          this.email = this.profiledetails[0].email
          this.phone = this.profiledetails[0].phone
        }
        // this.first_name = data[0].first_name;
        // this.last_name = data[0].last_name;
        // this.email = data[0].email;
        // this.phone = data[0].phone;
        // this.activation_date = data[0].activation_date;
        // this.address = data[0].address;
        // this.company_id__name = data[0].company_id__name;
        // this.state_id__name = data[0].state_id__name;
        // this.country_id__name = data[0].country_id__name;
        // this.designation_id__name = data[0].designation_id__name;
        // this.description = data[0].description;
        if(this.status == true){
          this.status = 'Active';
        }
        else{
          this.status = 'Inactive';
        }
        if(this.pilot == true){
          this.pilot = 'Yes';
        }
        else{
          this.pilot = 'No';
        }
      }
      else{
        //error page
        console.log(data[0].detail);             
        }

       });
  }

  UpdateProfile(){
    console.log(this.id);
    console.log(this.first_name)
    if(this.first_name != '' && this.last_name != '' && this.email != '' && this.phone != '' && this.id){
        
      let query = {
        id: this.id,
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        phone: this.phone
      }
      console.log('query', query);
    this.AuthService.UpdateUserdetails(query).subscribe((data: any)=>{
      if(data)
      {   
        if(data.success == 'true'){
        console.log('sisisi', data);
        this.router.navigate(['/avm/profile']);
        }
        else{
          console.log(data.msg);
        }
      }
      else{
        //error page
        this.error = 'Update Profile Error!';
      }

       });
    } else{
      //error page
      this.error = 'Please fill out the fields';
    }
  }

  OnCancel(){
    this.first_name = this.profiledetails[0].first_name
    this.last_name = this.profiledetails[0].last_name
    this.email = this.profiledetails[0].email
    this.phone = this.profiledetails[0].phone
  }
}

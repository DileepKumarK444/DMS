import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

// import { DomSanitizer } from '@angular/platform-browser'

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  id: any = '';
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
  edit_flag :boolean = false;
  profiledetails :any;
  error :any;
  pilot_license : any;
  tab:any = 'account';
  is_old_pass:any;
  is_pass:any;
  is_confirm_pass:any;
  image_format_error:any = false;
  customer_name:any;

  confirm_password:any = '';
  new_password:any = '';
  password:any = '';
  success:any = false;

  
  
  image:any = '';
  // loading: boolean = false; // Flag variable
  file: any = null;
  // base64data:any = '';
  
  constructor(private AuthService:AuthService, 
    private router: Router) { }

  ngOnInit(): void {
    this.AuthService.logincheck();
    console.log(this.router.url);
    this.customer_name = localStorage.getItem("customer_name");

    this.AuthService.getProfile().subscribe((data: any)=>{
      if(data)
      // {
      //   this.id = data[0].id;
      //   this.first_name = data[0].first_name;
      //   this.last_name = data[0].last_name;
      //   this.email = data[0].email;
      //   this.phone = data[0].phone;
      //   this.activation_date = data[0].activation_date;
      //   this.address = data[0].address;
      //   this.company_id__name = data[0].company_id__name;
      //   this.state_id__name = data[0].state_id__name;
      //   this.country_id__name = data[0].country_id__name;
      //   this.designation_id__name = data[0].designation_id__name;
      //   this.description = data[0].description;
      //   if(data[0].status == true){
      //     this.status = 'Active';
      //   }
      //   else{
      //     this.status = 'Inactive';
      //   }
      //   if(data[0].pilot == true){
      //     this.pilot = 'Yes';
      //   }
      //   else{
      //     this.pilot = 'No';
      //   }
      // }
      {   if(data.data)
            this.image = "data:image/png;base64,"+data.data
            else
          this.image = '../../assets/img/profile_new.jpg'
          this.profiledetails = data.customer;
          this.id = this.profiledetails[0].id
          this.first_name = this.profiledetails[0].first_name
          this.last_name = this.profiledetails[0].last_name
          this.pilot = this.profiledetails[0].pilot
          this.email = this.profiledetails[0].email
          this.phone = this.profiledetails[0].phone,
          this.status = this.profiledetails[0].status
          this.pilot_license = this.profiledetails[0].pilot_license;
          this.description = this.profiledetails[0].description;

          console.log('pilot', this.pilot)
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
  onbtnedit(event:any) {
    // this.file = event.target.files[0];
    console.log(this.id)
    // this.onUpload();
    let element:HTMLElement = document.getElementById('upload-photo') as HTMLElement;

    element.click();
  }
  // On file Select
  onChange(event:any) {
    this.file = event.target.files[0];
    // console.log(this.id)
    this.onUpload();
  }

  // OnClick of button Upload
  
  onUpload() {
    if(this.file.type=='image/jpeg'){
      this.image_format_error = false
        let query = {
          'id':this.id,
          'file':this.file
        }
        this.AuthService.upload(query).subscribe(
            (event: any) => {
              
            this.image = "data:image/png;base64,"+event.data
            // location.reload();
            let currentUrl = this.router.url;
            this.router.routeReuseStrategy.shouldReuseRoute = () => false;
            this.router.onSameUrlNavigation = 'reload';
            this.router.navigate([currentUrl]);
            // this.router.navigateByUrl('/', {skipLocationChange: true}).then(()=>
            // this.router.navigate([`${environment.AVM_URL}`+this.router.url]));
            // console.log(this.image)

            }
        );
      }
      else{
        this.image_format_error = true
      }
  }

  UpdateProfile(id:any){
    console.log(this.id);
    console.log(this.first_name)
    if(this.first_name != '' && this.last_name != '' && this.email != '' && this.phone != '' && this.id){
      
      if(this.pilot == 'Yes'){
        this.pilot = true;
      }
      else{
        this.pilot = false;
      }

      let query = {
        id: this.id,
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        phone: this.phone,
        pilot: this.pilot,
        status: this.status,
        pilot_license: this.pilot_license,
        description: this.description
      }
      console.log('query', query);
    this.AuthService.UpdateUserdetails(query).subscribe((data: any)=>{
      if(data)
      {   
        if(data.success == 'true'){
        console.log('sisisi', data);
        // this.router.navigate(['/profile']);
        this.edit_flag = false;

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
    this.pilot = this.profiledetails[0].pilot

    // this.router.navigate(['/profile']);

  }

  EditProfile(){
    this.edit_flag = true;
  }

  tabClick(q:any,t:any){
    // alert(t)
    this.tab = t;
    
  }
  ChangePasswordClick(){
    
    this.is_old_pass = false
    this.is_pass = false
    this.is_confirm_pass = false
    this.success = false
    this.error = ''
    if(this.confirm_password != '' && this.new_password != '' && this.password != ''){

      if(this.confirm_password == this.new_password){
        // console.log('dasdasdasd',this.confirm_password)
        let query = {
          confirm_password: this.confirm_password,
          new_password: this.new_password,
          password: this.password,
          id:this.id
        }
    
        this.AuthService.ChangePassword(query).subscribe((data: any)=>{
        if(data)
        {   
          if(data.success == true){
            this.success = true;
            this.confirm_password=''
            this.new_password=''
            this.password=''
          }
          else{
            this.error = data.msg
          }
        }
        })
      }
      else{
        this.error = "New password doesn't Match with the confirm password"
      }
    }
    else{
      if(this.confirm_password == '')
        this.is_confirm_pass =true
      if(this.new_password == '')
        this.is_pass =true
      if(this.password == '')
        this.is_old_pass =true
    }
    
  }


}

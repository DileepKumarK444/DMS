import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup } from "@angular/forms";
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-pilot',
  templateUrl: './pilot.component.html',
  styleUrls: ['./pilot.component.scss']
})
export class PilotComponent implements OnInit {

  // form: FormGroup;

  constructor(private AuthService:AuthService, 
    private router: Router,
    // public fb: FormBuilder,
    private http: HttpClientModule) { 
      // this.form = this.fb.group({
      //   img: [null]
      // })
    }

    first_name: string = '';
    last_name: string = '';
    email: string = '';
    phone: string = '';
    pilot_license: any = '';
    expiry_date: string = '';
    custid: any = '';
    error: string = '';

  ngOnInit(): void {
    this.AuthService.logincheck();
    this.custid = this.AuthService.getCustomerid();
  }

  OnSubmit(Image:any) {
    // console.log(Image)
      var formData = new FormData();
      formData.append("first_name", this.first_name);
      formData.append("last_name", this.last_name);
      formData.append("email", this.email);
      formData.append("phone", this.phone);
      formData.append("pilot_license", this.pilot_license);
      formData.append("expiry_date", this.expiry_date);
      console.log('formData', formData)
      this.AuthService.addPilot(formData).subscribe((data: any)=>{
      if(data)
      {
        console.log(data)
      }
    });
  }
  AddPilot() {
    if(this.first_name != '' && this.last_name != '' && this.email != '' && this.phone != '' && this.pilot_license != '' && this.expiry_date != '' && this.custid != ''){
        
      let query = {
        first_name: this.first_name,
        last_name: this.last_name,
        email: this.email,
        phone: this.phone,
        pilot_license: this.pilot_license,
        expiry_date: this.expiry_date,
        customer_id: this.custid
      }

      var formData: any = new FormData();
      formData.append("first_name", this.first_name);
      formData.append("last_name", this.last_name);
      formData.append("email", this.email);
      formData.append("phone", this.phone);
      formData.append("pilot_license", this.pilot_license);
      formData.append("expiry_date", this.expiry_date);

      this.AuthService.addPilot(formData).subscribe((data: any)=>{
      if(data)
      {   
        if(data.success == 'true'){
        console.log('sisira1', this.custid); 
        console.log('license',this.pilot_license);
        this.error = data.msg;

        }
        else{
          console.log(data.msg);
          this.error = data.msg;

        }
      }
      else{
        //error page
        this.error = 'Add Pilot Error!';
      }

       });
    } else{
      //error page
      this.error = 'Please fill out the fields';
    }
  }

//   upload(event:any) {
//     const file = (event.target as HTMLInputElement).files[0];
//     this.form.patchValue({
//       pilot_license: file
//     });
//     this.form.get('pilot_license').updateValueAndValidity()
//  }

}

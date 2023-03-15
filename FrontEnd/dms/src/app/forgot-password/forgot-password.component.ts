import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';



@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.scss']
})
export class ForgotPasswordComponent implements OnInit {

  constructor(private AuthService:AuthService,
    private router: Router) { }

  ngOnInit(): void {
  }

  email: string = '';
  // username: string = '';
  // password: string = '';
  error: string = '';
  error_status : boolean = false;
  success: string = '';
  success_status : boolean = false;
  // pass_hide = true;
  back_to_login(){
    this.router.navigate(['/login']);
  }
  forgot_password(){
    this.success_status = false;
    this.success = ''
    if(this.email == ''){
      this.error = "Please enter the email"
      this.error_status = true
    }
    else{
      this.error = ""
      this.error_status = false
      let query= {
        'email':this.email
      }
    this.AuthService.requestpasswordReset(query).subscribe((data: any)=> {
      if(data.st){
        this.email = ''
        this.success = data.msg
        this.success_status = true

      }
      else{
        this.success = ''
        this.success_status = false
      }
    });
  }
  }
  // Login() {

  //   if(this.username != '' && this.password != ''){
      
  //     let query = {
  //       username: this.username,
  //       password: this.password,
  //     }

  //     this.AuthService.requestToken(query).subscribe((data: any)=> {
  //       if(data.token){
  //           console.log(data.token);
  //           //redirect to dashboard
  //           //this.router.navigate(['/dashboard']);
  //           this.AuthService.saveAuth(data.token);

  //       setTimeout(() => {

  //         this.AuthService.getProcess(query).subscribe((data: any)=>{
  //         // console.log('sisira',data.status);
  //         if(data.status == true)
  //         {
  //           //console.log('Logined!');
  //           this.AuthService.permissionCheck().subscribe((data: any)=>{
  //             if(data.permissions)
  //             {
  //               this.AuthService.savePermissions(data.permissions, data.username, data.name, data.customer_id, data.role); 
  //               console.log(data);
  //               this.router.navigate(['/dashboard']);                   
  //             }
  //             else{
  //               //error page
  //               console.log(data.detail);             
  //               }
  
  //              });
  //           //redirect to dashboard
            

  //         }
  //         else{
  //           this.error = data.message;
  //           this.error_status = true;
  //           console.log('Login failure!');   
  //           this.AuthService.clearAuthData();
  //         }

  //          });

  //       }, 100);
  //      }
  //      else{
  //       this.error = 'Invalid Login!';
  //       this.error_status = true;
  //       console.log('Login failure!');
  //      }
  //     }, (error: any) => {
  //       var er = error.error.non_field_errors ? error.error.non_field_errors[0] : '';
  //       this.error = er;
  //       this.error_status = true;
  //     });

  //     this.username = ''; 
  //     this.password = ''; 
  //     this.error = ''; 
  //     this.error_status = false;
  //   }
  //   else{
  //    this.error = 'Enter a valid username and password!';
  //    this.error_status = true;
  //   }

  // }
  // passHideClick(){
    
  //   this.pass_hide = !this.pass_hide;
    
  // }
}

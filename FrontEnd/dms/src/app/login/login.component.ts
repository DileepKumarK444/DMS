import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router,ActivatedRoute  } from '@angular/router';



@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})

export class LoginComponent implements OnInit {
  id:any;
  constructor(private AuthService:AuthService,
    private router: Router,
    private route: ActivatedRoute
    ) { }

  ngOnInit(): void {
  // console.log('Login as User')
  
  // this.route.queryParams
  //     .subscribe(params => {
  //       console.log('paramsparamsparamsparams',(params['id']));

  //       if(params['id']!==undefined)
  //       {
  //         localStorage.clear();
  //         let id = params['id']
  //         let query = {
  //           token: id.trim()
  //         }
  //         this.AuthService.getLoginToken(query).subscribe((data: any)=> {
  //           // console.log('token',data)
  //           if(data.token){
  //               this.AuthService.saveAuth(data.token);
  //               this.AuthService.savePermissions(data.role_perm.permissions, data.role_perm.username, data.role_perm.name, data.role_perm.customer_id, data.role_perm.role, data.role_perm.last_name, data.role_perm.customer_name); 
  //                 console.log(data);
  //                 this.router.navigate(['/avm/dashboard']);  
  //          }
  //          else{
  //           this.error = 'Invalid Login!';
  //           this.error_status = true;
  //           console.log('Login failure!');
  //          }
  //         }, (error: any) => {
  //           var er = error.error.non_field_errors ? error.error.non_field_errors[0] : '';
  //           this.error = er;
  //           this.error_status = true;
  //         });
  //       }
  //       // else
  //       // console.log('No params'); // { orderby: "price" }
  //     }
  //   );
    const authToken = this.AuthService.getToken();
    console.log(authToken)
    if (authToken) {
      this.router.navigate(['/avm/dashboard']);
    }
  }

  username: string = '';
  last_name: string = '';
  password: string = '';
  error: string = '';
  error_status : boolean = false;
  pass_hide = true;
  forgot_password(){
    this.router.navigate(['/forgot-password']);
  }
    Login() {

      if(this.username != '' && this.password != ''){
        
        let query = {
          username: this.username,
          password: this.password,
        }

        this.AuthService.requestToken(query).subscribe((data: any)=> {
          if(data.token){
              console.log(data.token);
              //redirect to dashboard
              //this.router.navigate(['/dashboard']);
              this.AuthService.saveAuth(data.token);

          setTimeout(() => {

            this.AuthService.getProcess(query).subscribe((data: any)=>{
            // console.log('sisira',data.status);
            if(data.status == true)
            {
              //console.log('Logined!');
              this.AuthService.permissionCheck().subscribe((data: any)=>{
                if(data.permissions)
                {
                  this.AuthService.savePermissions(data.permissions, data.username, data.name, data.customer_id, data.role, data.last_name, data.customer_name); 
                  console.log(data);
                  // this.router.navigate(['/dashboard']);    
                  // window.location.href = '/dashboard' ;
                  this.router.navigate(['/avm/dashboard']);
               
                }
                else{
                  //error page
                  console.log(data.detail);             
                  }
    
                 });
              //redirect to dashboard
              

            }
            else{
              this.error = data.message;
              this.error_status = true;
              console.log('Login failure!');   
              this.AuthService.clearAuthData();
            }

             });

          }, 100);
         }
         else{
          this.error = 'Invalid Login!';
          this.error_status = true;
          console.log('Login failure!');
         }
        }, (error: any) => {
          var er = error.error.non_field_errors ? error.error.non_field_errors[0] : '';
          this.error = er;
          this.error_status = true;
        });

        this.username = ''; 
        this.password = ''; 
        this.error = ''; 
        this.error_status = false;
      }
      else{
       this.error = 'Enter a valid username and password!';
       this.error_status = true;
      }

    }
    passHideClick(){
      
      this.pass_hide = !this.pass_hide;
      
    }
    
}


import { Component, OnInit,AfterViewInit  } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-sub-user-edit',
  templateUrl: './sub-user-edit.component.html',
  styleUrls: ['./sub-user-edit.component.scss']
})
export class SubUserEditComponent implements OnInit  {

  constructor(private AuthService:AuthService, 
    private router: Router,
    private activatedRoute: ActivatedRoute) { }

    id: string = '';
    firstname: string = '';
    lastname: string = '';
    email: string = '';
    phone: string = '';
    password: string = '';
    custid: any = '';
    pilot: boolean = false;
    add_fields: boolean = false;

    error: string = '';
    userdetails: any;
    pilot_license: string = '';
    description: string = '';
    file: any = null;
    success: string = 'false';
    pilot_license_file:any = '';

    firstname_error:boolean=false;
    lastname_error:boolean=false;
    email_error:string='';
    email_val_error:string='';
    
    phone_error:string='';
    file_type_error:boolean=false;

    is_first_name :any; 
    is_last_name:any; 
    is_email:any; 
    is_phone :any; 
    notnumber: boolean = false;
    email_flag: boolean = false;

    profile_schema:string = '';
    profile_schema_model:any = [];
    profile_schema_model1:any = [];
    fileAttr = '';
    file_st:boolean = false;
    permission: any;
    userupdate_permission: boolean= false;
    // ngAfterViewInit(): void{
    //   // setTimeout(()=>{ 
    //   console.log('/////////////////////////////////////',this.profile_schema_model)
    //   // this.profile_schema_model = this.profile_schema_model1
    //   for (let key in this.profile_schema_model1) {
    //     console.log('cccccccccccccccccccccccccccc')
    //           // console.log('key',key,JSON.parse(this.userdetails[0].additional_fields)[key])
    //           this.profile_schema_model[key] = JSON.parse(this.userdetails[0].additional_fields)[key]
    //         }
    //       // }, 300);
    // }
  ngOnInit(): void {
    this.AuthService.logincheck();
    this.id = this.activatedRoute.snapshot.params['id'];
    // console.log("sisiraid", this.id);
    this.custid = this.AuthService.getCustomerid();
    let query = {
      customer_id: this.custid
    }
    let query_id = {
      id: this.id
    }
    this.permission = localStorage.getItem("permissions");
    this.userupdate_permission = this.permission.includes('user-update');
    this.AuthService.logincheck();
    this.custid = this.AuthService.getCustomerid();

    this.AuthService.getSelectedUserDetails(query_id).subscribe((data: any)=>{
      if(data){
        this.userdetails = data['customer'];
        console.log('this.userdetails',data['profile_schema'])
        
        this.profile_schema = JSON.parse(data['profile_schema'][0].conf_value)
        this.firstname = this.userdetails[0].first_name
        this.lastname = this.userdetails[0].last_name
        this.pilot = this.userdetails[0].pilot
        this.add_fields = this.userdetails[0].add_fields
        this.email = this.userdetails[0].email
        this.phone = this.userdetails[0].phone
        this.pilot_license = this.userdetails[0].pilot_license;
        this.description = this.userdetails[0].description;
        this.pilot_license_file = this.userdetails[0].pilot_license_file
        let filename = this.userdetails[0].pilot_license_file
        this.fileAttr = filename.split('/')[1]
        if(filename)
          this.file_st = true
        
        let dict:any = [];
        // setTimeout(()=>{ 
          if(this.userdetails[0].additional_fields)
            this.profile_schema_model = JSON.parse(this.userdetails[0].additional_fields);

        for(let key in JSON.parse(data['profile_schema'][0].conf_value)){
          console.log(key)
          if(!this.profile_schema_model[key])
          this.profile_schema_model[key]=''
        }
        // this.profile_schema_model = JSON.parse(this.userdetails[0].additional_fields)
          // for (let key in JSON.parse(this.userdetails[0].additional_fields)) {
          //   // console.log('key',key,JSON.parse(this.userdetails[0].additional_fields)[key])
          //   this.profile_schema_model[key] = this.userdetails[0].additional_fields)[key];
          // }
          
        // }, 300);
        

        
      }

    });
  }

  handleChange (e: any,k:any) {
    console.log(e)
    this.profile_schema_model[k] = e
  }

  SubUserList(){
    this.router.navigate(['/avmuser/sub-user-list']);
  }
  onChange(event:any) {
    if (event.target.files && event.target.files[0]) {
    this.file = event.target.files[0];
    this.fileAttr = this.file.name;
    // console.log(this.id)
    let file = event.target.files[0];
      console.log(file.typ1);
        if(file.type != "application/pdf") {
          this.file_type_error = true
          this.file = ''
          this.success='false';
          this.error='';
        }
      }
      // else{
      //   this.fileAttr = 'Choose File';
      // }
  }
  file_download(){
    let body = {
      id : this.id
    }
  
    this.AuthService.downloadLicence(body).subscribe((response: any)=>{
      if(response.data){
        let resp = this.base64ToArrayBuffer(response.data);
        let file = new Blob([resp], { type: 'application/pdf' });   
        let filename = response.file_name    
        let downloadLink = document.createElement('a');     
        downloadLink.href = window.URL.createObjectURL(file);
        downloadLink.setAttribute('download', filename);
        document.body.appendChild(downloadLink);
        downloadLink.click();
      }
      
  }
    );
  }

  base64ToArrayBuffer(base64:any):ArrayBuffer {
    var binary_string =  window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array( len );
    for (var i = 0; i < len; i++)        {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
  }
  testMethod(event:any,key:any,val:any) {
    console.log(val)
    this.profile_schema_model[key] = val}
  UpdateUser() {
    console.log('asddasdasd',this.profile_schema_model)
    // console.log(this.firstname)
    // console.log(this.lastname)
    // console.log(this.email)
    this.success='false';
    this.file_type_error = false;
    this.error='';
    this.email_error=''
    this.phone_error='';
    var emailReg =  /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    this.is_first_name = false
    this.is_last_name = false
    this.is_email = false
    this.is_phone = false
    this.email_flag = false;

    if(this.firstname == ''){
      this.is_first_name=true;
    }
    if(this.lastname == ''){
      this.is_last_name=true;
    }
    
    if(this.email == ''){
      this.email_error="This field is required.";
    }
    else if(!emailReg.test(this.email))
    {
      this.email_error="Enter a valid Email Address";
      this.email_flag = true;
    }
    if(this.phone == ''){
      this.phone_error="This field is required.";
    }
    else if (this.notnumber || (this.phone).length != 10){
      this.phone_error="Enter a valid phone number";
    }

   else if(!this.email_flag && this.firstname != '' && this.lastname != '' && this.email != '' && this.phone != '' && this.custid != '' && this.id){
        
      let query = {
        id: this.id,
        first_name: this.firstname,
        last_name: this.lastname,
        email: this.email,
        phone: this.phone,
        pilot: this.pilot,
        add_fields: this.add_fields,
        pilot_license: this.pilot_license,
        description: this.description,
        customer_id: this.custid,
        file:this.file,
        profile_schema_model:this.profile_schema_model
      }
      // console.log('sisira1', this.pilot)
    this.AuthService.UpdateUserdetails(query).subscribe((data: any)=>{
      if(data)
      {   
        // console.log('sisira', this.custid); 
        if(data.success == 'true'){
        // console.log('sisira1', this.custid); 
        this.password = data.password;
        this.success = data.success;
        if(data.file)
        {
          let filename = data.file
          console.log(filename.split('/')[1])
          this.fileAttr = filename.split('/')[1]
          this.file_st = true
        }
        

        // console.log(this.password);
        // console.log('sisisi', this.pilot);
        // this.router.navigate(['/sub-user-list']);

        }
        else if(data.success=='exist'){
          this.error = data.msg 
        }
        else{
          this.error = data.msg 
          console.log(data.msg);
        }
      }
      else{
        //error page
        this.error = 'Update User Error!';
      }

       });
    } else{
      if(this.firstname == '')
      this.is_first_name =true
      if(this.lastname == '')
      this.is_last_name =true
      // if(this.email == '')
      // this.is_email =true
      if(this.phone == '')
      this.is_phone =true
    }
  }

  OnCancel(){
    
    this.firstname = this.userdetails[0].first_name;
    this.lastname = this.userdetails[0].last_name;
    this.email = this.userdetails[0].email;
    this.phone = this.userdetails[0].phone;
    this.pilot = this.userdetails[0].pilot;
    this.add_fields = this.userdetails[0].add_fields;
    this.pilot_license = this.userdetails[0].pilot_license;
    this.description = this.userdetails[0].description;
  }

  check(event:any){
    if(event.target.checked){
      this.pilot = true;
    }
    else{
      this.pilot = false;
    }
  }

  check_fields(event:any){
    if(event.target.checked){
      this.add_fields = true;

    }
    else{
      this.add_fields = false;
    }
  }

  phoneChange(event:any){
    const pattern = /^[0-9\-]*$/;
    if (!pattern.test(event.target.value)) {
      // event.target.value = event.target.value.replace(/[^0-9\-]/g, "");
      // this.phone = event.target.value.replace(/[^0-9\-]/g, "");
      

      this.notnumber = true;
    }
  }

}

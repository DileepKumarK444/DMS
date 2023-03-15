import { Component, OnInit,ViewChild, ElementRef } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router, ActivatedRoute } from '@angular/router';
import { FormControl, Validators } from "@angular/forms";
declare var $ :any;

@Component({
  selector: 'app-sub-users',
  templateUrl: './sub-users.component.html',
  styleUrls: ['./sub-users.component.scss']
})

export class SubUsersComponent implements OnInit {
  // isAddMode: boolean = true;
  // id: string = '';
  @ViewChild('fileInput') fileInput: ElementRef;
  constructor(private AuthService:AuthService, 
    private router: Router) { }

    firstname: string = '';
    lastname: string = '';
    email: string = '';
    phone: string = '';
    password: string = '';
    custid: any = '';
    pilot: boolean = false;
    add_fields: boolean = false;
    error: string = '';
    pilot_license: string = '';
    description: string = '';
    success: string = 'false';
    file: any = null;
    firstname_error:boolean=false;
    lastname_error:boolean=false;
    email_error:string='';
    phone_error:string='';
    email_valid_error:boolean=false;
    file_type_error:boolean=false;
    is_first_name :any; 
    is_last_name:any; 
    is_email:any; 
    is_phone :any; 
    email_flag: boolean = false;
    notnumber: boolean = false;

    profile_schema:string = '';
    profile_schema_model:any = [];
    
    file_store: FileList;
    display: FormControl = new FormControl("", Validators.required);
    fileAttr = '';
    permission: any;
    usersave_permission: boolean= false;


    // event : any;
  ngOnInit(): void {
    this.AuthService.logincheck();
    this.custid = this.AuthService.getCustomerid();

    this.permission = localStorage.getItem("permissions");
    this.usersave_permission = this.permission.includes('user-save');
    
    this.AuthService.getProfileSchema().subscribe((data: any)=>{
      if(data){
        console.log('data', JSON.parse(data[0].conf_value))
        this.profile_schema = JSON.parse(data[0].conf_value)
        // this.userlist = data;
        // this.dataSource = new MatTableDataSource(data);
        //   this.dataSource.paginator = this.paginator;
        //   this.dataSource.sort = this.sort;

        

      }

    });

    // this.id = this.route.snapshot.params['id'];
    // this.isAddMode = !this.id;
  }
  // uploadFileEvt(imgFile: any) {
  //   console.log(imgFile.target.files[0].name)
  //   if (imgFile.target.files && imgFile.target.files[0]) {
  //     this.fileAttr = '';
  //     Array.from(imgFile.target.files).forEach((file: any) => {
  //       this.fileAttr += file.name + ' - ';
  //     });
  //     // HTML5 FileReader API
  //     let reader = new FileReader();
  //     reader.onload = (e: any) => {
  //       let image = new Image();
  //       image.src = e.target.result;
  //       image.onload = (rs) => {
  //         let imgBase64Path = e.target.result;
  //       };
  //     };
  //     reader.readAsDataURL(imgFile.target.files[0]);
  //     // Reset if duplicate image uploaded again
  //     this.fileInput.nativeElement.value = '';
  //   } else {
  //     this.fileAttr = 'Choose File';
  //   }
  // }
  // handleFileInputChange(l: FileList): void {
  //   this.file_store = l;
  //   if (l.length) {
  //     const f = l[0];
  //     const count = l.length > 1 ? `(+${l.length - 1} files)` : "";
  //     this.display.patchValue(`${f.name}${count}`);
  //   } else {
  //     this.display.patchValue("");
  //   }
  // }
  SubUserList(){
    this.router.navigate(['/avmuser/sub-user-list']);
  }
  onChange(event:any) {
    if (event.target.files && event.target.files[0]) {
    this.file = event.target.files[0];
    let file = event.target.files[0];
    this.fileAttr = file.name;
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
  AddUser() {

    // console.log($('.dv-dynamic').html())
    // $.each($('.dv-dynamic'),function(){
    //   console.log($(this).val());
    //   })
    // console.log(this.profile_schema);
    // for (let key in (this.profile_schema_model)) {
    //   if((this.profile_schema_model)[key]!=undefined)
    //     console.log('DDDDDDD',(this.profile_schema_model)[key])
    //     // Use `key` and `value`
    // }
    // (this.profile_schema_model).forEach(function (value:any) {
    //   console.log(value);
    // });
    // let array = this.profile_schema_model;
    // for (let i = 0; i < array.length; i++) {
    //   console.log(array[i]);
    // }
    this.success='false';
    this.error='';
    this.email_error = ''
    this.file_type_error = false;
    var emailReg =  /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

    this.is_first_name = false
    this.is_last_name = false
    this.is_email = false
    this.is_phone = false
    this.phone_error='';
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
    
    else if(!this.email_flag && this.firstname != '' && this.lastname != '' && this.email != '' && this.phone != '' && this.custid != ''){
        
      let query = {
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
      
    this.AuthService.saveUserdetails(query).subscribe((data: any)=>{
      if(data)
      {   
        if(data.success == 'true'){
        this.success = data.success;

        this.password = data.password;
        this.firstname = '';
        this.lastname = '';
        this.email = '';
        this.phone = '';
        this.pilot = false;
        this.add_fields = false;
        this.pilot_license = '';
        this.description = '';
        this.profile_schema_model = '';
        }else if(data.success=='exist'){
          this.error = data.msg 
        }
        else{
          this.error = data.msg 
        }
      }
      else{
        this.error = 'Add User Error!';
      }

       });
    } else{
      console.log(this.lastname)
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
    
    this.firstname = '';
    this.lastname = '';
    this.email = '';
    this.phone = '';
    this.pilot = false;
    this.add_fields = false;
    this.pilot_license = '';
    this.description = '';
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

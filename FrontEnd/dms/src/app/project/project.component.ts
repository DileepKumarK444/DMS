import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { formatDate } from '@angular/common';
// import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { MAT_DATE_FORMATS } from '@angular/material/core';

export const MY_DATE_FORMATS = {
  parse: {
    dateInput: 'MM/DD/YYYY',
  },
  display: {
    dateInput: 'MM/DD/YYYY',
    monthYearLabel: 'MMMM YYYY',
    dateA11yLabel: 'LL',
    monthYearA11yLabel: 'MMMM YYYY'
  },
};
@Component({
  selector: 'app-project',
  templateUrl: './project.component.html',
  styleUrls: ['./project.component.scss'],
  providers: [
    { provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS }
  ]
})
export class ProjectComponent implements OnInit {

  constructor(private AuthService:AuthService, 
    private router: Router) { }
  
    project_name: string = '';
    mission_commander: string = '';
    start_date: string = '';
    end_date: string = '';
    custid: any = '';
    userlist: any = '';
    from_date:any = '';
    msg: string = '';
    save_st:boolean = false
    // success: string = 'false';
    
    project_name_error:boolean=false;
    mission_commander_error:boolean=false;
    start_date_error:string='';
    end_date_error:string='';

    is_projectname :any; 
    is_missioncommander:any; 
    is_startdate:any; 
    is_enddate :any; 
    startDate = new Date(2000, 0, 1);
    permission: any;
    projectsave_permission: boolean= false;

  ngOnInit(): void {
    // this.from_date = new FormControl(new Date())
    let query = {
      customer_id: this.custid,
    }
    this.permission = localStorage.getItem("permissions");
    this.projectsave_permission = this.permission.includes('project-save');

    this.AuthService.logincheck();
    this.custid = this.AuthService.getCustomerid();
    this.AuthService.getUserList(query).subscribe((data: any)=>{
      if(data){
        this.userlist = data;
      }
      // console.log(data)

    });
   
  }
  ProjectList()
  {
    this.router.navigate(['/avmproject/project-list']);
  }

  AddProject() {

    const format = 'YYYY-MM-dd';
    // const end_date = this.end_date;
    const locale = 'en-US';
    // const end_date1 = ''
    // const start_date1 = ''
    if(this.end_date!='' && this.end_date!= null){
      this.end_date = formatDate(this.end_date, format, locale);
    }
    if(this.start_date!='' && this.start_date!= null){
      this.start_date = formatDate(this.start_date, format, locale);
    }

    // this.success='false';
    this.msg='';
    console.log(this.project_name)
    console.log(this.mission_commander)
    console.log(this.start_date)
    console.log("enddatetest:", this.end_date)
    // console.log("enddatetest1:", this.end_date.length)

    console.log(this.custid)
    console.log(this.start_date)
    var date1 = new Date('January 01, 2001 01:30:00');
    const dateString= '2020-09-24T16:57:23.985Z';
    // formatDate(datecomingfromdb,'yyyy-MM-dd','en_US');
    new Date();
    console.log(new Date());
    let thirdDate = new Date('2001-01-01')
    console.log(thirdDate);
    console.log(this.start_date);
    this.is_projectname = false
    this.is_missioncommander = false
    this.is_startdate = false
    this.is_enddate = false
    this.start_date_error = ''
    this.end_date_error = ''

    if(this.project_name == ''){
      this.is_projectname=true;
    }
    if(this.mission_commander == ''){
      this.is_missioncommander=true;
    }
    if(this.start_date == '' || this.start_date== null){
      this.start_date_error="This field is required.";
    }
    else if((new Date(this.start_date).getTime()) < thirdDate.getTime()){
      this.start_date_error="Please enter a Date greater than 2001.";
    }
    if(this.end_date == '' || this.end_date== null){
      this.end_date_error="This field is required.";
    }
    else if((new Date(this.end_date).getTime()) < thirdDate.getTime()){
      this.end_date_error="Please enter a Date greater than 2001.";
    }
    else if(this.start_date > this.end_date){
      this.end_date_error="End Date must be greater than Start Date";
    }

    else if(this.project_name != '' && this.mission_commander != '' && this.start_date != '' && this.start_date != null && this.end_date != '' && this.custid != ''){
        
      let query = {
        project_name: this.project_name,
        mission_commander: this.mission_commander,
        start_date: this.start_date,
        end_date: this.end_date,
        customer_id: this.custid,
      }
    // console.log('sisirasivan')
    this.AuthService.addProject(query).subscribe((data: any)=>{
      if(data)
      {   
        if(data.success == 'true'){
        this.msg = data.msg;
        this.save_st = true;
        console.log('sisira1', this.custid); 
        this.project_name = '';
        this.mission_commander = '';
        this.start_date = '';
        this.end_date = '';

        // this.router.navigate(['/project-list']);
        //this.password = data.password;
        //console.log(this.password);
        }
        else if(data.success=='exist')
        {
          this.save_st = false
          this.msg =data.msg
        }
        else{
          console.log(data.msg);
          this.save_st = false
          this.msg = data.msg;
        }
      }
      else{
        //error page
        this.save_st = false
        this.msg = 'Add Project Error!';
      }

       });
    } else{
      if(this.project_name == '')
      this.is_projectname =true
      if(this.mission_commander == '')
      this.is_missioncommander =true
      if(this.start_date == '')
      this.is_startdate =true
      if(this.end_date == '')
      this.is_enddate =true

    }
  }
  // AddProject() {

  //   const format = 'YYYY-MM-dd';
  //   // const end_date = this.end_date;
  //   const locale = 'en-US';
  //   const end_date = formatDate(this.end_date, format, locale);
  //   const start_date = formatDate(this.start_date, format, locale);

  //   this.success='false';
  //   this.error='';
  //   console.log(this.project_name)
  //   console.log(this.mission_commander)
  //   console.log(this.start_date)
  //   console.log(this.end_date)
  //   console.log(this.custid)
  //   console.log(this.start_date)
  //   var date1 = new Date('January 01, 2001 01:30:00');
  //   const dateString= '2020-09-24T16:57:23.985Z';
  //   // formatDate(datecomingfromdb,'yyyy-MM-dd','en_US');
  //   new Date();
  //   console.log(new Date());
  //   let thirdDate = new Date('2001-01-01')
  //   console.log(thirdDate);
  //   console.log(this.start_date);
  //   this.is_projectname = false
  //   this.is_missioncommander = false
  //   this.is_startdate = false
  //   this.is_enddate = false
  //   this.start_date_error = ''
  //   this.end_date_error = ''

  //   if(this.project_name == ''){
  //     this.project_name_error=true;
  //   }
  //   if(this.mission_commander == ''){
  //     this.mission_commander_error=true;
  //   }
  //   if(start_date == ''){
  //     this.start_date_error="This field is required.";
  //   }
  //   else if((new Date(start_date).getTime()) < thirdDate.getTime()){
  //     this.start_date_error="Please enter a Date greater than 2001.";
  //   }
  //   if(end_date == ''){
  //     this.end_date_error="This field is required.";
  //   }
  //   else if((new Date(end_date).getTime()) < thirdDate.getTime()){
  //     this.end_date_error="Please enter a Date greater than 2001.";
  //   }
  //   else if(start_date > end_date){
  //     this.end_date_error="End Date must be greater than Start Date";
  //   }

  //   else if(this.project_name != '' && this.mission_commander != '' && start_date != '' && end_date != '' && this.custid != ''){
        
  //     let query = {
  //       project_name: this.project_name,
  //       mission_commander: this.mission_commander,
  //       start_date: start_date,
  //       end_date: end_date,
  //       customer_id: this.custid,
  //     }
  //   // console.log('sisirasivan')
  //   this.AuthService.addProject(query).subscribe((data: any)=>{
  //     if(data)
  //     {   
  //       if(data.success == 'true'){
  //       this.success = data.success;
  //       console.log('sisira1', this.custid); 
  //       this.project_name = '';
  //       this.mission_commander = '';
  //       this.start_date = '';
  //       this.end_date = '';

  //       // this.router.navigate(['/project-list']);
  //       //this.password = data.password;
  //       //console.log(this.password);
  //       }
  //       else if(data.success=='exist')
  //       {
  //         this.error =data.msg
  //       }
  //       else{
  //         console.log(data.msg);
  //         this.error = data.msg;
  //       }
  //     }
  //     else{
  //       //error page
  //       this.error = 'Add Project Error!';
  //     }

  //      });
  //   } else{
  //     if(this.project_name == '')
  //     this.is_projectname =true
  //     if(this.mission_commander == '')
  //     this.is_missioncommander =true
  //     if(this.start_date == '')
  //     this.is_startdate =true
  //     if(this.end_date == '')
  //     this.is_enddate =true

  //   }
  // }

  OnCancel(){
    
    this.project_name = '';
    this.mission_commander = '';
    this.start_date = '';
    this.end_date = '';
  }

}


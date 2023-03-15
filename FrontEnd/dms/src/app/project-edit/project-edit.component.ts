import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router, ActivatedRoute } from '@angular/router';
import { MAT_DATE_FORMATS } from '@angular/material/core';
import { formatDate } from '@angular/common';
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
  selector: 'app-project-edit',
  templateUrl: './project-edit.component.html',
  styleUrls: ['./project-edit.component.scss'],
  providers: [
    { provide: MAT_DATE_FORMATS, useValue: MY_DATE_FORMATS }
  ]
})
export class ProjectEditComponent implements OnInit {
  // pipe = new DatePipe('en-US');
  constructor(private AuthService:AuthService, 
    private router: Router,
    private activatedRoute: ActivatedRoute) { }

    id: string = '';
    project_name: string = '';
    mission_commander: string = '';
    start_date: string = '';
    end_date: string = '';
    // error: string = '';
    projectdetails: any;
    custid: any = '';
    userlist: any = '';

    msg: string = '';
    // success: string = 'false';
    update_st:boolean = false;

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
    projectupdate_permission: boolean= false;

  ngOnInit(): void {
    this.AuthService.logincheck();
    this.permission = localStorage.getItem("permissions");
    this.projectupdate_permission = this.permission.includes('project-update');

    this.id = this.activatedRoute.snapshot.params['id'];
    console.log("sisiraid", this.id);
    let query = {
      customer_id: this.custid,
    }
    let query_id = {
      id: this.id
    }
    this.AuthService.logincheck();

    this.AuthService.getSelectedPojectDetails(query_id).subscribe((data: any)=>{
      if(data){
        this.projectdetails = data;
        console.log(this.projectdetails)
        this.project_name = this.projectdetails[0].project_name
        // this.mission_commander = this.projectdetails[0].mission_commander_id__first_name
        this.mission_commander = this.projectdetails[0].mission_commander_id__id
        this.start_date = this.projectdetails[0].start_date
        this.end_date = this.projectdetails[0].end_date
      }
      console.log("mission",this.mission_commander)
    });
    
    this.AuthService.getUserList(query).subscribe((data: any)=>{
      if(data){
        this.userlist = data;
      }
       console.log('user', data)

    });
  }
  ProjectList(){
    this.router.navigate(['/avmproject/project-list']);
  }
  UpdateProject() {
    console.log('this.end_date',this.end_date)
    console.log("end date test:", this.end_date);
    const format = 'YYYY-MM-dd';
    // const end_date = this.end_date;
    const locale = 'en-US';

    if(this.end_date!='' && this.end_date!= null){
      this.end_date = formatDate(this.end_date, format, locale);
    }
    if(this.start_date!='' && this.start_date!= null){
      this.start_date = formatDate(this.start_date, format, locale);
    }


    // this.success='false';
    this.msg='';
    
    this.is_projectname = false
    this.is_missioncommander = false
    this.is_startdate = false
    this.is_enddate = false

    this.start_date_error = ''
    this.end_date_error = ''
    // console.log(this.project_name)
    // console.log(this.mission_commander)
    let thirdDate = new Date('2001-01-01')

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

    else if(this.project_name != '' && this.mission_commander != '' && this.start_date != '' && this.start_date != null && this.end_date != '' && this.id){
        
      let query = {
        id: this.id,
        project_name: this.project_name,
        mission_commander: this.mission_commander,
        start_date: this.start_date,
        end_date: this.end_date,
      }
      console.log('mission_commander', query)
    this.AuthService.updateProjectdetails(query).subscribe((data: any)=>{
      if(data)
      {   
        if(data.success == 'true'){
        // this.success = data.success;
        this.msg =data.msg
        console.log('sisisi', data);
        this.update_st=true
        // this.router.navigate(['/project-list']);
        }else if(data.success=='exist')
        {
          this.update_st=false
          this.msg =data.msg
        }
        else{
          // console.log(data.msg);
          this.update_st=false
          this.msg =data.msg
        }
		
      }
      else{
        //error page
        this.update_st=false
        this.msg = 'Update Project Error!';
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

  OnCancel(){
    
    this.project_name =  this.projectdetails[0].project_name;
    this.mission_commander =  this.projectdetails[0].mission_commander_id__id;
    this.start_date =  this.projectdetails[0].start_date;
    this.end_date =  this.projectdetails[0].end_date;
  }

}

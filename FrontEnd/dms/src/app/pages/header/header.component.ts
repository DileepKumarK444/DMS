import { Component, OnInit, Renderer2, OnDestroy  } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import {SharedService} from '../../shared.service';
import { Subscription, interval } from 'rxjs';
import { environment } from '../../../environments/environment';


@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, OnDestroy  {
  name:any = '';
  username:any;
  last_name:any;
  role : any = '';
  menu_active = '';
  dronelist: any;
  permission: any;
  projectmenu_permission: boolean= false;
  usermenu_permission: boolean= false;
  image:any = '';
  dronelen: boolean = false;
  release_date:any = '';
  release_days:any ='';
  version:any;
  dDay:any;
  private subscription: Subscription;
  
    // version:any;
    public dateNow = new Date();
    // Release_date
    // public dDay = new Date(`${environment.RELEASE_DATE}`);
    // version = environment.VERSION;
    public ddddd = this.release_date;
    // version = environment.VERSION;

    milliSecondsInASecond = 1000;
    hoursInADay = 24;
    minutesInAnHour = 60;
    SecondsInAMinute  = 60;

    public timeDifference :any;
    public secondsToDday:any;
    public minutesToDday:any;
    public hoursToDday:any;
    public daysToDday:any;

  constructor(private AuthService:AuthService, 
    private router: Router,
    private renderer:Renderer2,
    private sharedService:SharedService 
    ) { 
      this.renderer.listen('window', 'click',(e:Event)=>{
        console.log("(e.target as Element).className", (e.target as Element).className);
        if(this.pClickSt==true && ((e.target as Element).className !='username') && ((e.target as Element).className !='fa fa-chevron-down mr-2 profile-down') && ((e.target as Element).className !='img-logo')  && ((e.target as Element).className !='img-logo ng-star-inserted')){
          this.pClickSt = false
        }
        if(this.help==true && ((e.target as Element).className !='cl-help')){
          this.help = false
        }
        // help
      })
    }
  
  //username: string = '';
  pClickSt: boolean = false;
  help: boolean = false;

  

  ngOnInit(): void {
    // let username = this.AuthService.getUsername();

    this.subscription = interval(1000)
           .subscribe(x => { this.getTimeDifference(); });
    // console.log('fsdfsdfsdfsdf')
    this.name = localStorage.getItem("name");
    this.username = localStorage.getItem("username");
    this.last_name = localStorage.getItem("last_name");

    this.role = localStorage.getItem("role");
    this.permission = localStorage.getItem("permissions");
    this.projectmenu_permission = this.permission.includes('project-menu');
    this.usermenu_permission = this.permission.includes('user-menu');


    console.log(this.name);
    console.log(this.username);

    console.log(this.role);
    this.AuthService.logincheck();

    this.AuthService.getReleasePlan().subscribe((data: any)=>{
      if(data)

      { 
        this.version = data.VERSION[0].conf_value;
        this.release_date = data.RELEASE_DATE[0].conf_value;
        this.release_days = data.RELEASE_DAYS[0].conf_value;
        console.log('version', this.version);
        console.log('releasedate', this.release_date);
        this.dDay = new Date(this.release_date);
        this.getTimeDifference();
      }
    });

    this.AuthService.getProfile().subscribe((data: any)=>{
      if(data)

      {   if(data.data)
            this.image = "data:image/png;base64,"+data.data
            else
          this.image = '../../assets/img/profile_new.jpg'
      }
    });
      this.AuthService.getDroneList().subscribe((data: any)=>{
      if(data){
        this.dronelist = data.data;
        console.log('this.dronelist',this.dronelist);
        console.log('dronelen', this.dronelen);
        if(this.dronelist.length == 0)
        {
          this.dronelen = true;
        }
        else{
          this.dronelen = false;

        }

      }

    });
  }


  getTimeDifference () {
        this.timeDifference = this.dDay.getTime() - new  Date().getTime();
        // console.log('timedifference', this.timeDifference);
        if(this.timeDifference>=0){
          this.allocateTimeUnits(this.timeDifference);
        }
    }

  allocateTimeUnits (timeDifference:any) {
        this.secondsToDday = Math.floor((timeDifference) / (this.milliSecondsInASecond) % this.SecondsInAMinute);
        this.minutesToDday = Math.floor((timeDifference) / (this.milliSecondsInASecond * this.minutesInAnHour) % this.SecondsInAMinute);
        this.hoursToDday = Math.floor((timeDifference) / (this.milliSecondsInASecond * this.minutesInAnHour * this.SecondsInAMinute) % this.hoursInADay);
        this.daysToDday = Math.floor((timeDifference) / (this.milliSecondsInASecond * this.minutesInAnHour * this.SecondsInAMinute * this.hoursInADay));
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
 }

  Logout(){
    this.AuthService.clearAuthData();
    this.AuthService.clearPermissions();
    localStorage.clear();
    // window.location.href = '/login' ;
    this.router.navigate(['/']);

  }
  downloadHelp(){
    console.log('Download Help Clicked')
  }
  UserList1()
  {
    console.log('HELP',this.help)
    if(this.help)
      this.help = false
      else
      this.help = true
  }
  profileMenuClick(){
    console.log(this.pClickSt)
    if(this.pClickSt)
      this.pClickSt = false
      else
      this.pClickSt = true
    
  }

  Profile(){
         this.router.navigate(['/avm/profile']);
  }
  DroneList(){
    this.router.navigate(['/drone/dashboard']);
  }
  ProjectList(){
    this.router.navigate(['/avmproject/project-list']);
  }

  UserList(){
  this.router.navigate(['/avmuser/sub-user-list']);
  }

  AddPilot(){
  this.router.navigate(['/avm/pilot']);
  }
  mouseEnter(menu:any){
    this.menu_active = menu;
  }
  mouseLeave(menu:any){
    if(this.menu_active != menu){
      this.menu_active = menu;
    }    
    this.menu_active ='';
  }
  DroneDetail(id:any){
    console.log('id', id);
    this.router.navigate(['/drone/drone-details', id]);
    this.sharedService.sendClickEvent(id);
  }
  LogoClick(){
    this.router.navigate(['/avm/dashboard']);
  }
}

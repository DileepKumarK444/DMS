import { AfterViewInit, Component, ViewChild, OnInit,enableProdMode, Renderer2,ElementRef  } from '@angular/core';
import {Chart,registerables } from 'chart.js'
import { AuthService } from '../services/auth.service';
import { environment } from '../../environments/environment';
import { Router, ActivatedRoute } from '@angular/router';
import { DatePipe } from '@angular/common'
import { HttpClient,HttpHeaders  } from '@angular/common/http';
import {SharedService} from '../shared.service';
import {Subscription} from 'rxjs';
import { formatDate } from '@angular/common';

// import {MatPaginator} from '@angular/material/paginator';
import { MatPaginator, PageEvent } from '@angular/material/paginator';
import {MatSort,Sort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';

import { interval, Observable } from 'rxjs';
import { mapTo, startWith, map, flatMap , mergeMap} from 'rxjs/operators';

// import { environment } from '../../environments/environment';
// import * as FileSaver from 'file-saver';
// import { exit } from 'process';
enableProdMode();
Chart.register(...registerables);
declare var jquery:any;
declare var $ :any;
declare var moment :any;

// interface IQuote {
//   categories: any[];
//   created_at: string,
//   icon_url: string;
//   id: string;
//   url: string;
//   value: string;
//   a: string;
//   cust_id:any[];
  
// }


@Component({
  selector: 'app-dashboard',
  templateUrl: './drone-details.component.html',
  styleUrls: ['./drone-details.component.scss', './drone-details.component2.scss'],
  providers: [DatePipe]
})
export class DroneDetailsComponent implements OnInit {
  // clickEventSubscription:Subscription;
  quote: any;
  
  dataSource:any;
  dataSourceRpt:any;
  drone_details:any = '';
  id: any;
  role:any = '';

  chart:any = [];
  chart1:any = [];
  download_log_permission:boolean=false;
  permission :any;

  // ELEMENT_DATA: USER[] = [];
  // isLoading = false;
  totalRows = 0;
  pageSize = environment.TABLE_ROW_LIMIT;
  currentPage = 0;
  count = 10;

  totalRowsRpt = 0;
  pageSizeRpt = environment.TABLE_ROW_LIMIT;
  currentPageRpt = 0;
  countRpt = 10;

  f_plan = 0
  f_project = 0
  f_date_from = ''
  f_date_to = ''
  f_time_from = ''
  f_time_to = ''
  filter = ''
  filter_rpt = ''
  pageSizeOptions: number[] = [5, 10, 25, 100];

  pageEvent: any;

  displayedColumns: string[] = ['id', 'log__plan__plan_date', 'log__plan__start_time', 'log__plan__end_time','log__plan__project__project_name','log__plan__plan','flight_time_max','flight_distance_max','download'];
      @ViewChild(MatPaginator) paginator: MatPaginator;
      @ViewChild(MatPaginator) paginator_rpt: MatPaginator;
      @ViewChild(MatSort) sort: MatSort;
      @ViewChild('sd') sdate : ElementRef;

      live_location:any;
      live_battery:any;
      live_altitude:any;
      live_flightDistance:any;
      live_flightTime:any;
      plan_name:any = ''
      project_name :any = ''
      scheduled_time :any = ''
      pilot_name :any = ''
      live_status:any = ''


   constructor(private AuthService:AuthService, 
      private router: Router,
      private activatedRoute: ActivatedRoute,
      public datepipe: DatePipe,
      private http: HttpClient,
      private renderer:Renderer2,
      private sharedService:SharedService) {
        this.renderer.listen('window', 'click',(e:Event)=>{
          if(this.fClickSt==true && ((e.target as Element).className !='form-control btn') && (((e.target as Element).className !='filter-container')&& ((e.target as Element).className !='filter-label')&& ((e.target as Element).className !='filter-span')&& ((e.target as Element).className !='filter-rb'))){
            console.log('fsdfsdfsdfsdf')
            this.fClickSt = false
          }

          if((e.target as Element).className =='applyBtn btn btn-sm btn-primary'){
            if(this.tab=='log')
              this.filterReport(false);
            // else if(this.tab=='reports')
            //   this.filterReportRpt();
          }

          // if((e.target as Element).className =='applyBtnRpt btn btn-sm btn-primary'){
          //   this.filterReportRpt(false);
          // }
        })

      // interval(2000)
      // .pipe(
      //   mergeMap(() => this.AuthService.getLiveData())
      // )
      // .subscribe(data => {
      //   console.log(data)
      //   this.time = data['clock.currentDate']
      // })
      let q={
        'drone_id':this.activatedRoute.snapshot.params['id']
      }
      interval(10000).pipe(
        mergeMap(() => this.AuthService.getLiveData(q))
      ).subscribe((data:any) => {
        console.log('DDDDDDDDDDDDDDDDDDD',data.data);
        // this.time = ''
        this.live_location = ''
        this.live_battery = ''
        this.live_altitude = ''
        this.live_flightDistance = ''
        this.live_flightTime = ''
        this.plan_name = ''
        this.project_name = ''
        this.scheduled_time = ''
        this.pilot_name = ''
        this.live_status = 'Inactive'
        if(data.data){
          // this.live_time = ''; //data.data['battery0.chargeState']
          this.live_location = data.data['gps.lat']+' - '+data.data['gps.lon']
          this.live_battery = data.data['battery0.instantPower']
          this.live_altitude = data.data['altitudeAMSL']
          this.live_flightDistance =data.data['flightDistance']
          this.live_flightTime = data.data['flightTime']
          this.plan_name = data.data['Plan']
          this.project_name = data.data['project']
          this.scheduled_time = data.data['scheduledtime']
          this.pilot_name = data.data['pilot']
          this.live_status = 'Active'
        }
        

      })
        
       }

       
    
    

   add_features : any = [];
   baseURL = environment.baseURL
  
   rule_ch:any = [];
   rule_all:any = false;
   approval_ch :any = [];
   approval_all :any = false;
   maintenance_ch :any = [];
   maintenance_all :any = false;
   plan_id:any = [];


   drone_list:any = [];
   schema:any = [];
   schema_details:any = [];
   
   tab:any = 'flight'
   checklist_st:any = ''

   rule_st:any = false
   maintenance_st:any = false
   approval_st:any = false

   rules:any = false
   maintenances:any = false
   approvals:any = false
   plan:any = ''
   
   
  //  project_name:any = ''
   
  //  pilot_name:any = ''
  //  scheduled_time:any = ''
   scheduled_date:any = ''
   flight_operation:any = ''
   flight_time:any = ''
   altitude:any = ''
   battery_consumed:any = ''
   distance_coverd:any = ''
   location:any = ''
   upcoming_plans:any =[]

   maintenance_data:any = ''
   approval_data:any = ''
   rule_data:any = ''

   is_active_plan:any = false;

   checklistData:any = []
   dashboard:any = true
   msg:any = ''
   save_status:any = false;
   msg_status:any = false;

   rpt_air_speed:any = [];
   rpt_flight_time:any = [];
   rpt_altitude_relative:any = [];
   report_data:any = [];
   logs:any = [];
   rt_panel:any = [];
   plan_rpt_name:any = [];

   plan_data:any = [];
   project_data:any = [];

   drone_id = ''
   filter_plan:any = []
   filter_project:any = []
   filter_from_dt:any = []
   filter_to_dt:any = []
   filter_limit:any = []

   filter_plan_rpt:any = []
   filter_project_rpt:any = []
   filter_from_dt_rpt:any = []
   filter_to_dt_rpt:any = []
   filter_limit_rpt:any = []

   ld_panel_down:any = true
   ld_panel_up:any = false
   
   typ:any ='';

   fClickSt: boolean = false;

   plan1:any = 'plan'

   img1:boolean = false;
   img2:boolean = false;
   togglest:boolean = false;

   image:any = '';
   image1:any = '';

   displayStyle = "none";
   displayStyleImg = 'none';
   vid_id:any= '1';
   video:any = '';
   currentRow:any = '';
   tr_id:any = '';
   image_prev:any = '';
   image_drone:any = '';
  //  img2:boolean = false;
  //  img3:boolean = false;
  observableData: Observable<any>;
  ngOnInit() {
    this.dataSource = {}
    this.dataSourceRpt = {}
    // while(true){
    //   setTimeout( () => { 
    //     console.log('API Call')
    //    }, 10 );
    // }
  //   $( document ).ready(function() {
  //   $('.applyBtn').on('click', function() {
  //     alert('sdfsdfsdfsdfsdf')
  //   });
  // });

  //   $( document ).ready(function() {
  //     setTimeout(function(){
  //     $('input[name="datetimes"]').daterangepicker({
  //       timePicker: true,
  //     });
  //   },100)
  // });
      
  //   setTimeout(function(){
  //     $('input[name="datetimes"]').daterangepicker();
  //  },1)

//   $(function() {
//     $( "#datepicker" ).datepicker();
// });

    

   this.role = localStorage.getItem("role");
   this.permission = localStorage.getItem("permissions");
   this.download_log_permission = this.permission.includes('download-log');

  //  this.rt_panel[0]=true;
   this.AuthService.logincheck();

   this.AuthService.getDroneList().subscribe((data: any)=>{
     
    this.drone_list = data.drone
    
   });
   this.id = this.activatedRoute.snapshot.params['id'];
   this.getDroneDetails(this.id);

   this.sharedService.menuClick$.subscribe(id =>{
    this.getDroneDetails(id);
    this.img1 = true;
    this.img2=false
   })

   
   
  //  this.AuthService.getDrone(this.id).subscribe((data: any)=>{
  //    this.drone_details = data;
  //  })
  }

  // ngAftervie
  // applyFilter(event: Event) {
  //   const filterValue = event.target.value.trim().toLowerCase();
  //   this.dataSource.filter = filterValue;
  //  }
  ldCardClick(){
    if(this.ld_panel_down){
      this.ld_panel_down = false
      this.ld_panel_up = true
    }
    else{
      this.ld_panel_down = true
      this.ld_panel_up = false
    }
  }
  test(e:Event, row:any,i:any){
    console.log(e)
    this.currentRow=i
    this.tr_id = i;
  }
  openPopupImg(id:any){
    
    // if(id==1)
    // this.image_prev = '../../assets/image1.png'
    // else 
    if(id==2)
    this.image_prev = '../../assets/image2.png'
    else  if(id==3)
    this.image_prev = '../../assets/image3.png'
    // else if(id==4)
    // this.image_prev = '../../assets/image4.png'
    else if(id==5)
    this.image_prev = '../../assets/image5.png'
    else if(id==6)
    this.image_prev = '../../assets/image6.png'
    this.displayStyleImg = "block";
  }
  closePopup() {
    this.displayStyle = "none";
  }
  closePopupImg() {
    this.displayStyleImg = "none";
  }
  openPopup(id:any) {
    this.vid_id = id
    if(id==1)
    this.video = '../../assets/video1.mp4'
    else if(id==2)
    this.video = '../../assets/video2.mp4'
    // if(id==3)
    // this.video = '../../assets/video3.mp4'
    // if(id==4)
    // this.video = '../../assets/video4.mp4'
    this.displayStyle = "block";
  }
  applyFilter(event: Event) {
    
    const filterValue = (event.target as HTMLInputElement).value;
    // this.dataSource.filter = filterValue.trim().toLowerCase();
    this.paginator.pageIndex = 0;
    this.currentPage = 0
    this.filter = filterValue.trim().toLowerCase();
    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
    this.loadData();

  }

  applyFilter1(event: Event) {
    
    const filterValue = (event.target as HTMLInputElement).value;
    // this.dataSource.filter = filterValue.trim().toLowerCase();
    // this.paginator_rpt.pageIndex = 0;
    // this.currentPageRpt = 0
    this.filter_rpt = filterValue.trim().toLowerCase();
    // if (this.dataSourceRpt.paginator) {
    //   this.dataSourceRpt.paginator.firstPage();
    // }
    // this.loadData1();

  }

  ClearFilter(){
    $('#datetimes').val('')
    $('#txt-search').val('')
    this.filter_plan[this.drone_id] = 0
    this.filter_project[this.drone_id] = 0
    this.filter  = ''
    this.filterReport(true);
  }

  ClearFilterRpt(){
    $('#datetimes-rpt').val('')
    $('#txt-search-rpt').val('')
    this.filter_plan_rpt[this.drone_id] = 0
    this.filter_project_rpt[this.drone_id] = 0
    this.filter_rpt  = ''
    this.filterReportRpt();
  }


  imgchange(id:any){
    if(id==1){
      this.img1=true
      this.img2=false
      // this.img3=false
    }
    else if(id==2){
      this.img1=false;
      this.img2=true
      // this.img3=false
    }
    if(this.togglest)
      this.toggleTitle(false)
  }
  //   else if(id==3){
  //     this.img1=false
  //     this.img2=false
  //     this.img3=true
  //   }
  //   this.toggleTitle(false)
  // }
  clickHandler(event:any){
    console.log("pageX: " + event.pageX + ", pageY: " + event.pageY)
  }
  toggleTitle(st:any){
    // alert('czxczxczxc')
    if(st)
      this.img1 = true;
    setTimeout(()=>{
      console.log(JSON.parse(this.schema_details))
    $("#Tokyo1").hotspot({
      mode: 'display',
      data: JSON.parse(this.schema_details),
      interactivity: "hover"
    }); 
    
    }, 300);
  }
  // ngAfterViewInit(){
  //   $(
  //     function() {
  //       // alert('sdfsdfs')
  //       // setTimeout(()=>{
  //       $('#datetimes').daterangepicker({
  //         timePicker: true,
          
  //         locale: {
  //           format: 'M/DD hh:mm A'
  //         }
  //       });
  //     // },500); 
  //     }
  // ); 
  // }
  
  // id = '0-dashboard'
  subId = 'flight'
  vTabId = ''
  handleChange(evt:any) {
    var target = evt.target;
    console.log(target)

  }
  changeType($event:any,val:any){
    console.log(val);
    this.typ=val;
  }


  mainTabClick(mTabId:any){
    this.id = mTabId
    this.subId = 'flight'
  }
  subTabClick(sTabId:any){
    this.subId = sTabId
  }

  verticalTabClick(d:any){
   
   if(this.vTabId == d)
      this.vTabId = ''
   else
   this.vTabId = d
   
  }
  dashboardClick(){
    this.dashboard=true
  }
  
    //   ngAfterViewInit() {
    //     this.dataSource.paginator = this.paginator;
    //     this.dataSource.sort = this.sort;
    //     // console.log('dfsdfsdfsddddddddddddddddddddddddddddddddddddddd')
    // }

    // applyFilter(event: Event) {
    //   const filterValue = (event.target as HTMLInputElement).value;
    //   this.dataSource.filter = filterValue.trim().toLowerCase();
  
    //   if (this.dataSource.paginator) {
    //     this.dataSource.paginator.firstPage();
    //   }
    // }

    // ngAfterViewInit(){
    //   this.dataSource = new MatTableDataSource(this.logs);

    //   // setTimeout(()=>{ 
    //   this.dataSource.paginator = this.paginator;
    //   this.dataSource.sort = this.sort;
    // // }, 3000);
    // }
    
  getDroneDetails(id:any)
  {

    
    this.dataSource = ''
    this.drone_details= [];
    this.drone_id = id
    this.tab ='flight'
    this.AuthService.getDrone(id).subscribe((data: any)=>{
      console.log(data)
      this.image_drone = "data:image/png;base64,"+data.dd
      this.drone_details = data.drone[0].model;
      this.schema_details = data.drone[0].schema
      this.upcoming_plans = []
      this.dashboard=false
      let today:any = ''
      let plan_date:any = ''
      let s_date:any = ''
      let e_date:any = ''
      let p_date:any = ''
      this.live_status = 'Inactive'
      // this.project_name = ''
      // this.plan_name = ''
      // this.pilot_name = ''
      // this.scheduled_time = ''
      this.scheduled_date = ''
      this.flight_operation = ''
      this.flight_time = ''
      this.altitude = ''
      this.battery_consumed = ''
      this.distance_coverd = ''
      this.location = ''
      
      this.rpt_air_speed = ''
      this.rpt_flight_time = ''
      this.rpt_altitude_relative = ''
      this.report_data = []
      this.logs=[];

      this.is_active_plan=false

      this.filter_plan[this.drone_id] = 0
      this.filter_project[this.drone_id] = 0
      this.filter_from_dt[this.drone_id] = ''
      this.filter_to_dt[this.drone_id] = ''
      this.filter_limit[this.drone_id] = 10

      this.filter_plan_rpt[this.drone_id] = 0
      this.filter_project_rpt[this.drone_id] = 0
      this.filter_from_dt_rpt[this.drone_id] = ''
      this.filter_to_dt_rpt[this.drone_id] = ''
      this.filter_limit_rpt[this.drone_id] = 10
      
      this.checklistData = (JSON.parse(data.checklist[0].fields.conf_value))
      this.project_data = data.project_data
      this.plan_data = data.plan_data


      this.rules = this.checklistData.rules
      
      this.maintenances = this.checklistData.maintanence
      this.approvals = this.checklistData.approval
      this.schema = []
      // console.log('data',data)
      this.schema = JSON.parse(data.schema[0].fields.additional_features)
      // console.log('schema length:', data.drone[0].additional_features);
      // if(data.drone[0].additional_features)
      
        this.add_features = JSON.parse(data.drone[0].additional_features)
      // else
      //   this.add_features =''
      
      // this.report_data = data.report_data
      this.logs = data.logs
    //   this.dataSource = new MatTableDataSource(data.logs);

    //   setTimeout(()=>{ 
    //   this.dataSource.paginator = this.paginator;
    //   this.dataSource.sort = this.sort;
    // }, 5000);
      
      this.plan = data.plan
      let st=''
      let et=''
      this.rule_ch = []
        this.maintenance_ch = []
        this.approval_ch = []
        this.rule_all = false
        this.maintenance_all = false
        this.approval_all = false
      for(let plan of data.plan){
        today=new Date();
        plan_date= plan.plan_date
        p_date =this.datepipe.transform(plan_date, 'yyyy-MM-dd')
        s_date = new Date(p_date)
        s_date.setHours(plan.start_time.split(':')[0]);
        s_date.setMinutes(plan.start_time.split(':')[1]);

        e_date = new Date(p_date)
        e_date.setHours(plan.end_time.split(':')[0]);
        e_date.setMinutes(plan.end_time.split(':')[1]);
        
        if(today > s_date && today < e_date){
// Read live data from log file
          // interval(2000).pipe(
          //   mergeMap(() => this.AuthService.getLiveData())
          // ).subscribe(data => {
          //   console.log(data)
          //   this.time = ''
          // })

// End here        

          this.is_active_plan = true
          this.live_status = 'Active'
          // this.project_name = plan.project_id__project_name
          // this.plan_name = plan.plan
          // this.pilot_name = plan.pilot_id__first_name
          st = plan.start_time.split(':');
          et = plan.end_time.split(':');
          this.scheduled_date = plan.plan_date
          // this.scheduled_time = st[0]+':'+st[1] +' - '+ et[0]+':'+et[1]
          this.flight_operation = ""
          this.plan_id = plan.id
          let query = {
              id: plan.id
            }
          setTimeout(() => {
            this.AuthService.getChecklist(query).subscribe((datas: any)=>{
              
              for(let data of Object.keys(datas)){
                
                if(data == 'rules'){
                  let all = false
                  this.rule_data = JSON.parse(datas[data][0].schema)
                  if(this.rule_data.checked_all == true)
                    all = true
                  this.rule_all = all
                  for(let d of this.rule_data.rules){
                    
                    let c = false
                    if(d.checked == true)
                      c= true
                    this.rule_ch[d.id] = c
                    
                  }
                }
                else if(data == 'maintanence'){

                  this.maintenance_data = JSON.parse(datas[data][0].schema)
                  let all = false
                  if(this.maintenance_data.checked_all == true)
                    all = true
                  this.maintenance_all = all
                  for(let m of this.maintenance_data.maintenance){
                    let c = false
                    if(m.checked == true)
                      c= true
                    this.maintenance_ch[m.id] = c
                  }
                }
                else if(data == 'approvals'){
                  this.approval_data = JSON.parse(datas[data][0].schema)
                  let all = false
                  if(this.approval_data.checked_all == true)
                    all = true
                  this.approval_all = all
                  for(let p of this.approval_data.approval){
                    let c = false
                    if(p.checked == true)
                      c= true
                    this.approval_ch[p.id] = c
                    
                  }
                }
                
              }
            });
          }, 100);

        }
        else if(today < e_date){
          if(this.upcoming_plans.length < 5){
            this.upcoming_plans.push(plan)
          }
        }
        
      }
      console.log('schedulelen',this.upcoming_plans.length)
     });
  }

  // filterReport(){

    
  //   let query = {
  //     drone_id : this.drone_id,
  //     filter_plan : this.filter_plan[this.drone_id],
  //     filter_project : this.filter_project[this.drone_id],
  //     filter_from_dt : this.filter_from_dt[this.drone_id],
  //     filter_to_dt : this.filter_to_dt[this.drone_id],
  //     filter_limit : Number(this.filter_limit[this.drone_id])
  //   }

  //   this.tabClick(query,'reports')
  //   // this.AuthService.getFilteredReports(query).subscribe((data: any)=>{
  //   //   this.report_data = data.report_data
  //   //   this.tabClick('reports',false,data.report_data)
  //   // });

    
  // }

  onRuleClick1(id:any){
    var keepGoing = true;
    (this.rules).forEach((d:any, i:any) => {
      if(keepGoing) {
        if(this.rule_ch[d.id])
        {
          this.rule_all = true
        }
        else{
          this.rule_all = false
          keepGoing = false;
        }
      }
    });

  }

  onMaintenanceClick1(id:any){
    var keepGoing = true;
    (this.maintenances).forEach((d:any, i:any) => {
      if(keepGoing) {
        if(this.maintenance_ch[d.id])
        {
          this.maintenance_all = true
        }
        else{
          this.maintenance_all = false
          keepGoing = false;
        }
      }
    });
    
  }

  onApprovalClick1(id:any){
    var keepGoing = true;
    (this.approvals).forEach((d:any, i:any) => {
      if(keepGoing) {
        if(this.approval_ch[d.id])
        {
          this.approval_all = true
        }
        else{
          this.approval_all = false
          keepGoing = false;
        }
      }
    });
    
  }

  save_checklist(){
    let rule_data:any = [];
    let r_data:any = [];

    let maintenance_data:any = [];
    let m_data:any = [];

    let approval_data:any = [];
    let a_data:any = [];
    
    (this.checklistData.rules).forEach((d:any, i:any) => {
      
      if( this.rule_ch[d.id] ==undefined || this.rule_ch[d.id] ==false){
        this.rule_ch[d.id] = false
      }
      r_data.push({"id":d.id,"val":d.val,"checked":this.rule_ch[d.id]})
    });

    rule_data.push({"checked_all":this.rule_all,"rules":r_data});

    (this.checklistData.maintanence).forEach((d:any, i:any) => {
      
      if( this.maintenance_ch[d.id] ==undefined || this.maintenance_ch[d.id] ==false){
        this.maintenance_ch[d.id] = false
      }
      m_data.push({"id":d.id,"val":d.val,"checked":this.maintenance_ch[d.id]})
    });

    maintenance_data.push({"checked_all":this.maintenance_all,"maintenance":m_data});
    
    (this.checklistData.approval).forEach((d:any, i:any) => {
      
      if( this.approval_ch[d.id] ==undefined || this.approval_ch[d.id] ==false){
        this.approval_ch[d.id] = false
      }
      a_data.push({"id":d.id,"val":d.val,"checked":this.approval_ch[d.id]})
    });

    approval_data.push({"checked_all":this.approval_all,"approval":a_data});

    let body = {
        plan_id : this.plan_id,
        rule_data : (rule_data),
        maintenance_data : (maintenance_data),
        approval_data : (approval_data)
      }
    
    this.AuthService.saveChecklist(body).subscribe((data: any)=>{
      this.msg=''
      if(data.status){
        this.save_status = true;
        this.msg_status = true;
        this.msg='Checklist Saved Successfully!'
        setTimeout(() => {
          this.msg_status = false;
        },2500)

      }
      else{
        this.save_status = false;
        this.msg_status = true;
        this.msg='Error on save!'
        setTimeout(() => {
          this.msg_status = false;
        },2500)
      }
      
    });
  }
  
  tabClick(q:any,t:any){
    // alert(t)
    this.tab = t;
    this.chart=[];
    this.chart1=[];
    this.report_data = [];
    this.image = ''
    this.image1 = ''
    this.f_plan = 0
    this.f_project = 0
    this.f_date_from = ''
    this.f_date_to = ''
    this.filter = ''
    this.filter_rpt = ''

    
    if(t=='reports')
    {
      
      setTimeout(() => {
        $('#cb-project-rpt').val(0)
        $('#cb-plan-rpt').val(0)
        $('input[name="datetimes-rpt"]').daterangepicker({
          timePicker: true,
          locale: {
            format: 'MM/DD/YYYY HH:mm:ss'
          }
      });
      if(this.f_date_from=='')
      $('input[name="datetimes-rpt"]').val('')
    },300);

      let  q = {
        drone_id : this.drone_id,
        pageSize : this.pageSizeRpt,
        currentPage : this.currentPageRpt+1,
        filter_plan : 0,
        filter_project : 0,
        filter_from_dt : '',
        filter_to_dt : '',
        filter_rpt : '',
        time_from : '',
        time_to : '',
        
      }

      this.AuthService.getFilteredReports(q).subscribe((data: any)=>{
        console.log('data.results',data.results)
        this.report_data = ''
        this.report_data = data.results
        this.countRpt = data.count
        this.dataSourceRpt = new MatTableDataSource(this.report_data);
          
      this.observableData = this.dataSourceRpt.connect();
      // this.dataSourceRpt.paginator = this.paginator_rpt;
        this.renderReport(data.results)
        
      });
      
    }
    else if(t=='more'){
     
      q = {
        id : this.drone_id,
      }
      this.AuthService.getDroneImage(q).subscribe((data: any)=>{
        
        if(data.data){
          this.image = "data:image/png;base64,"+data.data
          this.togglest = true
          this.toggleTitle(true)
        }
        else
        {
          this.image ='../../assets/img/nopreview.jpg'
          this.togglest = false
        }
          
        if(data.data1)
          this.image1 = "data:image/png;base64,"+data.data1
        else
          this.image1 ='../../assets/img/nopreview.jpg'
        
      });
      
      
    }
    else if(t=='log'){
      
      if(q=='')
      {
        q = {
          drone_id : this.drone_id,
          
        }
      }
      this.loadData();
    
    }



  }

  filterReport(status: any){
    // console.log(status);
    if (status = 'true')
    {
      let Id = this.filter_project[this.drone_id]
      console.log('Project IUD', this.filter_project[this.drone_id])
      console.log('drone_id IUD', this.drone_id)

      let q = {
        drone : this.drone_id,
        project_id : Id
      }

      this.AuthService.getPlans(q).subscribe((data: any)=>{
        console.log(data.plan_data)
        this.plan_data = data.plan_data
        
      });
      //
      
    }
    console.log($('#datetimes').val())
    let datetime = $('#datetimes').val()
    this.f_date_from = ''
    this.f_date_to = ''
    this.f_time_from = ''
    this.f_time_to = ''
    if(datetime!=''){
      let dt_from = (datetime.split(' - ',2)[0].split(' ',2))
      let dt_to = (datetime.split(' - ',2)[1].split(' ',2))

      const format = 'YYYY-MM-dd';
      const locale = 'en-US';
      // const end_date = formatDate(this.end_date, format, locale);
      this.f_date_from = formatDate(dt_from[0], format, locale);
      this.f_date_to = formatDate(dt_to[0], format, locale);
      this.f_time_from = dt_from[1]
      this.f_time_to = dt_to[1]
    }
    // console.log(dt_to)
    this.paginator.pageIndex = 0;
    this.currentPage = 0
    this.f_plan = this.filter_plan[this.drone_id]
    this.f_project = this.filter_project[this.drone_id]
    //     filter_project : this.filter_project[this.drone_id],
    //     filter_from_dt : this.filter_from_dt[this.drone_id],
    
    this.loadData();
  
  }
  getPlanData(){
      let Id = this.filter_project_rpt[this.drone_id]
      let q = {
        drone : this.drone_id,
        project_id : Id
      }

      this.AuthService.getPlans(q).subscribe((data: any)=>{
        this.plan_data = data.plan_data
        
      });
    
  }

  filterReportRpt(){
    
    let datetime = $('#datetimes-rpt').val()
    this.f_date_from = ''
    this.f_date_to = ''
    this.f_time_from = ''
    this.f_time_to = ''
    if(datetime!=''){
      let dt_from = (datetime.split(' - ',2)[0].split(' ',2))
      let dt_to = (datetime.split(' - ',2)[1].split(' ',2))

      const format = 'YYYY-MM-dd';
      const locale = 'en-US';
      this.f_date_from = formatDate(dt_from[0], format, locale);
      this.f_date_to = formatDate(dt_to[0], format, locale);
      this.f_time_from = dt_from[1]
      this.f_time_to = dt_to[1]
    }
    this.paginator_rpt.pageIndex = 0;
    this.currentPageRpt = 0
    this.f_plan = this.filter_plan_rpt[this.drone_id]
    this.f_project = this.filter_project_rpt[this.drone_id]
    
    this.loadData1();

  
  }

  loadData1() {
    // this.paginator_rpt.pageIndex = 0;
    // this.currentPageRpt = 0
    console.log('this.filter_project_rpt[this.drone_id]',this.filter_project_rpt[this.drone_id])
    let  q = {
      drone_id : this.drone_id,
      pageSize : this.pageSizeRpt,
      currentPage : this.currentPageRpt+1,

      filter_plan : this.filter_plan_rpt[this.drone_id],
      filter_project : this.filter_project_rpt[this.drone_id],
      filter_from_dt : this.f_date_from,
      filter_to_dt : this.f_date_to,
      time_from : this.f_time_from,
      time_to : this.f_time_to,
      
      filter_limit : 0,
      filter_rpt : this.filter_rpt
      
    }
    this.dataSourceRpt = ''
    this.AuthService.getFilteredReports(q).subscribe((data: any)=>{
      this.dataSourceRpt = new MatTableDataSource(data.results);
      this.countRpt = data.count
      this.observableData = this.dataSourceRpt.connect();
      if (this.dataSourceRpt.paginator) {
        this.dataSourceRpt.paginator.firstPage();
      }

      (data.results).forEach((d:any, i:any) => {
          console.log(this.chart[i])
          if (this.chart[i]) {
            this.chart[i].destroy();
    
          }
          if (this.chart1[i]) {
            this.chart1[i].destroy();
    
          }
        })

      // this.dataSourceRpt.paginator = this.paginator_rpt;
      setTimeout(() => {
        this.renderReport(data.results)
      },1000);
      
      // console.log('renderReport')
    });

    $('input[name="datetimes-rpt"]').daterangepicker({
      timePicker: true,
      // startDate: moment().startOf('hour'),
      // endDate: moment().startOf('hour').add(32, 'hour'),
      locale: {
        format: 'MM/DD/YYYY HH:mm:ss'
      }
    });
    if(this.f_date_from=='')
      $('input[name="datetimes-rpt"]').val('')
    
    
  }

  loadData() {
    let  q = {
        drone_id : this.drone_id,
        pageSize : this.pageSize,
        currentPage : this.currentPage+1,
        f_plan :this.f_plan ,
        f_project:this.f_project,
        f_date_from : this.f_date_from,
        f_date_to : this.f_date_to,
        f_time_from : this.f_time_from,
        f_time_to : this.f_time_to,
        filter:this.filter
        
      }
    
    this.AuthService.getDroneLogApi(q).subscribe((data: any)=>{
      this.logs = data
      this.count = data.count
      this.dataSource = new MatTableDataSource(data.results);

      

      setTimeout(() => {

        this.dataSource.sortingDataAccessor = (item:any, property:any) => {
          switch(property) {
            case 'log__plan__plan_date': return item.log.plan.plan_date;
            case 'log__plan__start_time': return item.log.plan.start_time;
            case 'log__plan__end_time': return item.log.plan.end_time;
            case 'log__plan__project__project_name': return item.log.plan.project.project_name;
            case 'log__plan__plan': return item.log.plan.plan;
            
            default: return item[property];
          }
        };
        this.dataSource.sort = this.sort;

        this.dataSource.filterPredicate = (data:any, filter:any) => {
          return data.log.plan.plan.toLocaleLowerCase().includes(filter) ||
            data.log.plan.project.project_name.toLocaleLowerCase().includes(filter) ||
            data.log.plan.plan_date.toLocaleLowerCase().includes(filter) ||
            data.log.plan.start_time.toLocaleLowerCase().includes(filter) ||
            data.flight_time_max.toLocaleLowerCase().includes(filter) ||
            data.flight_distance_max.toLocaleLowerCase().includes(filter) ||
            data.log.plan.end_time.toLocaleLowerCase().includes(filter) ;
        };

        $('input[name="datetimes"]').daterangepicker({
          timePicker: true,
          // startDate: moment().startOf('hour'),
          // endDate: moment().startOf('hour').add(32, 'hour'),
          locale: {
            format: 'MM/DD/YYYY HH:mm:ss'
          }
        });
        if(this.f_date_from=='')
          $('input[name="datetimes"]').val('')
        
      // this.dataSource.sort = this.sort;
      },300);
  });
  }
  
  pageChanged(event: PageEvent) {
    console.log({ event });
    this.pageSize = event.pageSize;
    this.currentPage = event.pageIndex;
    this.count =event.length;
    this.loadData();
  }

  pageChangedRpt(event: PageEvent) {
    console.log({ event });
    this.pageSizeRpt = event.pageSize;
    this.currentPageRpt = event.pageIndex;
    this.countRpt =event.length;
    this.loadData1();
  }

  filterClick(){
    console.log(this.fClickSt == true)
    if(this.fClickSt)
      this.fClickSt = false
    else
      this.fClickSt = true
    console.log(this.fClickSt == true)
  }
  renderReport(data:any){
    (data).forEach((d:any, i:any) => {
      console.log('IIIIIIIIIII',data)
      this.plan_rpt_name[i] = d.log__plan__plan;
      
      

    
      setTimeout(() => {
        // if (this.chart[i]) {
        //   this.chart[i].destroy();
  
        // }
      this.chart[i] = new Chart('airspeed_'+i, {
        type: 'line',
        data: {
            labels:JSON.parse(d.flight_time),
            datasets: [{
                label: 'Air Speed',
                data: JSON.parse(d.air_speed),
                fill:false,
                backgroundColor:'#F15722',
                borderColor:"#F15722",
                borderWidth: 1,
                pointRadius: 0,
                
            }]
        },
        options: {
          
          scales: {
            y: {
              title: {
                display: true,
                text: 'Air Speed (mph)',
                font: {
                    size: 15
                }
            },
              ticks: {
                  stepSize: 1
              }
          },
          
          
            xAxes: {
                title: {
                    display: true,
                    text: 'Time(s)',
                    font: {
                        size: 15
                    }
                },
                ticks: {
                  autoSkip: true,
                  maxTicksLimit: 20
              }
            }
        }
        }
        
      });
    },1000)
  
    
    setTimeout(() => {
      // console.log(this.chart1[i],i)
      // var chartExist = Chart.getChart(i); // <canvas> id
      // if (chartExist != undefined)  
      //   this.chart1[i]=''
      // if (this.chart1[i]) {
      //   this.chart1[i].destroy();
  
      // }
      this.chart1[i] = new Chart('altitude_'+i, {
        type: 'line',
        data: {
            labels:JSON.parse(d.flight_time),
            datasets: [{
                label: 'Altitude Relative',
                data: JSON.parse(d.altitude_relative),
                fill:false,
                backgroundColor:'#4B4A50',
                borderColor:"#4B4A50",
                borderWidth: 1,
                pointRadius: 0,
                
            }]
        },
        options: {
          
          scales: {
            y: {
              title: {
                display: true,
                text: 'Altitude Relative (m)',
                font: {
                    size: 15
                }
            },
              ticks: {
                  stepSize: 1
              }
          },
          
          
            xAxes: {
                title: {
                    display: true,
                    text: 'Time(s)',
                    font: {
                        size: 15
                    }
                },
                ticks: {
                  autoSkip: true,
                  maxTicksLimit: 20
              }
            }
        }
        }
        
      });
    },1000)
  

    });
    // this.dataSourceRpt = new MatTableDataSource(this.report_data);
        
    // this.observableData = this.dataSourceRpt.connect();
    // this.dataSourceRpt.paginator = this.paginator_rpt;
    console.log('renderReport')
  }

  file_download(id:any){
    let body = {
      log_id : id
    }
  
    this.AuthService.downloadLog(body).subscribe((response: any)=>{
      let binaryData = [];
      binaryData.push(response.data);
      let downloadLink = document.createElement('a');
      downloadLink.href = window.URL.createObjectURL(new Blob(binaryData, {type: 'text/csv'}));
      downloadLink.setAttribute('download', response.filename);
      document.body.appendChild(downloadLink);
      downloadLink.click();
  }
    );
  }
  downloadFile(data:any) {
    const blob = new Blob([data], { type: 'text/csv' });
    const url= window.URL.createObjectURL(blob);
    window.open(url);
  }
  rtCardClick(idx:any){
    this.rt_panel[idx] = !this.rt_panel[idx]
  }
  ruleCLick(){
    this.maintenance_st = false
    this.approval_st = false
    this.rule_st = !this.rule_st
  }
  maintenanceCLick(){
    this.maintenance_st = !this.maintenance_st
    this.approval_st = false
    this.rule_st = false
  }
  approvalCLick(){
    this.approval_st = !this.approval_st
    this.maintenance_st = false
    this.rule_st = false
  }
  

}


import { Injectable } from '@angular/core';
import { HttpClient,HttpHeaders  } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient,
    private router: Router
    ) { }
  
  requestToken(query: any)
  {
    return this.http.post<any>(`${environment.apiURL}/api/token-auth/`, query);
  }

  getProcess(query: any)
  {
    // let token = localStorage.getItem("token");
    //console.log(headers)
    return this.http.post<any>(`${environment.apiURL}/api/login/`, query);
  }

  saveAuth(token: string) {
      localStorage.setItem("token", token);
  }

  getToken() {
      return localStorage.getItem('token');
  }

  getReleasePlan() {
    return this.http.get<any>(`${environment.apiURL}/api/get_release_plan/`);
  }

  clearAuthData() {
    localStorage.removeItem("token");
  }
  
  logincheck(){
    const authToken = this.getToken();
    // console.log(authToken)
    if (!authToken) {
      this.router.navigate(['/login']);
    }
  }

  permissionCheck(){
    return this.http.get<any>(`${environment.apiURL}/api/role_permissions/`);
  }
  
  getUsername() {
    return localStorage.getItem('username');
  }

  getName() {
    return localStorage.getItem('name');
  }

  savePermissions(permissions: string, username: string, name:string, customer_id:string, role:string, last_name:string, customer_name:string) {
    localStorage.setItem("username", username);
    localStorage.setItem("name", name);
    localStorage.setItem("permissions", JSON.stringify(permissions));
    localStorage.setItem("customer_id", customer_id);
    localStorage.setItem("role", role);
    localStorage.setItem("last_name", last_name);
    localStorage.setItem("customer_name", customer_name);

  }

  getRole() {
    return localStorage.getItem('role');
  }

  clearPermissions() {
    localStorage.removeItem("permissions");
    localStorage.removeItem("username");
    localStorage.removeItem("name");
    localStorage.removeItem("customer_id");
    localStorage.removeItem("role");
    localStorage.removeItem("last_name");
    localStorage.removeItem("customer_name");

  }

  getCustomerid() {
    return localStorage.getItem('customer_id');
  }

  getProfile(){
    return this.http.get<any>(`${environment.apiURL}/api/get_customer_details/`);
  }

  saveUserdetails(query: any)
  {
    const formData = new FormData(); 
        
    // Store form name as "file" with file data
    if(query.file)
      formData.append("file", query.file, query.file.name);
    else
      formData.append("file", '');
    // formData.append("id", query.id);
    console.log('query.profile_schema_model',query.profile_schema_model)
    formData.append("first_name", query.first_name);
    formData.append("last_name", query.last_name);
    formData.append("email", query.email);
    formData.append("phone", query.phone);
    formData.append("pilot", query.pilot);
    formData.append("pilot_license", query.pilot_license);
    formData.append("description", query.description);
    formData.append("customer_id", query.customer_id);
    formData.append("add_fields", query.add_fields);

    var dict:any = {}; // create an empty array

    for (let key in (query.profile_schema_model)) {
      if((query.profile_schema_model)[key]!=undefined){
        dict[key] =  (query.profile_schema_model)[key]
      }
    }
    formData.append("profile_schema_model", JSON.stringify(dict));
    
    // formData.append("id", query.id);

    // first_name: this.firstname,
    //     last_name: this.lastname,
    //     email: this.email,
    //     phone: this.phone,
    //     pilot: this.pilot,
    //     pilot_license: this.pilot_license,
    //     description: this.description,
    //     customer_id: this.custid,

    return this.http.post<any>(`${environment.apiURL}/api/save_user_details/`, formData);
  }

  UpdateUserdetails(query: any)
  {

    const formData = new FormData(); 
        
    // Store form name as "file" with file data
    if(query.file)
      formData.append("file", query.file, query.file.name);
    else
      formData.append("file", '');
    // formData.append("id", query.id);
    
    
    formData.append("id", query.id);
    formData.append("first_name", query.first_name);
    formData.append("last_name", query.last_name);
    formData.append("email", query.email);
    formData.append("phone", query.phone);
    formData.append("pilot", query.pilot);
    formData.append("pilot_license", query.pilot_license);
    formData.append("description", query.description);
    formData.append("customer_id", query.customer_id);
    formData.append("add_fields", query.add_fields);
    var dict:any = {}; // create an empty array

    for (let key in (query.profile_schema_model)) {
      if((query.profile_schema_model)[key]!=undefined){
        dict[key] =  (query.profile_schema_model)[key]
      }
    }
    formData.append("profile_schema_model", JSON.stringify(dict));

    return this.http.post<any>(`${environment.apiURL}/api/update_user/`, formData);
  }

  getUserList(query: any)
  {
    return this.http.post<any>(`${environment.apiURL}/api/get_user_list/`, query);
  }
  
  addProject(query: any)
  {
    return this.http.post<any>(`${environment.apiURL}/api/add_project/`, query);
  }

  getPilotList(query: any)
  {
    return this.http.post<any>(`${environment.apiURL}/api/get_pilot_list/`, query);
  }
 

  getProjectList()
  {
    return this.http.get<any>(`${environment.apiURL}/api/get_project_list/`);
  }
  
  addPilot(body: any)
  {
    // console.log(body)
    const headers = new HttpHeaders().set('Content-Type', 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW');
// return this.httpClient.post<T>(this.httpUtilService.prepareUrlForRequest(url), body, {headers: headers})

    return this.http.post<any>(`${environment.apiURL}/api/add_pilot/`, body, {headers: headers});
  }
  // getDroneDetails(){
  //   return this.http.get<any>(`${environment.apiURL}/api/get_drone_details/`);
  // }

  getSelectedUserDetails(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/get_sel_user/`, body);
  }

  deleteUser(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/delete_user/`, body);
  }

  deleteProject(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/delete_project/`, body);
  }

  getSelectedPojectDetails(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/get_sel_project/`, body);
  }

  updateProjectdetails(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/update_project/`, body);
  }


  getChecklist(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/get_checklist/`, body);
  }

  saveChecklist(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/save_checklist/`, body);
  }

  getDroneList(){
    return this.http.get<any>(`${environment.apiURL}/api/get_dashboard_data/`);
  }
  getDrone(id:any){
    return this.http.post<any>(`${environment.apiURL}/api/get_drone/`,id);
  }

  downloadLog(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/download_log/`, body);
  }

  // getFilteredReports(body: any){
  //   return this.http.post<any>(`${environment.apiURL}/api/get_filtered_reports/`, body);
  // }
  getDroneLog(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/get_drone_log/`, body);
  }

  getDroneLogApi(body: any){
    console.log(body)
    const formData = new FormData(); 
    formData.append("drone_id", body.drone_id);
    formData.append("plan", body.f_plan);
    formData.append("project", body.f_project);

    formData.append("date_from", body.f_date_from);
    formData.append("date_to", body.f_date_to);
    formData.append("time_from", body.f_time_from);
    formData.append("time_to", body.f_time_to);
    formData.append("filter", body.filter);

    return this.http.post<any>(`${environment.apiURL}/api/api_logs_view/?page=${body.currentPage}&offset=${body.pageSize}`, formData);
  }

  getFilteredReports(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/get_filtered_reports/?page=${body.currentPage}&offset=${body.pageSize}`, body);
  }

  getLiveData(body: any){
    // const formData = new FormData(); 
    // formData.append("drone_id", body.drone_id);
    return this.http.get<any>(`${environment.apiURL}/api/read_data/?drone_id=${body.drone_id}`, body);
  }

  requestpasswordReset(body:any){
    return this.http.post<any>(`${environment.apiURL}/api/forgot_password/`, body);
  }
  
  upload(data:any){
    const formData = new FormData(); 
        
      // Store form name as "file" with file data
      formData.append("file", data.file, data.file.name);
      formData.append("id", data.id);
        
      // Make http post request over api
      // with formData as req
      return this.http.post<any>(`${environment.apiURL}/api/file_upload/`, formData);
  }

  downloadLicence(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/download_licence/`, body);
  }
  ChangePassword(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/change_password/`, body);
  }
  
  getDroneImage(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/get_drone_image/`, body);
  }

  // getLoginToken(body: any){
  //   return this.http.post<any>(`${environment.apiURL}/api/get_login_token/`, body);
  // }

  getProfileSchema(){
    return this.http.post<any>(`${environment.apiURL}/api/get_profile_schema/`,'');
  }
  getPlans(body: any){
    return this.http.post<any>(`${environment.apiURL}/api/get_plan/`, body);
  }
  
  
  // 
  
}

import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent, HttpResponse, HttpErrorResponse } from "@angular/common/http";
import { Injectable } from "@angular/core";
//import 'rxjs/add/operator/do';
import { AuthService } from './auth.service';
import { Router } from "@angular/router";
// import { Observable } from "rxjs";
// import {tap} from 'rxjs/internal/operators';
import { tap } from 'rxjs/operators';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private AuthService: AuthService,
    private router: Router
  ) { }

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    const authToken = this.AuthService.getToken();
    // console.log('authToken',authToken)
    if (authToken) {
      const authRequest = req.clone({
        headers: req.headers.set("Authorization", `Token ${authToken}`)
      });
      // console.log('authRequest',authRequest)
      return next.handle(authRequest).pipe(tap((event: HttpEvent<any>) => {
        if (event instanceof HttpResponse) {
          // do stuff with response if you want
        }
      }, (err: any) => {
        if (err instanceof HttpErrorResponse) {
          if (err.status === 401) {
            // console.log('404 - Session Expired');
            this.AuthService.clearAuthData();
            this.router.navigate(['/login']);
            // this.authService.sessionExpired(true);
          }
        }
      }));
    } else {
      return next.handle(req);
      // console.log('authRequest','authRequest')
    }
  }
}

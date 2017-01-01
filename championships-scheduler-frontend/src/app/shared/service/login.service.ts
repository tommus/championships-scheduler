import {Injectable} from "@angular/core";
import {Http} from "@angular/http";
import {Observable} from "rxjs";
import {Credentials} from "../model/credentials";
import {ProfileService} from "./profile.service";

@Injectable()
export class LoginService {
  private loginUrl: string = 'http://localhost:8000/api/login/';

  constructor(private http: Http,
              private profileService: ProfileService) {
  }

  login(username: string, password: string): Observable<Credentials> {
    return this.http
      .post(this.loginUrl, {'username': username, 'password': password})
      .map(response => {
        this.persistAuthToken(username, password);
        return new Credentials(username, password);
      }, error => {
        this.profileService.removeAuthToken();
        return Observable.throw(new Error(error));
      })
  }

  logout(): Observable<{}> {
    this.profileService.removeAuthToken();
    return Observable.of({});
  }

  private persistAuthToken(username: string, password: string): void {
    let token = 'Basic ' + btoa(username + ':' + password);
    this.profileService.setAuthToken(token);
  }
}

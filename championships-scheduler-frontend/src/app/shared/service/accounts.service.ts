import {Injectable} from "@angular/core";
import {Headers, Http, URLSearchParams} from "@angular/http";
import {ProfileService} from "./profile.service";
import {Observable} from "rxjs";
import {User} from "../model/user";

@Injectable()
export class AccountsService {
  private url: string = 'http://192.168.1.102:8000/api/accounts/users/';
  private headers = new Headers();

  constructor(private http: Http, profileService: ProfileService) {
    this.headers.append('Authorization', profileService.getAuthToken());
  }

  getUsers(): Observable<User[]> {
    return this.http
      .get(this.url, {headers: this.headers})
      .map(response => response.json() as User[]);
  }

  getUserById(id: number): Observable<User> {
    return this.http
      .get(this.url + id + '/', {headers: this.headers})
      .map(response => response.json() as User);
  }

  getChampionshipUsers(id: number): Observable<User[]> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('championship', '' + id);

    return this.http
      .get(this.url, {headers: this.headers, search: params})
      .map(response => response.json() as User[]);
  }
}

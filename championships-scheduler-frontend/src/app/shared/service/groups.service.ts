import {Injectable} from "@angular/core";
import {Headers, Http, URLSearchParams} from "@angular/http";
import {ProfileService} from "./profile.service";
import {Observable} from "rxjs";
import {Group} from "../model/group";

@Injectable()
export class GroupsService {
  private url: string = 'http://localhost:8000/api/championships/groups/';
  private headers = new Headers();

  constructor(private http: Http, profileService: ProfileService) {
    this.headers.append('Authorization', profileService.getAuthToken());
  }

  getGroups(): Observable<Group[]> {
    return this.http
      .get(this.url, {headers: this.headers})
      .map(response => response.json() as Group[]);
  }

  getChampionshipGroups(id: number): Observable<Group[]> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('championship', '' + id);

    return this.http
      .get(this.url, {headers: this.headers, search: params})
      .map(response => response.json() as Group[]);
  }
}

import {Injectable} from "@angular/core";
import {Headers, Http, URLSearchParams} from "@angular/http";
import {ProfileService} from "./profile.service";
import {Observable} from "rxjs";
import {Team} from "../model/team";

@Injectable()
export class TeamsService {
  private url: string = 'http://192.168.1.102:8000/api/championships/teams/';
  private headers = new Headers();

  constructor(private http: Http, profileService: ProfileService) {
    this.headers.append('Authorization', profileService.getAuthToken());
  }

  getTeams(): Observable<Team[]> {
    return this.http
      .get(this.url, {headers: this.headers})
      .map(response => response.json() as Team[]);
  }

  getTeamById(id: number): Observable<Team> {
    return this.http
      .get(this.url + id + '/', {headers: this.headers})
      .map(response => response.json() as Team);
  }

  getChampionshipTeams(id: number): Observable<Team[]> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('championship', '' + id);

    return this.http
      .get(this.url, {headers: this.headers, search: params})
      .map(response => response.json() as Team[]);
  }
}

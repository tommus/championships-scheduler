import {Injectable} from "@angular/core";
import {Headers, Http, URLSearchParams} from "@angular/http";
import {ProfileService} from "./profile.service";
import {Observable} from "rxjs";
import {Participate} from "../model/participate";

@Injectable()
export class ParticipatesService {
  private url: string = 'http://localhost:8000/api/championships/participates/';
  private headers = new Headers();

  constructor(private http: Http, profileService: ProfileService) {
    this.headers.append('Authorization', profileService.getAuthToken());
  }

  getParticipates(): Observable<Participate[]> {
    return this.http
      .get(this.url, {headers: this.headers})
      .map(response => response.json() as Participate[]);
  }

  getParticipateById(id: number): Observable<Participate> {
    return this.http
      .get(this.url + id + '/', {headers: this.headers})
      .map(response => response.json() as Participate);
  }

  getChampionshipParticipates(id: number): Observable<Participate[]> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('championship', '' + id);

    return this.http
      .get(this.url, {headers: this.headers, search: params})
      .map(response => response.json() as Participate[]);
  }
}

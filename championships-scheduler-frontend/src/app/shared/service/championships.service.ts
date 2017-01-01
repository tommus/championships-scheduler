import {Injectable} from "@angular/core";
import {Http, Headers} from "@angular/http";
import {Observable} from "rxjs";
import {Championship} from "../model/championship";
import {ProfileService} from "./profile.service";

@Injectable()
export class ChampionshipsService {
  private url: string = 'http://localhost:8000/api/championships/championships/';
  private scheduleUrl: string = 'http://localhost:8000/api/championships/schedule/';
  private headers = new Headers();

  constructor(private http: Http, profileService: ProfileService) {
    this.headers.append('Authorization', profileService.getAuthToken());
  }

  getChampionshipById(id: number): Observable<Championship> {
    return this.http
      .get(this.url + id + '/', {headers: this.headers})
      .map(response => response.json() as Championship);
  }

  getChampionships(): Observable<Championship[]> {
    return this.http
      .get(this.url, {headers: this.headers})
      .map(response => response.json() as Championship[]);
  }

  getChampionshipsCount(): Observable<number> {
    return this.getChampionships()
      .map(championships => championships.length);
  }

  scheduleChampionship(data): Observable<Championship> {
    return this.http
      .post(this.scheduleUrl, data, {headers: this.headers})
      .map(response => response.json() as Championship);
  }
}

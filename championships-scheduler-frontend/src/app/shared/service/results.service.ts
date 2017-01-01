import {Injectable} from "@angular/core";
import {Headers, Http, URLSearchParams} from "@angular/http";
import {ProfileService} from "./profile.service";
import {Observable} from "rxjs";
import {Result} from "../model/result";

@Injectable()
export class ResultsService {
  private url: string = 'http://192.168.1.102:8000/api/championships/results/';
  private headers = new Headers();

  constructor(private http: Http, profileService: ProfileService) {
    this.headers.append('Authorization', profileService.getAuthToken());
  }

  getResults(): Observable<Result[]> {
    return this.http
      .get(this.url, {headers: this.headers})
      .map(response => response.json() as Result[]);
  }

  getChampionshipResults(id: number): Observable<Result[]> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('championship', '' + id);

    return this.http
      .get(this.url, {headers: this.headers, search: params})
      .map(response => response.json() as Result[]);
  }
}

import {Injectable} from "@angular/core";
import {Headers, Http, URLSearchParams} from "@angular/http";
import {ProfileService} from "./profile.service";
import {Observable} from "rxjs";
import {Match} from "../model/match";

@Injectable()
export class MatchesService {
  private url: string = 'http://192.168.1.102:8000/api/championships/matches/';
  private headers = new Headers();

  constructor(private http: Http, profileService: ProfileService) {
    this.headers.append('Authorization', profileService.getAuthToken());
  }

  getMatches(): Observable<Match[]> {
    return this.http
      .get(this.url, {headers: this.headers})
      .map(response => response.json() as Match[]);
  }

  getChampionshipMatches(id: number): Observable<Match[]> {
    let params: URLSearchParams = new URLSearchParams();
    params.set('championship', '' + id);

    return this.http
      .get(this.url, {headers: this.headers, search: params})
      .map(response => response.json() as Match[]);
  }

  submitMatchResult(match: Match, data: any): Observable<Match> {
    return this.http
      .patch(this.url + match.id + '/', data, {headers: this.headers})
      .map(response => response.json() as Match);
  }
}

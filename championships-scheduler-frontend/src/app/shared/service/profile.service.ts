import {Injectable} from "@angular/core";

@Injectable()
export class ProfileService {
  private authToken: string = 'auth_token';

  getAuthToken(): string {
    return localStorage.getItem(this.authToken);
  }

  setAuthToken(token: string): void {
    localStorage.setItem(this.authToken, token);
  }

  removeAuthToken(): void {
    localStorage.removeItem(this.authToken);
  }
}

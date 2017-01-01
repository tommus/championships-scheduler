import {Component, OnDestroy} from "@angular/core";
import {Router} from "@angular/router";
import {Subscription} from "rxjs";
import {LoginService} from "../service/login.service";

@Component({
  selector: 'top-navigation',
  templateUrl: './top-navigation.component.html',
  styleUrls: ['./top-navigation.component.scss']
})
export class TopNavigationComponent implements OnDestroy {
  private subscription: Subscription;

  constructor(private router: Router, private loginService: LoginService) {
  }

  ngOnDestroy(): void {
    if (this.subscription != null && !this.subscription.closed) {
      this.subscription.unsubscribe();
    }
  }

  logout(): void {
    this.subscription = this.loginService
      .logout()
      .subscribe(
        () => this.router.navigate(['']),
        error => console.error(error)
      );
  }
}

import {Component, Input, OnInit, OnDestroy} from "@angular/core";
import {Router} from "@angular/router";
import {Subscription} from "rxjs";
import {LoginService} from "../shared/service/login.service";
import {ProfileService} from "../shared/service/profile.service";

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit, OnDestroy {
  @Input() username: string;
  @Input() password: string;
  private errors: string[] = [];
  private subscription: Subscription;

  constructor(private router: Router,
              private loginService: LoginService,
              private profileService: ProfileService) {
  }

  ngOnInit(): void {
    if (this.profileService.getAuthToken() != null) {
      this.router.navigate(['dashboard']);
    }
  }

  ngOnDestroy(): void {
    if (this.subscription != null && !this.subscription.closed) {
      this.subscription.unsubscribe();
    }
  }

  onSubmit(): void {
    this.subscription = this.loginService
      .login(this.username, this.password)
      .subscribe(response => {
        this.router.navigate(['dashboard']);
      }, error => {
        this.errors = error.json();
      });
  }
}

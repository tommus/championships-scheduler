import {Component, OnInit, OnDestroy, Input} from "@angular/core";
import {AccountsService} from "../../shared/service/accounts.service";
import {TeamsService} from "../../shared/service/teams.service";
import {ChampionshipsService} from "../../shared/service/championships.service";
import {Subscription} from "rxjs";
import {Router} from "@angular/router";

@Component({
  selector: 'app-create',
  templateUrl: './create.component.html',
  styleUrls: ['./create.component.scss']
})
export class CreateComponent implements OnInit, OnDestroy {
  private groupOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
  private players = [];
  private teams = [];
  private subscription: Subscription = new Subscription();

  @Input() request;

  constructor(private router: Router,
              private championshipsService: ChampionshipsService,
              private accountsService: AccountsService,
              private teamsService: TeamsService) {
    this.resetRequest();
  }

  ngOnInit(): void {
    this.subscription.add(
      this.accountsService.getUsers()
        .subscribe(users => this.players = users));

    this.subscription.add(
      this.teamsService.getTeams()
        .subscribe(teams => this.teams = teams));
  }

  ngOnDestroy(): void {
    if (this.subscription != null && !this.subscription.closed) {
      this.subscription.unsubscribe();
    }
  }

  onSubmit(): void {
    this.subscription.add(this.championshipsService.scheduleChampionship(this.request)
      .subscribe(
        championship => this.router.navigate(['/championships', 'details', championship.id]),
        error => console.error(error)
      ));
  }

  onReset(): void {
    this.resetRequest();
  }

  private resetRequest(): void {
    this.request = {
      'name': '',
      'groups': 1,
      'players': [],
      'teams': [],
      'home_away': true
    }
  }
}

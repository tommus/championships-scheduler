import {Component, OnDestroy} from "@angular/core";
import {TeamsService} from "../../../shared/service/teams.service";
import {AccountsService} from "../../../shared/service/accounts.service";
import {ParticipatesService} from "../../../shared/service/participates.service";
import {Observable, Subscription} from "rxjs";
import {Match} from "../../../shared/model/match";
import {User} from "../../../shared/model/user";
import {Team} from "../../../shared/model/team";
import {MatchesService} from "../../../shared/service/matches.service";

@Component({
  selector: 'match-modal',
  templateUrl: './match-modal.component.html',
  styleUrls: ['./match-modal.component.scss']
})
export class MatchModalComponent implements OnDestroy {
  match: Match;
  hostPlayer: User;
  hostTeam: Team;
  guestPlayer: User;
  guestTeam: Team;
  visible = false;
  visibleAnimate = false;
  private parentCallback: any;
  private subscription: Subscription = new Subscription();

  constructor(private matchesService: MatchesService,
              private participatesService: ParticipatesService,
              private teamsService: TeamsService,
              private accountsService: AccountsService) {
  }

  ngOnDestroy(): void {
    if (this.subscription != null && !this.subscription.closed) {
      this.subscription.unsubscribe();
    }
  }

  setMatch(match: Match): void {
    this.match = match;
    this.subscription.add(Observable.forkJoin([
      this.participatesService.getParticipateById(this.match.host_team),
      this.participatesService.getParticipateById(this.match.guest_team)
    ]).flatMap(([hostParticipate, guestParticipate]) => {
      let hostTeam = this.teamsService.getTeamById(hostParticipate.team);
      let guestTeam = this.teamsService.getTeamById(guestParticipate.team);
      let hostPlayer = this.accountsService.getUserById(hostParticipate.player);
      let guestPlayer = this.accountsService.getUserById(guestParticipate.player);
      return Observable.forkJoin([hostTeam, guestTeam, hostPlayer, guestPlayer]);
    }).subscribe(([hostTeam, guestTeam, hostPlayer, guestPlayer]) => {
      this.hostTeam = hostTeam;
      this.guestTeam = guestTeam;
      this.hostPlayer = hostPlayer;
      this.guestPlayer = guestPlayer;
    }));
  }

  show(): void {
    this.visible = true;
    setTimeout(() => this.visibleAnimate = true, 100);
    this.setBodyScrolling(false);
  }

  hide(): void {
    this.visible = false;
    setTimeout(() => this.visibleAnimate = false, 300);
    this.setBodyScrolling(true);
  }

  setBodyScrolling(flag: boolean): void {
    let body = document.getElementsByTagName('body')[0];

    if (flag) {
      body.classList.remove('modal-open');
    } else {
      body.classList.add('modal-open')
    }
  }

  submit(): void {
    this.subscription.add(this.matchesService.submitMatchResult(this.match, {
      host_team_goals: this.match.host_team_goals,
      guest_team_goals: this.match.guest_team_goals
    }).subscribe(match => {
      this.hide();

      // TODO: Reload parent data.
    }));
  }
}

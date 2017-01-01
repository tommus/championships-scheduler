import {Component, OnInit, OnDestroy, ViewChild} from "@angular/core";
import {ActivatedRoute} from "@angular/router";
import {Subscription, Observable} from "rxjs";
import {ChampionshipsService} from "../../shared/service/championships.service";
import {TeamsService} from "../../shared/service/teams.service";
import {AccountsService} from "../../shared/service/accounts.service";
import {ParticipatesService} from "../../shared/service/participates.service";
import {GroupsService} from "../../shared/service/groups.service";
import {MatchesService} from "../../shared/service/matches.service";
import {ResultsService} from "../../shared/service/results.service";
import {Group} from "../../shared/model/group";
import {Result} from "../../shared/model/result";
import {Match} from "../../shared/model/match";
import {MatchModalComponent} from "./match-modal/match-modal.component";

// TODO: Refactor team score widget as separate component.

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss']
})
export class DetailsComponent implements OnInit, OnDestroy {
  @ViewChild(MatchModalComponent) modal: MatchModalComponent;
  private subscription: Subscription = new Subscription();
  private championships;
  private groups = [];
  private results = [];
  private matches = [];
  private participates = [];
  private teams = [];
  private players = [];

  constructor(private championshipsService: ChampionshipsService,
              private groupsService: GroupsService,
              private resultsService: ResultsService,
              private matchesService: MatchesService,
              private participatesService: ParticipatesService,
              private teamsService: TeamsService,
              private accountService: AccountsService,
              private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.subscription.add(
      this.route.params
        .flatMap(params => {
          let championship = this.championshipsService.getChampionshipById(+params['id']);
          let groups = this.groupsService.getChampionshipGroups(+params['id']);
          let results = this.resultsService.getChampionshipResults(+params['id']);
          let matches = this.matchesService.getChampionshipMatches(+params['id']);
          let participates = this.participatesService.getChampionshipParticipates(+params['id']);
          let teams = this.teamsService.getChampionshipTeams(+params['id']);
          let players = this.accountService.getChampionshipUsers(+params['id']);
          return Observable.forkJoin([championship, groups, results, matches, participates, teams, players]);
        })
        .subscribe(([championship, groups, results, matches, participates, teams, players]) => {
          this.championships = championship;
          this.groups = groups;
          this.results = results;
          this.matches = matches;
          this.participates = participates;
          this.teams = teams;
          this.players = players;

          this.sortGroupParticipatesByResults(this.groups, this.results);
        }));
  }

  ngOnDestroy(): void {
    if (this.subscription != null && !this.subscription.closed) {
      this.subscription.unsubscribe();
    }
  }

  private sortGroupParticipatesByResults(groups: Group[], results: Result[]): void {
    groups.forEach(group => group.participates = this.sortByResults(group.participates, results));
  }

  private sortByResults(participates: number[], results: Result[]): number[] {
    return participates.sort((a, b) => {
      let aResults = this.getById(results, a).results;
      let bResults = this.getById(results, b).results;

      if (aResults['points'] === bResults['points']) {
        if (aResults['goals_balance'] === bResults['goals_balance']) {
          return bResults['games_played'] - aResults['games_played'];
        }
        return bResults['goals_balance'] - aResults['goals_balance'];
      }
      return bResults.points - aResults.points;
    })
  }

  getById(collection: any[], id: number): any {
    return collection.filter(item => item.id === id)[0];
  }

  getCardStyle(match, home) {
    if (match.host_team_goals === null || match.guest_team_goals === null) {
      return 'card';
    }
    if (match.host_team_goals > match.guest_team_goals) {
      return home ? 'card card-success' : 'card card-danger';
    }
    if (match.host_team_goals < match.guest_team_goals) {
      return home ? 'card card-danger' : 'card card-success';
    }
    return 'card card-info';
  }

  sanitizeScore(score) {
    if (score === null || score === null) {
      return '-';
    }
    return score;
  }

  showSetScore(match: Match): void {
    this.modal.setMatch(match);
    this.modal.show();
  }
}

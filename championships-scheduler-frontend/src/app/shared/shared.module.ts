import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import {TopNavigationComponent} from "./top-navigation/top-navigation.component";
import {SideNavigationComponent} from "./side-navigation/side-navigation.component";
import {RouterModule} from "@angular/router";
import {DropdownModule, DropdownConfig} from "ng2-bootstrap";
import {ProfileService} from "./service/profile.service";
import {LoginService} from "./service/login.service";
import {ChampionshipsService} from "./service/championships.service";
import {AccountsService} from "./service/accounts.service";
import {TeamsService} from "./service/teams.service";
import {ParticipatesService} from "./service/participates.service";
import {MatchesService} from "./service/matches.service";
import {GroupsService} from "./service/groups.service";
import {ResultsService} from "./service/results.service";

@NgModule({
  declarations: [
    TopNavigationComponent,
    SideNavigationComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    DropdownModule,
  ],
  exports: [
    TopNavigationComponent,
    SideNavigationComponent
  ],
  providers: [
    DropdownConfig,
    AccountsService,
    TeamsService,
    ParticipatesService,
    ProfileService,
    LoginService,
    ChampionshipsService,
    MatchesService,
    GroupsService,
    ResultsService
  ]
})
export class SharedModule {
}

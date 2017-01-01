import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import {ChampionshipsComponent} from "./championships.component";
import {SharedModule} from "../shared/shared.module";
import {RouterModule} from "@angular/router";
import {HomeComponent} from "./home/home.component";
import {FormsModule} from "@angular/forms";
import {NamePipe} from "./home/name.pipe";
import { CreateComponent } from './create/create.component';
import { DetailsComponent } from './details/details.component';
import {MatchModalComponent} from "./details/match-modal/match-modal.component";

@NgModule({
  declarations: [
    ChampionshipsComponent,
    HomeComponent,
    NamePipe,
    CreateComponent,
    DetailsComponent,
    MatchModalComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    SharedModule
  ],
  exports: [
    ChampionshipsComponent
  ]
})
export class ChampionshipsModule {
}

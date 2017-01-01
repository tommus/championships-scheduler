import {NgModule} from "@angular/core";
import {CommonModule} from "@angular/common";
import {DashboardComponent} from "./dashboard.component";
import {SharedModule} from "../shared/shared.module";
import {RouterModule} from "@angular/router";
import { HomeComponent } from './home/home.component';
import {ChampionshipsWidgetComponent} from "./home/championships-widget/championships-widget.component";

@NgModule({
  declarations: [
    DashboardComponent,
    HomeComponent,
    ChampionshipsWidgetComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    SharedModule
  ],
  exports: [
    DashboardComponent
  ]
})
export class DashboardModule {
}

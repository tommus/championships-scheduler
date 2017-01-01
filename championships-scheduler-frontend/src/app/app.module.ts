import {BrowserModule} from "@angular/platform-browser";
import {NgModule} from "@angular/core";
import {RouterModule} from "@angular/router";
import {routes} from "./app.routes";
import {AppComponent} from "./app.component";
import {LoginModule} from "./login/login.module";
import {DashboardModule} from "./dashboard/dashboard.module";
import {ChampionshipsModule} from "./championships/championships.module";

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes),
    LoginModule,
    DashboardModule,
    ChampionshipsModule
  ],
  exports: [
    RouterModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}

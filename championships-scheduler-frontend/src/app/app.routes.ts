import {Routes} from "@angular/router";
import {LoginRoutes} from "./login/login.routes";
import {DashboardRoutes} from "./dashboard/dashboard.routes";
import {ChampionshipRoutes} from "./championships/dashboard.routes";

export const routes: Routes = [
  ...LoginRoutes,
  ...DashboardRoutes,
  ...ChampionshipRoutes,
  {path: '**', redirectTo: 'login'}
];

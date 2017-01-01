import {Route} from "@angular/router";
import {ChampionshipsComponent} from "./championships.component";
import {HomeRoutes} from "./home/home.routes";
import {CreateRoutes} from "./create/create.routes";
import {DetailsRoutes} from "./details/details.routes";

export const ChampionshipRoutes: Route[] = [
  {
    path: 'championships',
    component: ChampionshipsComponent,
    children: [
      ...HomeRoutes,
      ...CreateRoutes,
      ...DetailsRoutes
    ]
  }
];

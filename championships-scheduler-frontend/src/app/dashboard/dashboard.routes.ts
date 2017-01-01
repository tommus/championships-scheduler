import {Route} from "@angular/router";
import {DashboardComponent} from "./dashboard.component";
import {HomeRoutes} from "./home/home.routes";

export const DashboardRoutes: Route[] = [
  {
    path: 'dashboard',
    component: DashboardComponent,
    children: [
      ...HomeRoutes
    ]
  },
];

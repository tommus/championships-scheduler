import {Route} from "@angular/router";
import {DetailsComponent} from "./details.component";

export const DetailsRoutes: Route[] = [
  {
    path: 'details/:id',
    component: DetailsComponent
  }
];

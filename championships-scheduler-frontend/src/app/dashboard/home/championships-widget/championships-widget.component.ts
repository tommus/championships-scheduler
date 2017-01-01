import {Component, OnInit, OnDestroy} from "@angular/core";
import {ChampionshipsService} from "../../../shared/service/championships.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'championships-widget',
  templateUrl: './championships-widget.component.html',
  styleUrls: ['./championships-widget.component.scss']
})
export class ChampionshipsWidgetComponent implements OnInit, OnDestroy {
  private subscription: Subscription;
  count: number;

  constructor(private championshipsService: ChampionshipsService) {
  }

  ngOnInit(): void {
    this.subscription = this.championshipsService
      .getChampionshipsCount()
      .subscribe(
        count => this.count = count,
        error => console.log(error)
      );
  }

  ngOnDestroy(): void {
    if (this.subscription != null && this.subscription.closed) {
      this.subscription.unsubscribe();
    }
  }
}

import {Component, OnInit, OnDestroy} from "@angular/core";
import {ChampionshipsService} from "../../shared/service/championships.service";
import {Championship} from "../../shared/model/championship";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {
  private championships: Championship[] = [];
  private subscription: Subscription;
  private showCountOptions: number[] = [5, 10, 25, 50];
  private showCount: number = this.showCountOptions[0];
  private filterName: string = '';

  constructor(private championshipsService: ChampionshipsService) {
  }

  ngOnInit(): void {
    this.subscription = this.championshipsService.getChampionships()
      .subscribe(championships => this.championships = championships);
  }

  ngOnDestroy(): void {
    if (this.subscription != null && !this.subscription.closed) {
      this.subscription.unsubscribe();
    }
  }
}

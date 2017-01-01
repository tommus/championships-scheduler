export class Result {
  id: number;
  championship: number;
  player: string;
  results: {
    games_drawn: number;
    games_lost: number;
    games_played: number;
    games_won: number;
    goals_balance: number;
    goals_lost: number;
    goals_scored: number;
    points: number;
  };
  team: string;
}

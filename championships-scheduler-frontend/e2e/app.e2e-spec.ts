import { ChampionshipsSchedulerFrontendPage } from './app.po';

describe('championships-scheduler-frontend App', function() {
  let page: ChampionshipsSchedulerFrontendPage;

  beforeEach(() => {
    page = new ChampionshipsSchedulerFrontendPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});

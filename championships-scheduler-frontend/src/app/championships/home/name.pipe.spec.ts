/* tslint:disable:no-unused-variable */
import {NamePipe} from "./name.pipe";
import {Championship} from "../../shared/model/championship";

describe('NamePipe', () => {
  let championships: Championship[] = [];

  beforeAll(() => {
    let one = new Championship();
    one.name = 'Bundesliga';
    championships.push(one);

    let two = new Championship();
    two.name = 'La Liga';
    championships.push(two);
  });

  it('should create an instance', () => {
    let pipe = new NamePipe();
    expect(pipe).toBeTruthy();
  });

  it('should result with an unchanged array for empty filter', () => {
    let pipe = new NamePipe();
    let result = pipe.transform(championships, '');

    expect(result).toEqual(championships);
  });

  it('should filter out not matching championships', () => {
    let pipe = new NamePipe();
    let result = pipe.transform(championships, 'Bundesliga');

    expect(result.length).toEqual(1);
    expect(result).not.toEqual(championships);
  });

  it('should result with an empty array for not matching filter', () => {
    let pipe = new NamePipe();
    let result = pipe.transform(championships, 'Premier League');

    expect(result.length).toEqual(0);
  });
});

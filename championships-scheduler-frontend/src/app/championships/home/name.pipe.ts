import {Pipe, PipeTransform} from "@angular/core";
import {Championship} from "../../shared/model/championship";

@Pipe({
  name: 'name'
})
export class NamePipe implements PipeTransform {
  transform(championships: Championship[], name: string): Championship[] {
    if (name == null || name.trim().length <= 0) {
      return championships;
    }
    return championships.filter(championships => championships.name.toLowerCase().includes(name.toLowerCase().trim()));
  }
}

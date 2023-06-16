import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class GetidService {

  private id: any;

  setId(id: any) {
    this.id = id;
  }

  getId(): any {
    return this.id;
  }


  constructor() { }
}

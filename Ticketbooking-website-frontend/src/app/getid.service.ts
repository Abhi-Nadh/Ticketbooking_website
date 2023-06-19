import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GetidService {
  private id: any;
  private vid: any;
  private vidSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

  setId(id: any) {
    this.id = id;
  }

  getId(): any {
    return this.id;
  }

  setIv(vid: any) {
    this.vid = vid;
    this.vidSubject.next(vid);
  }

  getIv(): any {
    return this.vidSubject.asObservable();
  }


  constructor() { }
}

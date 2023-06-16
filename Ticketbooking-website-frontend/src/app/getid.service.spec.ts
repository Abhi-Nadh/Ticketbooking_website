import { TestBed } from '@angular/core/testing';

import { GetidService } from './getid.service';

describe('GetidService', () => {
  let service: GetidService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GetidService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

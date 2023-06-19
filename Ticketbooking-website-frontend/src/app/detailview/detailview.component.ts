import { Component, OnInit } from '@angular/core';
import { UserOperationsService } from '../user-operations.service';
import { ActivatedRoute, Router } from '@angular/router';
import { GetidService } from '../getid.service'
declare var $: any;
declare var Razorpay: any;

interface seatForm {
  seat: string;
  language: string;
  price: number;
  count: number;
}

@Component({
  selector: 'app-detailview',
  templateUrl: './detailview.component.html',
  styleUrls: ['./detailview.component.css']
})
export class DetailviewComponent implements OnInit {
  data: any;
  id: any;
  vid:any;
  seatForm: seatForm = {
    seat: '',
    language:'',
    price: 0,
    count: 0
  };

  constructor(
    private userop: UserOperationsService,
    private router: Router,
    private route: ActivatedRoute,
    private idshare:GetidService
  ) {}

  ngOnInit(): void {
    const token = localStorage.getItem('token');
    if (token == null) {
      this.router.navigate(['/login']);
    } else {
      this.moviedetail();
    }
  }

  moviedetail(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    console.log(this.id)
    this.idshare.setId(this.id)
    this.userop.detailmovie(this.id).subscribe(response => {
      this.data = response;
      console.log(this.data);
    });
  }

  openModal(): void {
    $('#myModal').modal('show');
  }

  closeModal(): void {
    $('#myModal').modal('hide');
  }

  updatePrice(): void {
    const seat = this.seatForm.seat;
    if (seat === 'diamond') {
      this.seatForm.price = 300.0;
    } else if (seat === 'gold') {
      this.seatForm.price = 180.0;
    } else if (seat === 'silver') {
      this.seatForm.price = 120.0;
    }
  }

  booking(): void {
    this.id = this.route.snapshot.paramMap.get('id');
    this.userop.bookingmovie(this.seatForm, this.id).subscribe(response => {
      this.vid = response;
      console.log(this.vid);
      this.idshare.setIv(this.vid);
    });
    this.router.navigate(['booking']);
    this.closeModal();
  }
}


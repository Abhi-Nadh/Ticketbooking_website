import { Component, OnInit } from '@angular/core';
import { UserOperationsService } from '../user-operations.service';
import { ActivatedRoute, Router } from '@angular/router';
declare var $: any;


interface seatForm {
  seat: string;
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
  id:any;
  seatForm: seatForm = {
    seat: '',
    price: 0,
    count: 0
  };


  constructor(private userop:UserOperationsService , private router:Router, private route: ActivatedRoute,) { }

  ngOnInit(): void {
    const token=localStorage.getItem('token')
    if (token==null)
    {
      this.router.navigate(['/login'])
    }
    else{
    this.moviedetail()
    }
  }

  moviedetail(){
    this.id = this.route.snapshot.paramMap.get('id')
    this.userop.detailmovie(this.id).subscribe(response => {
      this.data=response
      console.log(this.data)
        });
      }

      openModal() {
        $('#myModal').modal('show');
      }
    
      closeModal() {
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
    

      booking(){
        this.id = this.route.snapshot.paramMap.get('id')
        this.userop.bookingmovie(this.seatForm,this.id).subscribe(response => {

          console.log(response)
            });
            }
}
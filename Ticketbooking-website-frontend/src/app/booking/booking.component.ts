import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { UserOperationsService } from '../user-operations.service';
import { GetidService } from '../getid.service'
declare var Razorpay: any;


@Component({
  selector: 'app-booking',
  templateUrl: './booking.component.html',
  styleUrls: ['./booking.component.css']
})
export class BookingComponent implements OnInit {

  options: any;
  id: any;
  bookeddata: any = {};
  orderform={
    customer_details:"",
    order_id:"",
    payment_id:"",
    payment_signature:""

  }
  data_id: any;
  vid: any;



  constructor(
    private userop: UserOperationsService,
    private router: Router,
    private route: ActivatedRoute,
    private idshare:GetidService

  ) { }

  ngOnInit(): void {
    this.idshare.getIv().subscribe(vid => {
      if (vid) {
        this.vid = vid;
        const token = localStorage.getItem('token');
        this.userop.display_book_model(this.vid, token).subscribe(response => {
          this.bookeddata=response
          console.log(response);
        });
      }
    });
  }




  payment_meth(){
    const com_instance=this
    this.id=this.idshare.getId()
    this.userop.user_bookin_details(this.id).subscribe(response => {
      console.log(response);
      const orderid = response.order.id;
      this.data_id = response.data_id;
      const convertedAmount = response.amount * 100;

      this.options = {
        key: 'rzp_test_DCDK7quKT85NaG',
        amount: convertedAmount.toString(),
        name: response.name,
        description: 'Web Development',
        order_id: orderid,
        handler: function (response) {
          const data=response
          var event = new CustomEvent('payment.success', {
            detail: response,
            bubbles: true,
            cancelable: true
          });
          window.dispatchEvent(event);    
          com_instance.orderform.order_id=data.razorpay_order_id
          com_instance.orderform.payment_id=data.razorpay_payment_id
          com_instance.orderform.payment_signature=data.razorpay_signature
          com_instance.orderform.customer_details=com_instance.data_id

          com_instance.userop.razorResponse(com_instance.orderform).subscribe(response => {
            console.log(response)
          })



        },
        prefill: {
          name: '',
          email: '',
          contact: ''
        },
        notes: {
          address: ''
        },
        theme: {
          color: '#3399cc'
        }
      };

      const rzp = new Razorpay(this.options);
      rzp.open();

      this.endfun()
    });
  

  }

  endfun(){
    this.router.navigate(['detailview/'+this.id])
  }



}

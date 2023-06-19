import { Component, OnInit } from '@angular/core';
import {UserOperationsService} from '../user-operations.service'
import { Router } from '@angular/router';
import { DomSanitizer } from '@angular/platform-browser';


@Component({
  selector: 'app-mybooking',
  templateUrl: './mybooking.component.html',
  styleUrls: ['./mybooking.component.css']
})
export class MybookingComponent implements OnInit {

  data:any
  pdfUrl: any;

  constructor(private userop:UserOperationsService, private router:Router,private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
    this.usermovielist()
  }

  usermovielist(){
    const token=localStorage.getItem('token')
    this.userop.userlistmovies().subscribe(response => {
      this.data=response
      console.log(this.data)
        });

      }

      printpdf(): void {

        const token = localStorage.getItem('token');
        
        this.userop.getpdf(token).subscribe((response: Blob) => {
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(response);
            link.download = 'movie_ticket.pdf';
            link.click();
            
           
            URL.revokeObjectURL(link.href);
            
          },
          (error) => {
            console.log('Error downloading PDF:', error);
          }
        );
      }
      



    }

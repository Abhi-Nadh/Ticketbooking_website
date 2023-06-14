import { Component, OnInit } from '@angular/core';
import {UserOperationsService} from '../user-operations.service'
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  data: any;

  constructor(private userop:UserOperationsService, private router:Router) { }

  ngOnInit(): void {
    const token=localStorage.getItem('token')
    if (token==null){
      this.router.navigate(['/login'])

    }
    else{
      this.movielist()
    }
  }

  movielist(){
    const token=localStorage.getItem('token')
    this.userop.listmovies().subscribe(response => {
      this.data=response
        });

      }

}

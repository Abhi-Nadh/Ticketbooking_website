import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor(private authservice:AuthService, private router:Router) { }

  ngOnInit(): void {
  }

  Onlogout(){
    this.authservice.logout().subscribe(response => {
      localStorage.removeItem('token')
      console.log(response)
      this.router.navigate(['/login']);
    });
  }

}

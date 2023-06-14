import { Component, OnInit } from '@angular/core';
import { AuthService } from '../auth.service';
import { Route, Router } from '@angular/router';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginData = {
    username: '',
    password: ''
  };
  constructor(private authservice:AuthService, private router:Router) { }

  ngOnInit(): void {
  }

  onLogin(){
    this.authservice.login(this.loginData).subscribe(response => {
      // const token = response.token;
      localStorage.setItem('token', response.token);
      const token=localStorage.getItem('token')
      this.router.navigate(['']);
    });
  }
}

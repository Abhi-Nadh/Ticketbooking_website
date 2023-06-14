import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  signupData = {
    username: '',
    email:'',
    password: '',
    conf_password:''
  };

message:any
  constructor(private authservice:AuthService, private router:Router) { }

  ngOnInit(): void {
  }

  onSignup(){
      this.authservice.signup(this.signupData).subscribe(response => {
        this.router.navigate(['/login']);
      },
      );  
  }

}

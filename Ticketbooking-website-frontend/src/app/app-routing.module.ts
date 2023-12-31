import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { HomeComponent } from './home/home.component';
import { DetailviewComponent } from './detailview/detailview.component';
import { BookingComponent } from './booking/booking.component';
import { MybookingComponent } from './mybooking/mybooking.component';


const routes: Routes = [
  {path:'',component:HomeComponent},
  {path:'login',component:LoginComponent},
  {path:'signup',component:SignupComponent},
  {path:'detailview/:id',component:DetailviewComponent},
  {path:'booking',component:BookingComponent},
  {path:'mybooking',component:MybookingComponent},




];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

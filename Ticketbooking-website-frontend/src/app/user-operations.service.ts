import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserOperationsService {

  private apiUrl="http://127.0.0.1:8000/Ticketbookapi"

  constructor(private http:HttpClient ,private route:ActivatedRoute) { }


  token=localStorage.getItem('token')

  listmovies():Observable <any>{
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `token ${this.token}`
      })
    };      
    return this.http.get<any>(`${this.apiUrl}/movielist`,httpOptions)
  }


  bookingmovie(data: any,id:any){
    
    const token=localStorage.getItem('token')
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `token ${token}`
      })
    };    
    console.log(id)  
    return this.http.post<any>(`${this.apiUrl}/bookingmovie/${id}`,data,httpOptions)
  }


  bookedmoviedetails(data: any,id:any){
    const token=localStorage.getItem('token')
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `token ${token}`
      })};    
    console.log(id)  
    return this.http.post<any>(`${this.apiUrl}/bookingmovie/${id}`,data,httpOptions)
  }

  user_bookin_details(id:any){
    const token=localStorage.getItem('token')
    const httpOptions = {

      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `token ${token}`
      })};    
    return this.http.get<any>(`${this.apiUrl}/neworder/${id}`,httpOptions)
  
  }

  detailmovie(id:any):Observable <any>{
    const token=localStorage.getItem('token')
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `token ${token}`
      })
    };      

    return this.http.get<any>(`${this.apiUrl}/moviedetails/${id}`,httpOptions)
  }


  razorResponse(data:any){
    const token=localStorage.getItem('token')
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `token ${token}`
      })
    };      
    console.log(data)

    return this.http.post(`${this.apiUrl}/callback`,data)
  }


}

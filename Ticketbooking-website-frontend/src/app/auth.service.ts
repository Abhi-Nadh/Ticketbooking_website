import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl="http://127.0.0.1:8000/Ticketbookapi"

  constructor(private http:HttpClient ) { }

  signup(data: any):Observable <any>{
    return this.http.post<any>(`${this.apiUrl}/signup`, data);
  }

  login(data:any):Observable <any>{
    return this.http.post<any>(`${this.apiUrl}/login`,data);
  }

  logout():Observable<any>{
    const token=localStorage.getItem('token')
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `token ${token}`
      })
    };

    return this.http.post<any>(`${this.apiUrl}/logout`,{},httpOptions)
  }

}

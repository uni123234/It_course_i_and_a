import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpResponse } from '@angular/common/http';
import { catchError, map, Observable, throwError } from 'rxjs';
import { AuthService } from './auth.service';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private apiUrl = 'http://localhost:8000/api/';
  constructor(private http: HttpClient, private authService: AuthService) {}

  // Method to fetch all courses
  getCourses(): Observable<any> {
    return this.http.get(`${this.apiUrl}course/`);
  }

  // Method to enroll in a course
  enrollInCourse(courseId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}course/enroll/${courseId}/`, {});
  }

  // Method to request email change
  requestEmailChange(newEmail: string): Observable<any> {
    return this.http.post(`${this.apiUrl}edit_email/`, {
      new_email: newEmail,
    });
  }

  // Method to request password change
  requestPasswordChange(data: {
    userId: number;
    newPassword: string;
    token: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}edit_password/`, data);
  }

  // Method to get group chat messages
  getGroupChatMessages(courseId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}group_chat/`, {
      params: { course_id: courseId.toString() },
    });
  }

  // Method to send a group chat message
  sendGroupChatMessage(data: {
    courseId: number;
    userId: number;
    message: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}group_chat/`, data);
  }

  // Method to submit help request
  submitHelpRequest(helpRequestData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}help/`, helpRequestData);
  }

  // Method for user login
  userLogin(credentials: { email: string; password: string }): Observable<any> {
    console.log(credentials);
    return this.http.post(`${this.apiUrl}login/`, credentials, { observe: 'response' }).pipe(
      map((response: HttpResponse<any>) => {
        const body = response.body;
        const token = body?.refresh;
        const email: string = credentials.email;
        console.log("token2 " + token);
        if (token) {
          this.authService.setToken(token)
        }
        return body;
      }),
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'Unknown error!';
    if (error.error instanceof ErrorEvent) {
      // Client-side errors
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side errors
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(errorMessage);
  }

  logout(): void {
    localStorage.removeItem('authToken');
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem('authToken');
  }

  userRegister(credentials: {
    username: string;
    email: string;
    password: string;
  }): Observable<any> {
    console.log(credentials)
    return this.http.post(`${this.apiUrl}register/`, credentials);
  }
}

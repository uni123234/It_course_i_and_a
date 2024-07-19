import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private apiUrl = 'http://localhost:8000/api/';
  constructor(private http: HttpClient) {}

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
  userLogin(credentials: {
    email: string;
    password: string;
  }): Observable<any> {
    console.log(credentials)
    return this.http.post(`${this.apiUrl}login/`, credentials);
  }

  // Method for teacher login
  teacherLogin(credentials: {
    username: string;
    password: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}t_login/`, credentials);
  }

  userRegister(credentials: {
    username: string;
    email: string;
    password: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}register/`, credentials);
  }

  teacherRegister(credentials: {
    username: string;
    email: string;
    password1: string;
    password2: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}register_t/`, credentials);
  }
}

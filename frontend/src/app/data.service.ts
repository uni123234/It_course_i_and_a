import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private apiUrl = '/api/'; // Use /api prefix for the proxy

  constructor(private http: HttpClient) {}

  // Method to fetch all courses
  getCourses(): Observable<any> {
    return this.http.get(`${this.apiUrl}courses/`);
  }

  // Method to enroll in a course
  enrollInCourse(courseId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}courses/enroll/${courseId}/`, {});
  }

  // Method to request email change
  requestEmailChange(newEmail: string): Observable<any> {
    return this.http.post(`${this.apiUrl}edit/email-change/`, {
      new_email: newEmail,
    });
  }

  // Method to request password change
  requestPasswordChange(data: {
    userId: number;
    newPassword: string;
    token: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}edit2/password-change/`, data);
  }

  // Method to get group chat messages
  getGroupChatMessages(courseId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}group_chat/messages/`, {
      params: { course_id: courseId.toString() },
    });
  }

  // Method to send a group chat message
  sendGroupChatMessage(data: {
    courseId: number;
    userId: number;
    message: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}group_chat/messages/`, data);
  }

  // Method to submit help request
  submitHelpRequest(helpRequestData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}help/request-help/`, helpRequestData);
  }

  // Method for user login
  userLogin(credentials: {
    username: string;
    password: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}login_in/login-in/`, credentials);
  }

  // Method for teacher login
  teacherLogin(credentials: {
    username: string;
    password: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}t_login/t-login/`, credentials);
  }

  userRegister(credentials: {
    username: string;
    email: string;
    password1: string;
    password2: string;
  }): Observable<any> {
    return this.http.post(`${this.apiUrl}sign_in/register/`, credentials);
  }

  teacherRegister(credentials: {
    username: string;
    email: string;
    password1: string;
    password2: string;
  }): Observable<any> {
    return this.http.post(
      `${this.apiUrl}teacher_sign_in/register/`,
      credentials
    );
  }
}

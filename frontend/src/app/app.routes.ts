import { RouterModule, Routes } from '@angular/router';
import { EditEmailComponent } from './edit-email/edit-email.component';
import { EditPasswordComponent } from './edit-password/edit-password.component';
import { EditPointComponent } from './edit-point/edit-point.component';
import { GroupChatComponent } from './group-chat/group-chat.component';
import { HelpCHComponent } from './help-c-h/help-c-h.component';
import { HomeComponent } from './home/home.component';
import { LmsForItComponent } from './lms-for-it/lms-for-it.component';
import { LoginComponent } from './login/login.component';
import { ResetEmailComponent } from './reset-email/reset-email.component';
import { ResetPasswordComponent } from './reset-password/reset-password.component';
import { RegisterComponent } from './register/register.component';
import { TeacherChatComponent } from './teacher-chat/teacher-chat.component';
import { TeacherLoginComponent } from './teacher-login/teacher-login.component';
import { TeacherPointAddAndEditComponent } from './teacher-point-add-and-edit/teacher-point-add-and-edit.component';
import { TeacherRegisterInComponent } from './teacher-register/teacher-register.component';
import { CourseComponent } from './course/course.component';
import { NgModule } from '@angular/core';

export const routes: Routes = [
  { path: 'course', component: CourseComponent},
  { path: 'edit_email', component: EditEmailComponent },
  { path: 'edit_password', component: EditPasswordComponent },
  { path: 'edit_point', component: EditPointComponent },
  { path: 'group_chat', component: GroupChatComponent },
  { path: 'help', component: HelpCHComponent },
  { path: 'lms_for_it', component: LmsForItComponent },
  { path: 'login', component: LoginComponent},
  { path: 'reset_email', component: ResetEmailComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'teacher_chat', component: TeacherChatComponent },
  { path: 'teacher_login', component: TeacherLoginComponent },
  { path: 'teacher_point_add_and_edit', component: TeacherPointAddAndEditComponent },
  { path: 'register_t', component: TeacherRegisterInComponent },
  { path: '', component: HomeComponent },
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

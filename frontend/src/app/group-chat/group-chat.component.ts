import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DataService } from '../data.service';

@Component({
  selector: 'app-group-chat',
  templateUrl: './group-chat.component.html',
  styleUrls: ['./group-chat.component.css'],
})
export class GroupChatComponent implements OnInit {
  chatForm: FormGroup;
  messages: any[] = [];
  courseId = 1; // Example course ID

  constructor(private fb: FormBuilder, private dataService: DataService) {
    this.chatForm = this.fb.group({
      message: ['', [Validators.required]],
    });
  }

  ngOnInit(): void {
    this.getMessages();
  }

  getMessages(): void {
    this.dataService.getGroupChatMessages(this.courseId).subscribe(
      (data) => {
        this.messages = data;
      },
      (error) => {
        console.error('Error fetching messages:', error);
      }
    );
  }

  sendMessage(): void {
    if (this.chatForm.valid) {
      const messageData = {
        courseId: this.courseId,
        userId: 1, // Example user ID, replace with actual user ID
        message: this.chatForm.get('message')?.value,
      };
      this.dataService.sendGroupChatMessage(messageData).subscribe(
        (response) => {
          this.chatForm.reset();
          this.getMessages(); // Refresh messages after sending
        },
        (error) => {
          console.error('Error sending message:', error);
        }
      );
    }
  }
}

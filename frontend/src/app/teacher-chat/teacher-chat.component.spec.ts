import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherChatComponent } from './teacher-chat.component';

describe('TeacherChatComponent', () => {
  let component: TeacherChatComponent;
  let fixture: ComponentFixture<TeacherChatComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeacherChatComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TeacherChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

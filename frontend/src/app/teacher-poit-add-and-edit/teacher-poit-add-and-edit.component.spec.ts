import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherPoitAddAndEditComponent } from './teacher-poit-add-and-edit.component';

describe('TeacherPoitAddAndEditComponent', () => {
  let component: TeacherPoitAddAndEditComponent;
  let fixture: ComponentFixture<TeacherPoitAddAndEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeacherPoitAddAndEditComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TeacherPoitAddAndEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherPointAddAndEditComponent } from './teacher-point-add-and-edit.component';

describe('TeacherPointAddAndEditComponent', () => {
  let component: TeacherPointAddAndEditComponent;
  let fixture: ComponentFixture<TeacherPointAddAndEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TeacherPointAddAndEditComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TeacherPointAddAndEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

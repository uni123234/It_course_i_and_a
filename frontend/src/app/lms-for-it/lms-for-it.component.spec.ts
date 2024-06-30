import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LmsForItComponent } from './lms-for-it.component';

describe('LmsForItComponent', () => {
  let component: LmsForItComponent;
  let fixture: ComponentFixture<LmsForItComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LmsForItComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(LmsForItComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

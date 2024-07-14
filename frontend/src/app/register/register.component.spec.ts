import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Register_Component } from './register.component';

describe('Register_Component', () => {
  let component: Register_Component;
  let fixture: ComponentFixture<Register_Component>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Register_Component]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(Register_Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

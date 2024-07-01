import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EnroollComponent } from './enrooll.component';

describe('EnroollComponent', () => {
  let component: EnroollComponent;
  let fixture: ComponentFixture<EnroollComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EnroollComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EnroollComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HelpCHComponent } from './help-c-h.component';

describe('HelpCHComponent', () => {
  let component: HelpCHComponent;
  let fixture: ComponentFixture<HelpCHComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HelpCHComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(HelpCHComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

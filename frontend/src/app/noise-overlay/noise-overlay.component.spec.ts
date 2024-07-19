import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NoiseOverlayComponent } from './noise-overlay.component';

describe('NoiseOverlayComponent', () => {
  let component: NoiseOverlayComponent;
  let fixture: ComponentFixture<NoiseOverlayComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NoiseOverlayComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(NoiseOverlayComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubUserEditComponent } from './sub-user-edit.component';

describe('SubUserEditComponent', () => {
  let component: SubUserEditComponent;
  let fixture: ComponentFixture<SubUserEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SubUserEditComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubUserEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

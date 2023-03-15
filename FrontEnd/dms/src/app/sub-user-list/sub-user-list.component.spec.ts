import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubUserListComponent } from './sub-user-list.component';

describe('SubUserListComponent', () => {
  let component: SubUserListComponent;
  let fixture: ComponentFixture<SubUserListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SubUserListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubUserListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

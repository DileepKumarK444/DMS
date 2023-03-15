import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProjectmoduleComponent } from './projectmodule.component';

describe('ProjectmoduleComponent', () => {
  let component: ProjectmoduleComponent;
  let fixture: ComponentFixture<ProjectmoduleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProjectmoduleComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProjectmoduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

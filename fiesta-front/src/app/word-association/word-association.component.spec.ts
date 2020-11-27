import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WordAssociationComponent } from './word-association.component';

describe('WordAssociationComponent', () => {
  let component: WordAssociationComponent;
  let fixture: ComponentFixture<WordAssociationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WordAssociationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WordAssociationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

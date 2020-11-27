import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-word-association',
  templateUrl: './word-association.component.html',
  styleUrls: ['./word-association.component.scss']
})
export class WordAssociationComponent implements OnInit {

  waiting = false;

  characters: string[] = [];
  lastWords: string[] = [];

  selectedWord: string;
  selectedCharacter: string;

  answers = {};

  constructor(
    public socket: Socket,
    private playerService: PlayerService
  ) {}

  ngOnInit(): void {
    this.getAllCharacters();
    this.getAllLastWords();
  }

  getAllCharacters() {
    this.playerService.getAllCharacters().subscribe((response) => {
      console.log("[info] Got all characters");
      this.characters = response.characters;
    });
  }

  getAllLastWords() {
    this.playerService.getAllLastWords().subscribe((response) => {
      console.log("[info] Got all last words");
      this.lastWords = response["last_words"];
    });
  }

  selectWord(word: string) {
    if (this.selectedWord === word) {
      this.selectedWord= null;
    } else {
      this.selectedWord = word;
      this.associate();
    }
  }

  selectCharacter(character: string) {
    if (this.selectedCharacter === character) {
      this.selectedCharacter= null;
    } else {
      this.selectedCharacter = character;
      this.associate();
    }
  }

  associate() {
    if (this.selectedCharacter && this.selectedWord) {
      Object.keys(this.answers).forEach((word) => {
        if (this.answers[word] === this.selectedCharacter) {
          delete this.answers[word];
        }
      });
      this.answers[this.selectedWord] = this.selectedCharacter;
      this.selectedWord = null;
      this.selectedCharacter = null;
    }
  }

  colorFor(character: string) {
    const wordId = this.lastWords.findIndex((word) => this.answers[word] === character);
    return wordId >= 0 ? wordId + 1 : 0;
  }

  allAnswered() {
    return Object.values(this.answers).filter((v) => v != null).length === this.lastWords.length;
  }

  sendAnswers() {
    this.playerService.sendAnswers(this.answers).subscribe((response) => {
      this.waiting = true;
    }, (error) => {
      console.error(error);
    });
  }


}

import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-solution',
  templateUrl: './solution.component.html',
  styleUrls: ['./solution.component.scss']
})
export class SolutionComponent implements OnInit {

  lastWords: string[] = [];

  currentNotebook = null;

  constructor(
    public socket: Socket,
    private playerService: PlayerService
  ) {}

  ngOnInit(): void {
    this.getAllLastWords();

    this.playerService.getNotebookEvent().subscribe((response) => {
      console.log("[info] Got notebook");
      console.log(response);
      const lastWord = response["word_list"][response["word_list"].length - 1];
      this.currentNotebook = {...response, lastWord: lastWord};
    });
  }

  getAllLastWords() {
    this.playerService.getAllLastWords().subscribe((response) => {
      console.log("[info] Got all last words");
      this.lastWords = response["last_words"].sort();
    });
  }

  selectWord(word: string) {
    console.log("[info] Launch notebook " + word);
    this.playerService.getNotebook(word).subscribe((response) => {
      console.log("[info] Launched notebook");
      console.log(response);
    });
  }

  displayNotebook(notebook) {

  }

  getCorrections() {
    return Object.keys(this.currentNotebook.corrections).map((name) => {
      return {
        name,
        correct: this.currentNotebook.corrections[name]
      };
    })
  }

  clearGame() {
    this.playerService.clearGame().subscribe((response) => {
      console.log("[info] Cleared game");
    });
  }

}

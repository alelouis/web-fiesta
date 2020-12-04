import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.scss']
})
export class GameComponent implements OnInit {

  constructor(
    public socket: Socket,
    private playerService: PlayerService
  ) {}

  game: any;
  word: string;
  waiting = true;

  cardFlipped = false;

  rotationCompleted = true;
  allAnswersSubmitted = false;

  gameStage = 'WORDS';

  sendMessage() {
    
  }

  ngOnInit(): void {
    this.getWord();

    this.playerService.getAllWordsSubmitted().subscribe(() => {
      this.getWord();
      console.log("[info] All words submitted");
    }, (error) => {
      console.error(error);
    });

    this.playerService.getAllAnswersSubmitted().subscribe(() => {
      this.gameStage = 'SOLUTION';
      console.log("[info] All answers submitted");
    }, (error) => {
      console.error(error);
    });

    this.playerService.getRotationCompleted().subscribe(() => {
      this.gameStage = 'ASSOCIATION';
      console.log("[info] Rotation completed");
    }, (error) => {
      console.error(error);
    });
  }

  

  getWord() {
    this.playerService.getWord().subscribe((response) => {
      console.log(response);
      this.game = response;
      this.waiting = false;
    }, (error) => {
      console.error(error);
    });
  }

  sendWord() {
    this.playerService.sendWord(this.word).subscribe((response) => {
      console.log(response);
      this.word = '';
      this.waiting = true;
      // this.getWord();
    }, (error) => {
      console.error(error);
    });
  }

}

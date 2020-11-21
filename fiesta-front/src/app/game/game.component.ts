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

  sendMessage() {
    
  }

  ngOnInit(): void {
    this.getWord();

    this.playerService.getAllWordsSubmitted().subscribe(() => {
      this.getWord();
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
      this.waiting = true;
      // this.getWord();
    }, (error) => {
      console.error(error);
    });
  }

}

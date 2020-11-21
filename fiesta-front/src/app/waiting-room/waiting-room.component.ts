import { Component, OnInit } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-waiting-room',
  templateUrl: './waiting-room.component.html',
  styleUrls: ['./waiting-room.component.scss']
})
export class WaitingRoomComponent implements OnInit {

  nickname = '';
  ready: false;

  logged = false;

  players: any[];
  playerMap: any;

  allReady = false;

  constructor(public socket: Socket,
    private playerService: PlayerService) {
  }

  sendMessage() {
    this.playerService.createPlayer(this.nickname).subscribe((response) => {
      console.log(response);
      this.logged = true;
    }, (error) => {
      console.error(error);
    });
  }

  setReady() {
    this.playerService.setReady(this.ready).subscribe((response) => {
      console.log(response);
    }, (error) => {
      console.error(error);
    });
  }

  ngOnInit(): void {
    this.playerService.getPlayers().subscribe((playerMap) => {
      this.playerMap = playerMap;
      this.players = Object.values(playerMap);
      console.log(playerMap);
    }, (error) => {
      console.error(error);
    });

    this.playerService.getAllReady().subscribe(() => {
      this.allReady = true;
    }, (error) => {
      console.error(error);
    });
  }

}

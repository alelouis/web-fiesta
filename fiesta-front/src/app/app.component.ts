import { Component } from '@angular/core';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'fiesta-front';

  constructor(private socket: Socket) {
  }

  sendMessage(){
    this.socket.emit('new_player', {nickname: 'alexis'});
  }
  
}

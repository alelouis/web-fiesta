import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  constructor(private http: HttpClient,
    private socket: Socket) { }

  createPlayer(nickname): Observable<any> {
    return this.http.post(environment.backend + '/create_player', 
      {nickname: nickname, sid: this.socket.ioSocket.id}
    );
  }

  setReady(ready: boolean): Observable<any> {
    return this.http.put(environment.backend + '/set_ready', 
      {ready: ready, sid: this.socket.ioSocket.id}
    );
  }

  getPlayers(): Observable<any> {
    return this.socket.fromEvent('players');
  }

  getAllReady(): Observable<any> {
    return this.socket.fromEvent('all_ready');
  }

}

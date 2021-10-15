import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  constructor(
    private http: HttpClient,
    private socket: Socket) { }

  private room_id = "ejka";

  createRoom(): Observable<any> {
    return this.http.post(environment.backend + '/create_room' , 
      {room_id: this.room_id}
    );
  }

  getWord(): Observable<any> {
    return this.http.post(environment.backend + '/' + this.room_id + '/get_word' , 
      {sid: this.socket.ioSocket.id}
    );
  }

  sendWord(word: string): Observable<any> {
    return this.http.post(environment.backend + '/' + this.room_id + '/send_word', 
      {word: word, sid: this.socket.ioSocket.id}
    );
  }

  sendAnswers(answers): Observable<any> {
    return this.http.post(environment.backend + '/' + this.room_id + '/send_answers', 
      {answers: answers, sid: this.socket.ioSocket.id}
    );
  }

  createPlayer(nickname): Observable<any> {
    return this.http.post(environment.backend + '/' + this.room_id + '/create_player', 
      {nickname: nickname, sid: this.socket.ioSocket.id}
    );
  }

  setReady(ready: boolean): Observable<any> {
    return this.http.put(environment.backend + '/' + this.room_id + '/set_ready', 
      {ready: ready, sid: this.socket.ioSocket.id}
    );
  }

  getNotebook(lastWord: string): Observable<any> {
    return this.http.post(environment.backend + '/' + this.room_id + '/get_notebook', 
      {last_word: lastWord}
    );
  }

  getAllCharacters(): Observable<any> {
    return this.http.get(environment.backend + '/' + this.room_id + '/get_all_characters');
  }

  getAllLastWords(): Observable<any> {
    return this.http.get(environment.backend + '/' + this.room_id + '/get_all_last_words');
  }

  clearGame(): Observable<any> {
    return this.http.get(environment.backend + '/' + this.room_id + '/clear_game');
  }

  getPlayers(): Observable<any> {
    return this.socket.fromEvent('players');
  }

  getAllReady(): Observable<any> {
    return this.socket.fromEvent('all_ready');
  }

  getAllWordsSubmitted(): Observable<any> {
    return this.socket.fromEvent('all_words_submitted');
  }
  
  getAllAnswersSubmitted(): Observable<any> {
    return this.socket.fromEvent('all_answers_submitted');
  }

  getRotationCompleted(): Observable<any> {
    return this.socket.fromEvent('rotation_completed');
  }

  getNotebookEvent(): Observable<any> {
    return this.socket.fromEvent('notebook');
  }

  getGameCleared(): Observable<any> {
    return this.socket.fromEvent('clear_game');
  }

}

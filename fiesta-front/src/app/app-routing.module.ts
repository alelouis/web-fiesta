import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { WaitingRoomComponent } from './waiting-room/waiting-room.component';

const routes: Routes = [
  // { path: 'waiting-room', component: WaitingRoomComponent },
  // { path: '',   redirectTo: '/waiting-room', pathMatch: 'full' },
  { path: '',   component: WaitingRoomComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {})],
  exports: [RouterModule]
})
export class AppRoutingModule { }

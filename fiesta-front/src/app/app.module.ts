import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { WaitingRoomComponent } from './waiting-room/waiting-room.component';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule} from '@angular/material/list';
import { MatCardModule} from '@angular/material/card';
import { MatTabsModule} from '@angular/material/tabs';
import { MatChipsModule} from '@angular/material/chips';
import { MatDividerModule} from '@angular/material/divider';
import { MatMenuModule} from '@angular/material/menu';
import { MatGridListModule} from '@angular/material/grid-list';
import { MatExpansionModule} from '@angular/material/expansion';
import { MatSliderModule} from '@angular/material/slider';
import { MatSelectModule} from '@angular/material/select';
import { MatCheckboxModule} from '@angular/material/checkbox';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';
import { GameComponent } from './game/game.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { far } from '@fortawesome/free-regular-svg-icons';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { fab } from '@fortawesome/free-brands-svg-icons';

// Add icons to the library for convenient access in other components
import { FaIconLibrary } from '@fortawesome/angular-fontawesome';
import { WordAssociationComponent } from './word-association/word-association.component';
import { SolutionComponent } from './solution/solution.component';
import { environment } from 'src/environments/environment';
 
const config: SocketIoConfig = { url: environment.websocket, options: {} };

@NgModule({
  declarations: [
    AppComponent,
    WaitingRoomComponent,
    GameComponent,
    WordAssociationComponent,
    SolutionComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    SocketIoModule.forRoot(config),
    BrowserAnimationsModule,
    MatToolbarModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatCardModule,
    MatTabsModule,
    MatChipsModule,
    MatDividerModule,
    MatMenuModule,
    MatGridListModule,
    MatExpansionModule,
    MatSliderModule,
    MatSelectModule,
    MatCheckboxModule,
    MatSlideToggleModule,
    FontAwesomeModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
  constructor(library: FaIconLibrary) {
    // Add multiple icons to the library
    library.addIconPacks(far, fas, fab);
  }
}

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
import { MatLegacyInputModule as MatInputModule } from '@angular/material/legacy-input';
import { MatLegacyButtonModule as MatButtonModule } from '@angular/material/legacy-button';
import { MatIconModule } from '@angular/material/icon';
import { MatLegacyListModule as MatListModule} from '@angular/material/legacy-list';
import { MatLegacyCardModule as MatCardModule} from '@angular/material/legacy-card';
import { MatLegacyTabsModule as MatTabsModule} from '@angular/material/legacy-tabs';
import { MatLegacyChipsModule as MatChipsModule} from '@angular/material/legacy-chips';
import { MatDividerModule} from '@angular/material/divider';
import { MatLegacyMenuModule as MatMenuModule} from '@angular/material/legacy-menu';
import { MatGridListModule} from '@angular/material/grid-list';
import { MatExpansionModule} from '@angular/material/expansion';
import { MatLegacySliderModule as MatSliderModule} from '@angular/material/legacy-slider';
import { MatLegacySelectModule as MatSelectModule} from '@angular/material/legacy-select';
import { MatLegacyCheckboxModule as MatCheckboxModule} from '@angular/material/legacy-checkbox';
import {MatLegacySlideToggleModule as MatSlideToggleModule} from '@angular/material/legacy-slide-toggle';
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

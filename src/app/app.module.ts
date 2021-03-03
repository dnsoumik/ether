import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FlexLayoutModule } from '@angular/flex-layout';
import { InputComponent } from './components/input/input.component';
import { ButtonComponent } from './components/button/button.component';
import { MatPseudoCheckboxModule, MatRippleModule } from '@angular/material/core';
import { NgxJsonViewerModule } from 'ngx-json-viewer';
import { AceEditorModule } from 'ng2-ace-editor';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatButtonModule } from '@angular/material/button';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { MatListModule } from '@angular/material/list';
import { MatExpansionModule } from '@angular/material/expansion';
import { CheckboxComponent } from './components/checkbox/checkbox.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { VesselComponent } from './components/vessel/vessel.component';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { SelectComponent } from './components/select/select.component';
import { DropdownComponent } from './components/dropdown/dropdown.component';
import { MatSelectModule } from '@angular/material/select';

@NgModule({
  declarations: [
    AppComponent,
    InputComponent,
    ButtonComponent,
    CheckboxComponent,
    VesselComponent,
    SelectComponent,
    DropdownComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatFormFieldModule,
    FlexLayoutModule,
    MatRippleModule,
    NgxJsonViewerModule,
    AceEditorModule,
    MatIconModule,
    MatToolbarModule,
    MatTooltipModule,
    MatButtonModule,
    DragDropModule,
    MatListModule,
    MatExpansionModule,
    MatCheckboxModule,
    MatSlideToggleModule,
    FormsModule,
    MatCardModule,
    MatTabsModule,
    MatSelectModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

import { Component } from '@angular/core';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  title = 'demo';
  mainData = {
    "data": [
      {
        "id": "input",
        "label": "First name"
      },
      {
        "id": "input",
        "label": "Last name"
      },
      {
        "id": "input",
        "label": "Phone number"
      },
      {
        "id": "input",
        "label": "Email (optional)"
      },
      {
        "id": "button",
        "label": "Submit"
      }
    ],
    "style": {
      'padding': '10px'
    }
  };

  get mainDataInString() {
    return JSON.stringify(this.mainData, null, 2);
  }

  set mainDataInString(v) {
    try {
      this.mainData = JSON.parse(v);
    }
    catch (e) {
      console.log('error occored while you were typing the JSON');
    };
  }

  onMobilePreview() {
    document.getElementById('preview_container').style.width = '400px';
    document.getElementById('preview_container').style.height = '800px';
  }

  onDesktopPreview() {
    document.getElementById('preview_container').style.width = '100%';
    document.getElementById('preview_container').style.height = '100%';
  }

  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.mainData.data, event.previousIndex, event.currentIndex);
  }


}

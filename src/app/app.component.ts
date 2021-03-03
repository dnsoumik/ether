import { Component } from '@angular/core';
import { CdkDragDrop, moveItemInArray, copyArrayItem } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  title = 'demo';

  componentList = {
    'basic': [
      {
        'id': 'input',
        'label': 'Text Field',
        'icon': 'input',
        "expand": false,
      },
      {
        'id': 'button',
        'label': 'Mat Raised Button',
        'icon': 'smart_button',
        "expand": false,
      },
      {
        'id': 'checkbox',
        'label': 'Checkbox',
        'icon': 'check_box',
        "expand": false,
      },
      {
        'id': 'dropdown',
        'label': 'Dropdown',
        'icon': 'arrow_drop_down_circle',
        "expand": false,
      }
    ]
  };

  mainData = {
    "data": [
      {
        "id": "input",
        "label": "First name",
        "expand": false,
      },
      {
        "id": "input",
        "label": "Last name",
        "expand": false,
      },
      {
        "id": "input",
        "expand": false,
        "label": "Phone number"
      },
      {
        "id": "input",
        "expand": false,
        "label": "Email (optional)"
      },
      {
        "id": "button",
        "expand": false,
        "label": "Submit"
      }
    ],
    "style": {
      'width': '100%',
      'padding': '10px',
      'padding-top': '50px',
      'padding-bottom': '50px',
    }
  };

  get mainDataInString() {
    return JSON.stringify(this.mainData, null, 4);
  }

  set mainDataInString(v) {
    try {
      this.mainData = JSON.parse(v);
    }
    catch (e) {
      // console.log(e, 'error occored while you were typing the JSON');
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


  drop2(event: any) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      copyArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }

    if (this.currentSelectedIndex != null) {
      this.mainData.data[this.currentSelectedIndex].expand = false;
    }

    setTimeout(() => {
      this.currentSelectedIndex = event.currentIndex;
      this.mainData.data[event.previousIndex].expand = false;
      this.mainData.data[event.currentIndex].expand = true;
    }, 100);
    this.currentSelectedItem = JSON.parse(JSON.stringify(this.mainData.data[event.currentIndex]));
  }

  currentSelectedIndex: number = null;
  currentSelectedItem: any = {
    'id': '',
    'label': '',
    'icon': '',
  };
  onSelected(i: number, item: any) {
    console.log('on_selected', i, item);
    this.currentSelectedItem = item;
    if (this.currentSelectedIndex == null) {
      this.currentSelectedIndex = i;
      this.mainData.data[i].expand = true;
      this.labelController = this.mainData.data[i].label;
    } else {
      this.currentSelectedIndex = this.currentSelectedIndex;
      this.mainData.data[this.currentSelectedIndex].expand = false;

      this.currentSelectedIndex = i;
      this.mainData.data[i].expand = true;
      this.labelController = this.mainData.data[i].label;
    }
  }

  onEdit(i: number, item: any): void {
    console.log(i, item);
  }

  labelController = '';
  onDelete(i: number, item: any) {
    // console.log(i, item);
    this.mainData.data.splice(i, 1);
    this.currentSelectedIndex = null;
  }

  onChangeSave(i: number, item: any) {
    console.log(i, item);
    this.mainData.data[i].label = this.labelController;
  }

  onClone(i: number, item: any) {
    console.log('on_clone', i, item);
    // item.expand = false;
    this.mainData.data.splice(i, 0, item);
    setTimeout(() => {
      this.mainData.data[i].expand = true;
      this.mainData.data[i + 1].expand = false;
    }, 50);
  }

  onMouseHover(i) {
    console.log('on', i);
    document.getElementById('action_viewer').style.display = 'block';
    document.getElementById('component_viewer').style.display = 'none';
  }

  onMouseHoverLeave(i) {
    console.log('leave', i);
  }

  onSave(i: number, element: any) {
    console.log('on_save', i);
    this.mainData.data[this.currentSelectedIndex] = this.currentSelectedItem;
  }

  onMoveUp(i: number, element: any): void {
    let oData = this.mainData.data[i - 1];
    oData.expand = false;
    this.mainData.data.splice(i - 1, 1, element);
    this.mainData.data.splice(i, 1, oData);
  }

  onMoveDown(i: number, element: any): void {
    console.log(i, element);
    let oData = this.mainData.data[i + 1];
    oData.expand = false;
    this.mainData.data.splice(i + 1, 1, element);
    this.mainData.data.splice(i, 1, oData);
  }


}

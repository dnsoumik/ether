import { Component } from '@angular/core';
import { CdkDragDrop, moveItemInArray, copyArrayItem } from '@angular/cdk/drag-drop';
import { Compute } from './compute/compute';
import { environment } from 'src/environments/environment';
import { ActivatedRoute } from '@angular/router';
import { Log } from './util/log_util';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  title = 'demo';
  environment = environment;

  componentList = {
    'basic': [
      {
        'id': 'input',
        'label': 'Text Field',
        'icon': 'input',
        "eSelect": false,
        'eId': Compute.getUniqueId(),
        childs: [],
      },
      {
        'id': 'checkbox',
        'label': 'Checkbox',
        'icon': 'check_box',
        "eSelect": false,
        'eId': Compute.getUniqueId(),
        childs: [],
      },
      {
        'id': 'dropdown',
        'label': 'Dropdown',
        'icon': 'arrow_drop_down_circle',
        "eSelect": false,
        'eId': Compute.getUniqueId(),
        childs: [
          {
            text: 'Value 1',
            valueType: 'string',
            value: 'value1'
          },
          {
            text: 'Value 2',
            valueType: 'string',
            value: 'value2'
          },
          {
            text: 'Value 3',
            valueType: 'string',
            value: 'value3'
          }
        ]
      },
      {
        'id': 'button',
        'label': 'Button',
        'icon': 'smart_button',
        "eSelect": false,
        'eId': Compute.getUniqueId(),
        childs: [],
      },
    ]
  };

  mainData = {
    "data": [
    ],
    "style": {
      'width': '100%',
      'min-height': '600px',
      'padding': '10px',
      'padding-top': '50px',
      'padding-bottom': '50px',
    }
  };

  constructor(private activatedRoute: ActivatedRoute) {
    
  }

  ngOnInit(): void {
    setTimeout(() => {
      this.activatedRoute.queryParams.subscribe(params => {

        const parms: Object = params;
        Log.i('params', parms);
        if (parms['edit'] != undefined && parms['edit'] != null && parms['edit'] == 'true') {
          this.mainData.data = [
            {
              "id": "input",
              "label": "Title of the Scheme",
              "eSelect": false,
              'eId': Compute.getUniqueId(),
              childs: [],
            },
            {
              'id': 'dropdown',
              'label': 'Scheme Category',
              'icon': 'arrow_drop_down_circle',
              "eSelect": false,
              'eId': Compute.getUniqueId(),
              childs: [
                {
                  text: 'Capital Expenditure',
                  value: 'Capital Expenditure',
                },
                {
                  text: 'Construction',
                  value: 'Resort',
                },
                {
                  text: 'Vehicle',
                  value: 'Guest House',
                },
                {
                  text: 'Mechinery and Equipment',
                  value: 'Homestay',
                },
                {
                  text: 'Scholarship',
                  value: 'Scholarship',
                },
                {
                  text: 'Grant in Aid/Subsidy',
                  value: 'Scholarship',
                },
                {
                  text: 'Cretion of Posts',
                  value: 'Cretion of Posts',
                }
              ]
            },
            {
              "id": "input",
              "eSelect": false,
              "label": "Phone number",
              'eId': Compute.getUniqueId(),
              childs: [],
            },
            {
              "id": "input",
              "eSelect": false,
              "label": "Email (optional)",
              'eId': Compute.getUniqueId(),
              childs: [],
            },
            {
              "id": "button",
              "eSelect": false,
              "label": "Submit",
              'eId': Compute.getUniqueId(),
              childs: [],
            }
          ]
        }
      });
    }, 200);
  }

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
    document.getElementById('preview_container').style.height = '600px';
    document.getElementById('template_viewer').style.width = '400px';
    document.getElementById('template_viewer').style.height = '600px';
  }

  onDesktopPreview() {
    document.getElementById('preview_container').style.width = '100%';
    document.getElementById('preview_container').style.height = '600px';
    document.getElementById('template_viewer').style.width = '100%';
    document.getElementById('template_viewer').style.height = '600px';
  }

  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.mainData.data, event.previousIndex, event.currentIndex);
  }


  drop2(event: any) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
      setTimeout(() => {
        this.currentSelectedIndex = event.currentIndex;
        this.mainData.data[event.currentIndex].eSelect = true;
        this.currentSelectedItem = JSON.parse(JSON.stringify(this.mainData.data[event.currentIndex]));
      }, 200);
    } else {
      copyArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
      this.mainData.data[event.currentIndex].eId = Compute.getUniqueId();
    }
  }

  currentSelectedIndex: number = null;
  currentSelectedItem: any = {
    'id': '',
    'label': '',
    'icon': '',
    'eId': '',
  };
  selectedElementDefault = {
    'id': '',
    'label': '',
    'icon': '',
    'eId': '',
  };
  onSelected(j: number, item: any) {
    console.log('on_selected', j, item);
    if (this.currentSelectedIndex != null) {
      console.log('id_matched_idx', item.eId);
      console.log('id_matched_2', this.currentSelectedItem.eId);
      for (let i = 0; i < this.mainData.data.length; i++) {
        let idx = this.mainData.data[i];
        if (idx.eSelect) {
          this.mainData.data[i].eSelect = false;
          break;
        }
      }
    }
    setTimeout(() => {
      this.currentSelectedIndex = j;
      this.mainData.data[j].eSelect = true;
      this.currentSelectedItem = item;
    }, 100);
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
    // item.eSelect = false;
    this.mainData.data.splice(i, 0, item);
    this.mainData.data[i + 1].eSelect = false;    
    setTimeout(() => {
      this.mainData.data[i].eSelect = true;
      this.mainData.data[i + 1].eId = Compute.getUniqueId();
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

  onSave(n: number, element: any) {
    console.log('on_save', n);
    for (let i = 0; i < this.mainData.data.length; i++) {
      let idx = this.mainData.data[i];
      if (idx.eId == this.currentSelectedItem.eId) {
        this.mainData.data[i] = this.currentSelectedItem;
        break;
      }
    }
  }

  onMoveUp(i: number, element: any): void {
    let oData = this.mainData.data[i - 1];
    oData.eSelect = false;
    this.mainData.data.splice(i - 1, 1, element);
    this.mainData.data.splice(i, 1, oData);
  }

  onMoveDown(i: number, element: any): void {
    console.log(i, element);
    let oData = this.mainData.data[i + 1];
    oData.eSelect = false;
    this.mainData.data.splice(i + 1, 1, element);
    this.mainData.data.splice(i, 1, oData);
  }

  onClear(i: number) {
    this.currentSelectedIndex = null;
    this.currentSelectedItem = this.selectedElementDefault;
    this.mainData.data[i].eSelect = false;
  }


}

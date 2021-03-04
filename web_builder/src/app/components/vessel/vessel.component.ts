import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-vessel',
  templateUrl: './vessel.component.html',
  styleUrls: ['./vessel.component.scss']
})
export class VesselComponent implements OnInit {

  @Input()
  value: any;

  constructor() { }

  ngOnInit(): void {
  }

}


import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:hovering/hovering.dart';

class VesselEditor extends StatefulWidget {

  Map data;
  VesselEditor({this.data});

  @override
  _VesselEditorState createState() => _VesselEditorState();
}

class _VesselEditorState extends State<VesselEditor> {
  @override
  Widget build(BuildContext context) {
    return HoverWidget(
      child: Container(
        child: buildVessel(widget.data),
      ),
      hoverChild: Stack(
        alignment: Alignment.topLeft,
        children: [
          buildElementVision(),
          IgnorePointer(
            ignoring: true,
            child: buildVessel(widget.data),
          ),
        ],
      ),
      onHover: (event) {

      },
    );
  }

  Widget buildElementVision() {
    return InkWell(
      onTap: () {
        log('clicked');
      },
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(
              color: Colors.blue,
              width: 2
          ),
        ),
        height: 70,
        width: MediaQuery.of(context).size.width,
        // color: Colors.blue[900].withAlpha(150),
        alignment: Alignment.topLeft,
        child: Container(
          color: Colors.blue,
          padding: EdgeInsets.only(
            left: 10,
            right: 20,
          ),
          child: Text(
            widget.data['eId'],
            style: TextStyle(
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }

  Widget buildVessel(Map data) {
    Widget vessel = Text('N/A');

    if (data['eId'] == 'input') {
      vessel = Container(
        child: TextField(
          decoration: InputDecoration(
              labelText: data['label']
          ),
        ),
      );
    } else if (data['eId'] == 'text') {
      vessel = Container(
        child: Text(
            data['label']
        ),
      );
    } else if (data['eId'] == 'button') {
      vessel = Container(
        width: MediaQuery.of(context).size.width,
        child: ElevatedButton(
          child: Text(
            data['label'],
          ),
          onPressed: () {
          },
        ),
      );
    } else if (data['eId'] == 'checkbox') {
      vessel = Container(
        width: MediaQuery.of(context).size.width,
        child: Row(
          children: [
            Checkbox(
              value: true,
              onChanged: (a) {

              },
            ),
            Text(data['label'])
          ],
        ),
      );
    }

    vessel = Container(
      margin: EdgeInsets.only(
        top: 10,
        right: 10,
        bottom: 10,
      ),
      child: vessel,
    );

    return vessel;
  }

}

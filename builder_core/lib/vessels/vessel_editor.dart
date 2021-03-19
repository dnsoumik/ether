
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
    return Stack(
      children: [
        (widget.data['eSelect'] ==  true)? buildElementVision(Colors.deepOrangeAccent): Container(),
        HoverWidget(
          child: Container(
            alignment: Alignment.center,
            child: buildVessel(widget.data),
          ),
          hoverChild: Stack(
            alignment: Alignment.topLeft,
            children: [
              buildElementVision(Colors.blue[800]),
              buildVessel(widget.data),
            ],
          ),
          onHover: (event) {

          },
        ),
      ],
    );
  }

  Widget buildElementVision(Color backColor) {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(
            color: backColor,
            width: 2
        ),
      ),
      height: 70,
      width: MediaQuery.of(context).size.width,
      // color: Colors.blue[900].withAlpha(150),
      alignment: Alignment.topLeft,
      child: Container(
        color: backColor,
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
    );
  }

  Widget buildVessel(Map data) {
    Widget vessel = Text('N/A');

    if (data['eId'] == 'input') {
      vessel = Container(
        width: MediaQuery.of(context).size.width,
        child: TextField(
          decoration: InputDecoration(
              labelText: data['label']
          ),
        ),
      );
    } else if (data['eId'] == 'text') {
      vessel = Container(
        width: MediaQuery.of(context).size.width,
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
    } else if (data['eId'] == 'dropdown') {
      vessel = DropdownButtonFormField<String>(
        value: '1',
        decoration: InputDecoration(
          labelText: data['label'],
        ),
        items: ['1', '2', '3', '4', '5']
            .map((label) => DropdownMenuItem(
          child: Text(label.toString()),
          value: label,
        ))
            .toList(),
        hint: Text(data['label']),
        onChanged: (value) {
          // setState(() {
          //   _ratingController = value;
          // });
        },
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

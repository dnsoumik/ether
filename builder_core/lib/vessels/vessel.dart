

import 'package:ether/util/log_util.dart';
import 'package:flutter/material.dart';

class Vessel extends StatefulWidget {
  Map data;
  var xController;
  Vessel({this.data, this.xController});

  @override
  _VesselState createState() => _VesselState();
}

class _VesselState extends State<Vessel> {

  @override
  Widget build(BuildContext context) {
    return Container(
      child: buildVessel(widget.data),
    );
  }

  Widget buildVessel(Map data) {
    Widget vessel = Text('N/A');

    if (data['eId'] == 'input') {
      var x = TextEditingController();
      widget.xController = '';
      vessel = Container(
        child: TextField(
          decoration: InputDecoration(
              labelText: data['label']
          ),
          controller: x,
          onChanged: (value) {
            widget.xController = value;
          },
          onEditingComplete: () {
            widget.xController = x.text;
          },
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
      widget.xController = false;
      vessel = Container(
        width: MediaQuery.of(context).size.width,
        child: Row(
          children: [
            Checkbox(
              value: widget.xController,
              onChanged: (a) {

              },
            ),
            Text(data['label'])
          ],
        ),
      );
    } else if (data['eId'] == 'dropdown') {
      widget.xController = '1';
      vessel = DropdownButtonFormField<String>(
        value: widget.xController,
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

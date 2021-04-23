

import 'package:flutter/material.dart';

class Vessel extends StatefulWidget {
  Map data;
  Vessel({this.data});

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

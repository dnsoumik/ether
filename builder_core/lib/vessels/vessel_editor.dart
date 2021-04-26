import 'dart:developer';

import 'package:ether/util/toast_util.dart';
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
        (widget.data['eSelect'] == true)
            ? buildElementVision(Colors.deepOrangeAccent)
            : Container(),
        IgnorePointer(
          ignoring: (widget.data['eSelect'] == true),
          child: HoverWidget(
            child: Container(
              alignment: Alignment.center,
              child: IgnorePointer(ignoring: true, child: buildVessel(widget.data)),
            ),
            hoverChild: Stack(
              alignment: Alignment.topCenter,
              children: [
                buildElementVision(Colors.blue[800]),
                IgnorePointer(ignoring: true, child: buildVessel(widget.data)),
              ],
            ),
            onHover: (event) {},
          ),
        ),
      ],
    );
  }

  Widget buildElementVision(Color backColor) {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: backColor, width: 2),
      ),
      height: 70,
      width: MediaQuery.of(context).size.width,
      alignment: Alignment.topLeft,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
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
          Visibility(
            visible: (backColor == Colors.deepOrangeAccent),
            child: Container(
              color: backColor,
              padding: EdgeInsets.only(
                left: 5,
                right: 5,
              ),
              child: Row(
                children: [
                  IconButton(
                    icon: Icon(
                      Icons.arrow_upward,
                      color: Colors.white,
                    ),
                    tooltip: 'Move up',
                    onPressed: () {},
                  ),
                  IconButton(
                    icon: Icon(
                      Icons.arrow_downward,
                      color: Colors.white,
                    ),
                    tooltip: 'Move down',
                    onPressed: () {},
                  ),
                  IconButton(
                    icon: Icon(
                      Icons.clear,
                      color: Colors.white,
                    ),
                    tooltip: 'Delete element',
                    onPressed: () {
                      Toaster.w(context, message: 'Element has been deleted');
                    },
                    splashColor: Colors.black,
                  ),
                ],
              ),
            ),
          ),
        ],
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
        alignment: Alignment.center,
        child: Text(data['label']),
      );
    } else if (data['eId'] == 'button') {
      vessel = Container(
        width: MediaQuery.of(context).size.width,
        child: ElevatedButton(
          child: Text(
            data['label'],
          ),
          onPressed: () {},
        ),
      );
    } else if (data['eId'] == 'checkbox') {
      vessel = Container(
        width: MediaQuery.of(context).size.width,
        child: Row(
          children: [
            Checkbox(
              value: true,
              onChanged: (a) {},
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

/// Flutter code sample for Draggable

// The following example has a [Draggable] widget along with a [DragTarget]
// in a row demonstrating an incremented `acceptedData` integer value when
// you drag the element to the target.

import 'package:flutter/material.dart';

import 'drag_handle_example.dart';

void main() => runApp(MyApp());

/// This is the main application widget.
class MyApp extends StatelessWidget {
  static const String _title = 'Flutter Code Sample';

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: _title,
      home: Scaffold(
        appBar: AppBar(title: const Text(_title)),
        body: DragHandleExample(),
      ),
    );
  }
}

/// This is the stateful widget that the main application instantiates.
class MyStatefulWidget extends StatefulWidget {
  MyStatefulWidget({Key key}) : super(key: key);

  @override
  _MyStatefulWidgetState createState() => _MyStatefulWidgetState();
}

/// This is the private State class that goes with MyStatefulWidget.
class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  int acceptedData = 0;
  Widget build(BuildContext context) {
    return Row(
      // mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Flexible(
          flex: 1,
          child: Container(
            color: Colors.blue,
            width: MediaQuery.of(context).size.width,
            child: Draggable<int>(
              // Data is the value this Draggable stores.
              data: 10,
              child: Container(
                height: 100.0,
                color: Colors.lightGreenAccent,
                child: Center(
                  child: Text("Draggable"),
                ),
              ),
              feedback: Container(
                color: Colors.deepOrange,
                height: 100,
                width: 100,
                child: Icon(Icons.directions_run),
              ),
              childWhenDragging: Container(
                height: 100.0,
                width: 100.0,
                color: Colors.pinkAccent,
                child: Center(
                  child: Text("Child When Dragging"),
                ),
              ),
            ),
          ),
        ),
        Flexible(
          flex: 4,
          child: Container(
            color: Colors.red,
            child: DragTarget(
              builder: (
                  BuildContext context,
                  List<dynamic> accepted,
                  List<dynamic> rejected,
                  ) {
                return Container(
                  height: 100.0,
                  color: Colors.cyan,
                  child: Center(
                    child: Text("Value is updated to: $acceptedData"),
                  ),
                );
              },
              onAccept: (int data) {
                setState(() {
                  acceptedData += data;
                });
              },
            ),
          ),
        ),
        Flexible(
          flex: 1,
          child: Container(
            color: Colors.green,
          ),
        )
      ],
    );
  }
}

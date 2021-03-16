import 'dart:convert';
import 'dart:developer';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_icons/flutter_icons.dart';
import 'package:flutter_json_widget/flutter_json_widget.dart';

void main() => runApp(new MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: App(),
      ),
    );
  }
}

class App extends StatefulWidget {
  @override
  AppState createState() => AppState();
}

class AppState extends State<App> {

  Color caughtColor = Colors.grey;
  int acceptedData = 0;

  List<Map> components = [
      {
        "title": "Basic",
        "children": [
          {
            "eId": "text",
            "label": "Text",
            "icon": "text_fields",
            "eSelect": false,
            "id": "",
            "children": [
              {
                "text": "",
                "valueType": "string",
                "value": 19
              }
            ]
          },
          {
            "eId": "input",
            "label": "Input Field",
            "icon": "input",
            "eSelect": false,
            "id": "",
            "children": [
              {
                "text": "",
                "valueType": "string",
                "value": 19
              }
            ]
          },
          {
            "eId": "button",
            "label": "Button",
            "icon": "input",
            "eSelect": false,
            "id": "",
            "children": [
              {
                "text": "",
                "valueType": "string",
                "value": 19
              }
            ]
          }
        ]
      }
  ];

  List<Map> mainData = [
    {
      "eId": "input",
      "label": "Text Field",
      "icon": "input",
      "eSelect": false,
      "id": "",
      "children": [
        {
          "text": "",
          "valueType": "string",
          "value": 19
        }
      ]
    }
  ];

  @override
  Widget build(BuildContext context) {
    var testString = '''{
        "I": "How are you?",
        "You": "Excellent!"}
        ''';
    Map<String, dynamic> jsonObj = jsonDecode(json.encode({"root": mainData}));
    return Scaffold(
      appBar: AppBar(
        title: Text('Ether v1.0.0'),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              height: 600,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: <Widget>[
                  Flexible(
                    flex: 1,
                    child: Container(
                      width: MediaQuery.of(context).size.width,
                      height: MediaQuery.of(context).size.height,
                      child: Column(
                        children: componentsViewer(),
                      ),
                    ),
                  ),
                  Flexible(
                    flex: 3,
                    child: Container(
                      width: MediaQuery.of(context).size.width,
                      height: MediaQuery.of(context).size.height,
                      child: DragTarget<Map>(
                        builder: (
                            BuildContext context,
                            List<dynamic> accepted,
                            List<dynamic> rejected,
                            ) {
                          return Column(
                            children: vesselViewer(),
                          );
                        },
                        onAccept: (data) {
                          setState(() {
                            mainData.add(data);
                            // acceptedData += data;
                          });
                        },
                        onMove: (data) {
                          return Container(
                            height: 200,
                            width: 100,
                            color: Colors.black,
                          );
                        },
                      ),
                    ),
                  ),
                  Flexible(
                      child: Container(
                        color: Colors.blue,
                        child: DefaultTabController(
                          length: 2,
                          child: new Scaffold(
                            appBar: new PreferredSize(
                              preferredSize: Size.fromHeight(kToolbarHeight+20),
                              child: new Container(
                                color: Colors.green,
                                child: new SafeArea(
                                  child: Column(
                                    children: <Widget>[
                                      new Expanded(child: new Container()),
                                      new TabBar(
                                        tabs: [
                                          Tab(
                                              icon: Icon(Icons.vertical_split),
                                              text: "Content",
                                          ),
                                          Tab(
                                              icon: Icon(Icons.brush),
                                              text: "Style",
                                          )
                                        ],
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                            body: new TabBarView(
                              children: <Widget>[
                                new Column(
                                  children: <Widget>[new Text("Lunches Page")],
                                ),
                                new Column(
                                  children: <Widget>[new Text("Cart Page")],
                                )
                              ],
                            ),
                          ),
                        ),
                      )
                  ),
                ],
              ),
            ),
            Container(
              margin: EdgeInsets.only(
                top: 50,
                bottom: 50,
                left: 30,
                right: 30,
              ),
              child: Column(
                children: [
                  Container(
                    margin: EdgeInsets.only(
                      top: 20,
                      bottom: 20,
                      // left: 20,
                      // right: 20,
                    ),
                    padding: EdgeInsets.only(
                      top: 10,
                      bottom: 10,
                    ),
                    width: MediaQuery.of(context).size.width,
                    alignment: Alignment.center,
                    color: Colors.blue[300],
                    child: Text(
                      'Mata-data viewer',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Flexible(
                        flex: 1,
                          child: SafeArea(
                            child: SingleChildScrollView(
                                child: JsonViewerWidget(jsonObj)
                            ),
                          ),
                      ),
                      Flexible(
                        flex: 1,
                        child: Text(mainData.toString()),
                      )
                    ],
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }

  List<Widget> componentsViewer() {
    List<Widget> list = [];

    for (int i =0; i < components[0]['children'].length; i++) {
      list.add(
          Draggable<Map>(
            // Data is the value this Draggable stores.
            data: components[0]['children'][i],
            child: buildComponent(components[0]['children'][i]),
            feedback: buildComponent(components[0]['children'][i]),
            childWhenDragging: buildComponent(components[0]['children'][i]),
          )
      );
    }
    return list;
  }

  Widget buildComponent(Map component) {
    return Card(
      child: Container(
        constraints: BoxConstraints(
          minWidth: 100,
          maxWidth: 200,
        ),
        child: ListTile(
          leading: Icon(
            Icons.text_fields,
          ),
          title: Text(component['label']),
        ),
      ),
    );
  }

  List<Widget> vesselViewer() {
    List<Widget> list = [];

    for (int i =0; i < mainData.length; i++) {
      list.add(
        buildVessel(mainData[i])
      );
    }
    return list;
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


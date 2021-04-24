import 'dart:async';
import 'dart:convert';
import 'dart:developer';

import 'package:dio/dio.dart';
import 'package:ether/compute.dart';
import 'package:ether/handler/static_memory.dart';
import 'package:ether/util/log_util.dart';
import 'package:ether/util/toast_util.dart';
import 'package:ether/vessels/vessel.dart';
import 'package:ether/vessels/vessel_editor.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_json_widget/flutter_json_widget.dart';

class EtherBuilder extends StatefulWidget {
  @override
  AppState createState() => AppState();
}

class AppState extends State<EtherBuilder> {
  Color caughtColor = Colors.grey;
  int acceptedData = 0;

  Dio dio;
  BuildContext _context;

  AppState() {
    var options = BaseOptions(
      baseUrl: BuildConfig.serverUrl,
      connectTimeout: 5000,
      receiveTimeout: 5000,
    );
    dio = Dio(options);
  }

  List<Map> components = [
    {
      "title": "Basic",
      "children": [
        {
          "eId": "text",
          "label": "Text",
          "icon": "text_fields",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        },
        {
          "eId": "input",
          "label": "Input Field",
          "icon": "input",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        },
        {
          "eId": "button",
          "label": "Button",
          "icon": "input",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        },
        {
          "eId": "dropdown",
          "label": "Dropdown",
          "icon": "input",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        },
        {
          "eId": "checkbox",
          "label": "Checkbox",
          "icon": "input",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        },
        {
          "eId": "divider",
          "label": "Divider",
          "icon": "input",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        },
        {
          "eId": "toggle",
          "label": "Toggle Button",
          "icon": "input",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        },
        {
          "eId": "progressbar",
          "label": "Progressbar",
          "icon": "input",
          "eSelect": false,
          "id": Compute.getUniqueKey(),
          "children": [
            {"text": "", "valueType": "string", "value": 19}
          ]
        }
      ]
    }
  ];

  List<Map> mainData = [];

  TextEditingController _labelEditor = new TextEditingController();
  TextEditingController _formTitle = new TextEditingController();
  @override
  Widget build(BuildContext context) {
    var testString = '''{
        "I": "How are you?",
        "You": "Excellent!"}
        ''';
    Map<String, dynamic> jsonObj = json.decode(json.encode({"root": mainData}));
    return Scaffold(
      appBar: AppBar(
        title: Text('Create new form'),
      ),
      body: SingleChildScrollView(
        child: Container(
          padding: EdgeInsets.all(20),
          width: MediaQuery.of(context).size.width,
          child: Column(
            children: [
              TextField(
                controller: _formTitle,
                decoration: new InputDecoration(
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                        width:2,
                      color: Colors.blue
                    ),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderSide: BorderSide(
                        width: 2,
                    ),
                  ),
                  hintText: 'Form title',
                ),
              ),
              SizedBox(
                height: 20,
              ),
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
                        padding: EdgeInsets.all(10),
                        margin: EdgeInsets.all(10),
                        decoration: BoxDecoration(
                            border: Border.all(
                          color: Colors.black,
                        )),
                        width: MediaQuery.of(context).size.width,
                        height: MediaQuery.of(context).size.height,
                        child: DragTarget<Map>(
                          builder: (
                            BuildContext context,
                            List<dynamic> accepted,
                            List<dynamic> rejected,
                          ) {
                            return Column(
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: vesselEditor(),
                            );
                          },
                          onAccept: (data) {
                            setState(() {
                              data['id'] = Compute.getUniqueKey();
                              mainData.add(new Map.from(data));
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
                            preferredSize: Size.fromHeight(kToolbarHeight + 20),
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
                              (selectElement != null)
                                  ? Column(
                                      children: <Widget>[
                                        Text('Basic setting'),
                                        TextField(
                                          controller: _labelEditor,
                                          decoration:
                                              InputDecoration(labelText: 'Label'),
                                        ),
                                        SizedBox(
                                          height: 40,
                                        ),
                                        Row(
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          children: [
                                            ElevatedButton(
                                              onPressed: () {
                                                onSave();
                                              },
                                              child: Row(
                                                mainAxisSize: MainAxisSize.min,
                                                children: [
                                                  Text('Save'),
                                                  Icon(Icons.check),
                                                ],
                                              ),
                                            ),
                                            SizedBox(
                                              width: 20,
                                            ),
                                            ElevatedButton(
                                              onPressed: () {
                                                onDiscard();
                                              },
                                              style: ElevatedButton.styleFrom(
                                                primary: Colors.red, // background
                                                onPrimary:
                                                    Colors.white, // foreground
                                              ),
                                              child: Row(
                                                mainAxisSize: MainAxisSize.min,
                                                children: [
                                                  Text('Discard'),
                                                  Icon(Icons.close),
                                                ],
                                              ),
                                            ),
                                          ],
                                        ),
                                      ],
                                    )
                                  : Container(),
                              new Column(
                                children: <Widget>[new Text("Style page")],
                              )
                            ],
                          ),
                        ),
                      ),
                    )),
                  ],
                ),
              ),
              // Container(
              //   margin: EdgeInsets.only(
              //     top: 50,
              //     bottom: 50,
              //     left: 30,
              //     right: 30,
              //   ),
              //   child: Column(
              //     children: [
              //       Container(
              //         margin: EdgeInsets.only(
              //           top: 20,
              //           bottom: 20,
              //           // left: 20,
              //           // right: 20,
              //         ),
              //         padding: EdgeInsets.only(
              //           top: 10,
              //           bottom: 10,
              //         ),
              //         width: MediaQuery.of(context).size.width,
              //         alignment: Alignment.center,
              //         color: Colors.blue[300],
              //         child: Text(
              //           'Mata-data viewer',
              //           style: TextStyle(
              //             fontSize: 18,
              //             fontWeight: FontWeight.bold,
              //           ),
              //         ),
              //       ),
              //       Row(
              //         crossAxisAlignment: CrossAxisAlignment.start,
              //         children: [
              //           Flexible(
              //             flex: 1,
              //             child: SafeArea(
              //               child: SingleChildScrollView(
              //                   child: JsonViewerWidget(jsonObj, notRoot: true,)
              //               ),
              //             ),
              //           ),
              //           Flexible(
              //             flex: 1,
              //             child: Text(mainData.toString()),
              //           )
              //         ],
              //       ),
              //     ],
              //   ),
              // ),
              Container(
                margin: EdgeInsets.only(
                  top: 20,
                  left: 20,
                  right: 20,
                  bottom: 80,
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
                      color: Colors.green[300],
                      child: Text(
                        'View Renderer',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    Container(
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.black),
                      ),
                      padding: EdgeInsets.all(10),
                      child: Column(
                        children: vesselViewer(),
                      ),
                    ),
                  ],
                ),
              ),

              Container(
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ElevatedButton(
                      onPressed: () {

                      },
                      child: Container(
                        padding: EdgeInsets.only(
                          left: 20,
                          right: 20,
                          top: 10,
                          bottom: 10
                        ),
                        child: Text(
                            'Create Form',
                          style: TextStyle(
                            fontSize: 18
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(
                height: 50,
              ),
            ],
          ),
        ),
      ),
    );
  }

  onCreateNewForm() async {

    // Validation
    if (_formTitle.text.length == 0) {
      Toaster.e(message: '')
    }

    var response = await dio.get('/forms', queryParameters: {});
    try {
      Log.i(response);
    } catch (e, s) {
      Log.e(e, s);
    }
  }

  List<Widget> componentsViewer() {
    List<Widget> list = [];

    for (int i = 0; i < components[0]['children'].length; i++) {
      list.add(Draggable<Map>(
        // Data is the value this Draggable stores.
        data: components[0]['children'][i],
        child: buildComponent(components[0]['children'][i]),
        feedback: buildComponent(components[0]['children'][i]),
        childWhenDragging: buildComponent(components[0]['children'][i]),
      ));
    }
    return list;
  }

  onSave() {
    selectElement['label'] = _labelEditor.text;
    for (int i = 0; i < mainData.length; i++) {
      var idx = mainData[i];
      if (idx['id'] == selectElement['id']) {
        setState(() {
          mainData[i] = selectElement;
        });
        break;
      }
    }
  }

  onDiscard() {
    for (int i = 0; i < mainData.length; i++) {
      mainData[i]['eSelect'] = false;
    }
    setState(() {
      selectElement = null;
    });
  }

  Widget buildComponent(Map component) {
    log('text' + component.toString());
    IconData tileIcon = Icons.text_fields;
    if (component['eId'] == 'text') {
      tileIcon = Icons.text_fields;
    } else if (component['eId'] == 'input') {
      tileIcon = Icons.input;
    } else if (component['eId'] == 'button') {
      tileIcon = Icons.smart_button;
    } else if (component['eId'] == 'input') {
      tileIcon = Icons.input;
    } else if (component['eId'] == 'checkbox') {
      tileIcon = Icons.check_box;
    } else if (component['eId'] == 'dropdown') {
      tileIcon = Icons.arrow_drop_down_circle_outlined;
    } else if (component['eId'] == 'toggle') {
      tileIcon = Icons.toggle_off_outlined;
    } else if (component['eId'] == 'progressbar') {
      tileIcon = Icons.upload_outlined;
    }

    return Card(
      child: Container(
        constraints: BoxConstraints(
          minWidth: 200,
          maxWidth: 200,
        ),
        child: ListTile(
          leading: Icon(
            tileIcon,
          ),
          title: Text(component['label']),
        ),
      ),
    );
  }

  List<Widget> vesselViewer() {
    List<Widget> list = [];

    for (int i = 0; i < mainData.length; i++) {
      list.add(Vessel(data: mainData[i]));
    }
    return list;
  }

  Map selectElement;
  void onTapVessel(int idx) {
    for (int i = 0; i < mainData.length; i++) {
      mainData[i]['eSelect'] = false;
    }
    Timer(Duration(milliseconds: 400), () {
      setState(() {
        selectElement = mainData[idx];
        mainData[idx]['eSelect'] = true;
        _labelEditor.text = selectElement['label'];
      });
    });
  }

  List<Widget> vesselEditor() {
    List<Widget> list = [];

    for (int i = 0; i < mainData.length; i++) {
      list.add(InkWell(
        onTap: () {
          log('clicked');
          onTapVessel(i);
        },
        child: IgnorePointer(
          ignoring: true,
          child: VesselEditor(
            data: mainData[i],
          ),
        ),
      ));
    }
    return list;
  }
}

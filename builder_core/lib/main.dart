import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:hovering/hovering.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Ether v1.0.0'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String? title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title!),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Container(
              height: 600,
              // padding: EdgeInsets.all(10),
              child: Row(
                children: [
                  Flexible(
                    flex: 1,
                    child: Container(
                      // color: Colors.green,
                      child: Column(
                        children: [
                          HoverCrossFadeWidget(
                            duration: Duration(milliseconds: 200),
                            firstChild: ListTile(
                              title: Text('Input field'),
                              leading: Icon(
                                Icons.input,
                              ),
                            ),
                            secondChild: Container(
                              color: Colors.grey[300],
                              child: ListTile(
                                title: Text('Input field'),
                                leading: Icon(
                                  Icons.input,
                                ),
                              ),
                            ),
                          ),
                          HoverCrossFadeWidget(
                            duration: Duration(milliseconds: 200),
                            firstChild: ListTile(
                              title: Text('Text'),
                              leading: Icon(
                                Icons.text_fields,
                              ),
                            ),
                            secondChild: Container(
                              color: Colors.grey[300],
                              child: ListTile(
                                title: Text('Text'),
                                leading: Icon(
                                  Icons.text_fields,
                                ),
                              ),
                            ),
                          ),
                          HoverCrossFadeWidget(
                            duration: Duration(milliseconds: 200),
                            firstChild: ListTile(
                              title: Text('Button'),
                              leading: Icon(
                                Icons.smart_button,
                              ),
                            ),
                            secondChild: Container(
                              color: Colors.grey[300],
                              child: ListTile(
                                title: Text('Button'),
                                leading: Icon(
                                  Icons.smart_button,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  Flexible(
                    flex: 4,
                    child: Container(
                      color: Colors.blue,
                    ),
                  ),
                  Flexible(
                    flex: 1,
                    child: Container(
                      color: Colors.red,
                    ),
                  ),
                ],
              ),
            ),
            Container(
              height: 200,
            )
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: Icon(Icons.add),
      ),
    );
  }
}

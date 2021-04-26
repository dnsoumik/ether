import 'package:ether/create/create_form.dart';
import 'package:ether/submit/submit_list.dart';
import 'package:ether/submit/submit_list_2.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class EtherHome extends StatefulWidget {
  @override
  _EtherHomeState createState() => _EtherHomeState();
}

class _EtherHomeState extends State<EtherHome> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Ether v1.0.0 build 3'),
      ),
      body: Container(
        width: MediaQuery.of(context).size.width,
        padding: EdgeInsets.only(
          top: 60,
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          mainAxisAlignment: MainAxisAlignment.center,
          // crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Card(
              elevation: 5,
              child: InkWell(
                onTap: () {
                  Navigator.of(context).push(
                      MaterialPageRoute(builder: (context) => EtherBuilder())
                  );
                },
                child: Container(
                  width: 380,
                  padding: EdgeInsets.only(
                    left: 20,
                    right: 20,
                    top: 10,
                    bottom: 10,
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      SvgPicture.asset('assets/1.svg',
                          height: 140,
                          semanticsLabel: 'Acme Logo',
                      ),
                      SizedBox(
                        width: 10,
                      ),
                      Flexible(
                        child: Text(
                          'Create new Form',
                          style: TextStyle(
                            fontSize: 20,
                            color: Colors.blue[900],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            SizedBox(
              width: 10,
            ),
            Card(
              elevation: 5,
              child: InkWell(
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(builder: (context) => EtherFormsList())
                  );
                },
                child: Container(
                  width: 380,
                  padding: EdgeInsets.only(
                    left: 20,
                    right: 20,
                    top: 10,
                    bottom: 10,
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      SvgPicture.asset(
                          'assets/svg/5.svg',
                          height: 140,
                          semanticsLabel: 'Acme Logo',
                      ),
                      Flexible(
                        child: Text(
                          'Submit Form',
                          style: TextStyle(
                            fontSize: 20,
                            color: Colors.blue[900],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            SizedBox(
              width: 10,
            ),
            Card(
              elevation: 5,
              child: InkWell(
                onTap: () {
                  Navigator.of(context).push(
                      MaterialPageRoute(builder: (context) => EtherFormsList_2())
                  );
                },
                child: Container(
                  width: 380,
                  padding: EdgeInsets.only(
                    left: 20,
                    right: 20,
                    top: 10,
                    bottom: 10,
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      SvgPicture.asset(
                        'assets/svg/4.svg',
                        height: 140,
                        semanticsLabel: 'Acme Logo',
                      ),
                      SizedBox(
                        width: 10,
                      ),
                      Flexible(
                        child: Text(
                          'View Form Data',
                          style: TextStyle(
                            fontSize: 20,
                            color: Colors.blue[900],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

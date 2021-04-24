

import 'package:dio/dio.dart';
import 'package:ether/handler/static_memory.dart';
import 'package:ether/util/log_util.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class EtherFormsList extends StatefulWidget {
  @override
  _EtherFormsListState createState() => _EtherFormsListState();
}

class _EtherFormsListState extends State<EtherFormsList> {

  Dio dio;
  BuildContext _context;

  _EtherFormsListState() {
    var options = BaseOptions(
      baseUrl: BuildConfig.serverUrl,
      connectTimeout: 5000,
      receiveTimeout: 5000,
    );
    dio = Dio(options);
  }

  @override
  Widget build(BuildContext context) {

    if (_context == null) {
      _context = context;
      getFormList();
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('Forms List'),
        actions: [
          IconButton(
              icon: Icon(
                  Icons.refresh
              ), onPressed: getFormList,
          )
        ],
      ),
      body: Container(
        width: MediaQuery.of(context).size.width,
        child: (forms.length > 0)? Column(
          children: [],
        ): Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            SvgPicture.asset('assets/svg/3.svg',
              height: 100,
              semanticsLabel: 'Acme Logo',
            ),
            SizedBox(
              height: 20,
            ),
            Text(
                'No forms found.',
              style: TextStyle(
                fontSize: 18,
                color: Colors.blue[800],
                fontStyle: FontStyle.italic,
              ),
            )
          ],
        ),
      ),
    );
  }

  List<Map> forms = [];
  getFormList() async {
    var response = await dio.get('/forms', queryParameters: {});
    try {
      Log.i(response);
    } catch (e, s) {
      Log.e(e, s);
    }
  }


}

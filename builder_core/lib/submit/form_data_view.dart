

import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:ether/handler/static_memory.dart';
import 'package:ether/util/log_util.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class FormDataViewer extends StatefulWidget {

  Map formDataConf;
  FormDataViewer(this.formDataConf);

  @override
  _FormDataViewerState createState() => _FormDataViewerState();
}

class _FormDataViewerState extends State<FormDataViewer> {

  Dio dio;
  BuildContext _context;

  _FormDataViewerState() {
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
        title: Text('Select your form'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: getFormList,
          )
        ],
      ),
      body: Container(
        width: MediaQuery.of(context).size.width,
        child: (forms.length > 0)
            ? SingleChildScrollView(
          child: Column(
            children: getFormsList(),
          ),
        )
            : Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            SvgPicture.asset(
              'assets/svg/6.svg',
              height: 200,
              semanticsLabel: 'Acme Logo',
            ),
            SizedBox(
              height: 20,
            ),
            Text(
              'No records found.',
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
    forms = [];
    var response = await dio.get('/forms_data', queryParameters: {
      'id': widget.formDataConf['_id']['\$oid']
    });
    try {
      // forms = response.data['result'];
      for (int i = 0; i < response.data['result'].length; i++) {
        // Log.i(response.data['result'][i].runtimeType);
        Map v = json.decode(response.data['result'][i]);
        // Log.i(v);
        forms.add(v);
      }
      Log.i(forms.length);
      setState(() {});
    } catch (e, s) {
      Log.e(e, s);
    }
  }


  List<Widget> getFormsList() {
    List<Widget> comps = [];

    for (int i = 0; i < forms.length; i++) {
      // Log.i('form list', forms[i]['metaData']);
      comps.add(
        Card(
          child: InkWell(
            onTap: () {
              // Navigator.of(context).push(
              //     MaterialPageRoute(builder: (context) => FormSubmit(forms[i]))
              // );
            },
            child: Container(
              padding: EdgeInsets.only(
                top: 10,
                left: 10,
                right: 10,
                bottom: 20,
              ),
              width: MediaQuery.of(context).size.width,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'No.' + (i+1).toString(),
                    style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold
                    ),
                    textAlign: TextAlign.center,
                  ),
                  // SvgPicture.asset(
                  //   'assets/svg/7.svg',
                  //   height: 80,
                  //   semanticsLabel: 'Acme Logo',
                  // ),
                  Container(
                    padding: EdgeInsets.only(
                      left: 10
                    ),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: getColumnList(forms[i]),
                    ),
                  )
                ],
              ),
            ),
          ),
        ),
      );
    }
    return comps;
  }

  List<Widget> getColumnList(dynamic colData) {

    List<Widget> cols = [];

    Log.i('column_data', colData['columnData'].length);
    var clD = colData['columnData'];
    for (int i = 0; i < clD.length; i++) {
      var v = clD[i];
      cols.add(
        Container(
          padding: EdgeInsets.only(
            bottom: 5,
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                  v['label'] + ' :',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(
                width: 10,
              ),
              Text(v['value'])
            ],
          ),
        )
      );
    }

    return cols;
  }


}

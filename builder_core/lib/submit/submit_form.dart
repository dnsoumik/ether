

import 'dart:async';
import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:ether/handler/static_memory.dart';
import 'package:ether/util/log_util.dart';
import 'package:ether/util/toast_util.dart';
import 'package:ether/vessels/vessel.dart';
import 'package:flutter/material.dart';

class FormSubmit extends StatefulWidget {

  Map formBuildConfig;
  FormSubmit(this.formBuildConfig);

  @override
  _FormSubmitState createState() => _FormSubmitState();
}

class _FormSubmitState extends State<FormSubmit> {

  List<Map> metaData = [];
  BuildContext _context;
  Dio dio;

  _FormSubmitState() {
    var options = BaseOptions(
      baseUrl: BuildConfig.serverUrl,
      connectTimeout: 5000,
      receiveTimeout: 5000,
    );
    dio = Dio(options);
  }


  @override
  void initState() {
    super.initState();
    try {
      for (int i = 0; i < widget.formBuildConfig['metaData'].length; i++) {
        Map v = widget.formBuildConfig['metaData'][i];
        // metaData.add();
        metaData.add(v);
        // Log.i(v);
      }
    } catch (e, s) {
      Log.e(e, s);
    }
  }

  @override
  Widget build(BuildContext context) {

    if (_context == null) {
      _context = context;
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(
          widget.formBuildConfig['formTitle']
        ),
      ),
      body: Container(
        padding: EdgeInsets.only(
          top: 20,
          left: 20,
          right: 20,
          bottom: 20,
        ),
        child: Column(
          children: [
            Column(
              children: vesselViewer(),
            ),
            Container(
              margin: EdgeInsets.only(
                  top: 20
              ),
              child: ElevatedButton(
                child: Container(
                  padding: EdgeInsets.only(
                    top: 8,
                    left: 20,
                    right: 20,
                    bottom: 8,
                  ),
                  child: Text(
                    'Submit',
                    style: TextStyle(
                      fontSize: 16,
                    ),
                  ),
                ),
                onPressed: () {
                  onSubmitData();
                },
              ),
            )
          ],
        ),
      ),
    );
  }

  List<Vessel> compsList = [];
  List<Vessel> vesselViewer() {
    compsList = [];
    for (int i = 0; i < metaData.length; i++) {
      compsList.add(
          Vessel(data: metaData[i]),
      );
    }
    return compsList;
  }

  void onSubmitData() async {

    Map formDt = {
      'formId': widget.formBuildConfig['_id'],
      'columnData': []
    };

    for (int i = 0; i < metaData.length; i++) {
      if (compsList[i].xController != null) {
        Log.i(compsList[i].xController.toString().length);
        try {
          if (compsList[i].xController.toString().length == 0) {
            Toaster.e(_context,
                message: 'Please enter ' + metaData[i]['label'].toString());
            return;
          } else {
            formDt['columnData'].add({
              'value': compsList[i].xController,
              'label': metaData[i]['label'],
              'id': metaData[i]['id'],
            });
          }
        } catch (e, s) {
          Log.e(e, s);
        }
      }
    }

    try {
      Log.i(json.encode(formDt));
    } catch (e, s) {
      Log.i();
    }

    var response = await dio.post(
      '/forms_data',
      data: json.encode(formDt),
    );
    try {
      Log.i(response);
      var rs = json.decode(response.data);
      if (rs['status']) {
        Toaster.s(_context, message: 'Form has been submitted');
        Timer(Duration(seconds: 1), () {
          Navigator.of(context).pop(true);
        });
      }
    } catch (e, s) {
      Log.e(e, s);
    }

  }

}

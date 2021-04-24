import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
// import 'package:fluttertoast/fluttertoast.dart';

class Toaster {
  static w({@required String message, bool shortLen=false}) {
    Toast toastLen = Toast.LENGTH_LONG;
    if (shortLen) {
      toastLen = Toast.LENGTH_SHORT;
    }
    Fluttertoast.showToast(
      msg: message,
      toastLength: toastLen,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.blueGrey,
        textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  static s({@required String message, bool shortLen=false}) {

    if (shortLen) {
      Fluttertoast.showToast(
        msg: message,
        toastLength: Toast.LENGTH_SHORT,
        gravity: ToastGravity.BOTTOM,
        timeInSecForIosWeb: 1,
        backgroundColor: Colors.green[500],
        textColor: Colors.white,
        fontSize: 16.0,
      );
    } else {
      Fluttertoast.showToast(
        msg: message,
        toastLength: Toast.LENGTH_LONG,
        gravity: ToastGravity.BOTTOM,
        timeInSecForIosWeb: 1,
        backgroundColor: Colors.green[500],
        textColor: Colors.white,
        fontSize: 16.0,
      );
    }
  }

  static e({@required String message, bool shortLen=false}) {
    Toast toastLen = Toast.LENGTH_LONG;
    if (shortLen) {
      toastLen = Toast.LENGTH_SHORT;
    }
    Fluttertoast.showToast(
      msg: message,
      toastLength: toastLen,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.redAccent,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  static i({@required String message, bool shortLen=false}) {
    Toast toastLen = Toast.LENGTH_LONG;
    if (shortLen) {
      toastLen = Toast.LENGTH_SHORT;
    }
    Fluttertoast.showToast(
      msg: message,
      toastLength: toastLen,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.blueAccent,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }

  static d({@required String message, bool shortLen=false}) {
    Toast toastLen = Toast.LENGTH_LONG;
    if (shortLen) {
      toastLen = Toast.LENGTH_SHORT;
    }
    Fluttertoast.showToast(
      msg: message,
      toastLength: toastLen,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.white,
      textColor: Colors.black,
      fontSize: 16.0,
    );
  }

  static r({@required String message, bool shortLen=false}) {
    Toast toastLen = Toast.LENGTH_LONG;
    if (shortLen) {
      toastLen = Toast.LENGTH_SHORT;
    }
    Fluttertoast.showToast(
      msg: message,
      toastLength: toastLen,
      gravity: ToastGravity.BOTTOM,
      timeInSecForIosWeb: 1,
      backgroundColor: Colors.black,
      textColor: Colors.white,
      fontSize: 16.0,
    );
  }
}

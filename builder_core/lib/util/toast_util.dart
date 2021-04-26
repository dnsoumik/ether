import 'package:ether/util/log_util.dart';
import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
// import 'package:fluttertoast/fluttertoast.dart';

class Toaster {

  static w(BuildContext _context, {@required String message, bool shortLen=false}) {
    int toastLen = 2;
    if (shortLen) {
      toastLen = 1;
    }

    if (_context == null) {
      return;
    }

    FlutterToast flutterToast = FlutterToast(_context);
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.blueGrey,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icon(Icons.check),
          SizedBox(
            width: 12.0,
          ),
          Text(
            message,
            style: TextStyle(
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
    flutterToast.showToast(
      child: toast,
      gravity: ToastGravity.BOTTOM,
      toastDuration: Duration(seconds: toastLen),
    );
  }

  static s(BuildContext _context, {@required String message, bool shortLen=false}) {
    int toastLen = 2;
    if (shortLen) {
      toastLen = 1;
    }

    if (_context == null) {
      return;
    }

    FlutterToast flutterToast = FlutterToast(_context);
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.green,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icon(Icons.check),
          SizedBox(
            width: 12.0,
          ),
          Text(
            message,
            style: TextStyle(
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
    flutterToast.showToast(
      child: toast,
      gravity: ToastGravity.BOTTOM,
      toastDuration: Duration(seconds: toastLen),
    );
  }

  static e(BuildContext _context, {@required String message, bool shortLen=false}) {
    int toastLen = 2;
    if (shortLen) {
      toastLen = 1;
    }

    if (_context == null) {
      return;
    }

    FlutterToast flutterToast = FlutterToast(_context);
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.redAccent,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icon(Icons.check),
          SizedBox(
            width: 12.0,
          ),
          Text(
            message,
            style: TextStyle(
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
    flutterToast.showToast(
      child: toast,
      gravity: ToastGravity.BOTTOM,
      toastDuration: Duration(seconds: toastLen),
    );
  }

  static i(BuildContext _context, {@required String message, bool shortLen=false}) {
    int toastLen = 2;
    if (shortLen) {
      toastLen = 1;
    }

    if (_context == null) {
      return;
    }

    FlutterToast flutterToast = FlutterToast(_context);
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.blueAccent,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icon(Icons.check),
          SizedBox(
            width: 12.0,
          ),
          Text(
            message,
            style: TextStyle(
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
    flutterToast.showToast(
      child: toast,
      gravity: ToastGravity.BOTTOM,
      toastDuration: Duration(seconds: toastLen),
    );
  }

  static d(BuildContext _context, {@required String message, bool shortLen=false}) {
    int toastLen = 2;
    if (shortLen) {
      toastLen = 1;
    }

    if (_context == null) {
      return;
    }

    FlutterToast flutterToast = FlutterToast(_context);
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.white,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icon(Icons.check),
          SizedBox(
            width: 12.0,
          ),
          Text(
            message,
            style: TextStyle(
              color: Colors.black,
            ),
          ),
        ],
      ),
    );
    flutterToast.showToast(
      child: toast,
      gravity: ToastGravity.BOTTOM,
      toastDuration: Duration(seconds: toastLen),
    );
  }

  static r(BuildContext _context, {@required String message, bool shortLen=false}) {
    int toastLen = 2;
    if (shortLen) {
      toastLen = 1;
    }

    if (_context == null) {
      return;
    }

    FlutterToast flutterToast = FlutterToast(_context);
    Widget toast = Container(
      padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(25.0),
        color: Colors.black,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icon(Icons.check),
          SizedBox(
            width: 12.0,
          ),
          Text(
            message,
            style: TextStyle(
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
    flutterToast.showToast(
      child: toast,
      gravity: ToastGravity.BOTTOM,
      toastDuration: Duration(seconds: toastLen),
    );
  }

}

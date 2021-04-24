import 'dart:async';
import 'dart:convert';
import 'dart:developer';

import 'package:ether/compute.dart';
import 'package:ether/home/home.dart';
import 'package:ether/vessels/vessel.dart';
import 'package:ether/vessels/vessel_editor.dart';
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
        body: EtherHome(),
      ),
    );
  }
}
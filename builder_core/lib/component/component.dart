import 'dart:convert';

class Components {
  List<Basic> basic;

  Components({this.basic});

  Components.fromJson(Map<String, dynamic> json) {
    if (json['basic'] != null) {
      basic = new List<Basic>();
      json['basic'].forEach((v) {
        basic.add(new Basic.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    if (this.basic != null) {
      data['basic'] = this.basic.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Basic {
  String id;
  String label;
  String icon;
  bool eSelect;
  String eId;
  List<Children> children;

  Basic(
      {this.id, this.label, this.icon, this.eSelect, this.eId, this.children});

  Basic.fromJson(Map<String, dynamic> json) {
    id = json['id'];
    label = json['label'];
    icon = json['icon'];
    eSelect = json['eSelect'];
    eId = json['eId'];
    if (json['children'] != null) {
      children = new List<Children>();
      json['children'].forEach((v) {
        children.add(new Children.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['id'] = this.id;
    data['label'] = this.label;
    data['icon'] = this.icon;
    data['eSelect'] = this.eSelect;
    data['eId'] = this.eId;
    if (this.children != null) {
      data['children'] = this.children.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Children {
  String text;
  String valueType;
  int value;

  Children({this.text, this.valueType, this.value});

  Children.fromJson(Map<String, dynamic> json) {
    text = json['text'];
    valueType = json['valueType'];
    value = json['value'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['text'] = this.text;
    data['valueType'] = this.valueType;
    data['value'] = this.value;
    return data;
  }
}
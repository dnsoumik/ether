
import 'package:uuid/uuid.dart';

class Compute {

  static int _salt = 0;
  static getUniqueKey() {
    // var uuid = Uuid();
    // return uuid.v1();
    return (_salt++).toString();
  }

}
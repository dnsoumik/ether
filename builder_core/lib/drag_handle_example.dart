import 'package:drag_and_drop_lists/drag_and_drop_lists.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';

class DragHandleExample extends StatefulWidget {
  DragHandleExample({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _DragHandleExample createState() => _DragHandleExample();
}

class _DragHandleExample extends State<DragHandleExample> {
  List<DragAndDropList> _contents = [];

  @override
  void initState() {
    super.initState();

    _contents = List.generate(4, (index) {
      return DragAndDropList(
        header: Container(),
        children: <DragAndDropItem>[
          DragAndDropItem(
            child: Row(
              children: [
                Padding(
                  padding: EdgeInsets.symmetric(vertical: 8, horizontal: 12),
                  child: Text(
                    'Sub $index.1',
                  ),
                ),
              ],
            ),
          ),
        ],
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    var backgroundColor = Color.fromARGB(255, 243, 242, 248);

    return Scaffold(
      backgroundColor: backgroundColor,
      appBar: AppBar(
        title: Text('Drag Handle'),
      ),
      body: DragAndDropLists(
        children: _contents,
        onItemReorder: _onItemReorder,
        onListReorder: _onListReorder,
        listPadding: EdgeInsets.symmetric(horizontal: 15, vertical: 10),
        itemDivider: Divider(
          thickness: 2,
          height: 2,
          color: backgroundColor,
        ),
        itemDecorationWhileDragging: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5),
              spreadRadius: 2,
              blurRadius: 3,
              offset: Offset(0, 0), // changes position of shadow
            ),
          ],
        ),
        listInnerDecoration: BoxDecoration(
          color: Theme.of(context).canvasColor,
          borderRadius: BorderRadius.all(Radius.circular(8.0)),
        ),
        lastItemTargetHeight: 8,
        addLastItemTargetHeightToTop: true,
        lastListTargetSize: 40,
        itemDragHandle: DragHandle(
          child: Padding(
            padding: EdgeInsets.only(right: 10),
            child: Icon(
              Icons.crop,
              color: Colors.black26,
            ),
          ),
        ),
      ),
    );
  }

  _onItemReorder(
      int oldItemIndex, int oldListIndex, int newItemIndex, int newListIndex) {
    setState(() {
      var movedItem = _contents[oldListIndex].children.removeAt(oldItemIndex);
      _contents[newListIndex].children.insert(newItemIndex, movedItem);
    });
  }

  _onListReorder(int oldListIndex, int newListIndex) {
    setState(() {
      var movedList = _contents.removeAt(oldListIndex);
      _contents.insert(newListIndex, movedList);
    });
  }
}

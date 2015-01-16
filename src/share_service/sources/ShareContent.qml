import QtQuick 2.1
import Deepin.Widgets 1.0

Item {
	width: 300
	height: 300

	TextEdit {
	    width: parent.width
	    height: 30
	    text: "在此输入想说的话．．．"
	    color: "grey"
	    wrapMode:TextEdit.Wrap

	    anchors.horizontalCenter: parent.horizontalCenter
	}

	DSeparatorHorizontal {
		width: parent.width
	}

	Rectangle {
	    x: parent.x + 20
	    y: parent.y + 45
	    width: 100
	    height: 100
	    border.width:2
	    border.color: "white"
	}

	DSeparatorHorizontal {
		width: parent.width
	}
}
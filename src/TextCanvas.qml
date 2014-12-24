import QtQuick 2.1

Rectangle {
	x: parent.curX
	y: parent.curY
	width: Math.max(5,text.contentWidth)
	height: Math.max(10,text.contentHeight)
	border.width: 2
	border.color: "white"
    function draw(ctx) {
    
    
    }
    
    TextEdit {
    	id:text
    	anchors.fill: parent
    }



}

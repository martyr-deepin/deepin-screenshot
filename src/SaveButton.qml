import QtQuick 2.1

Item {
    id: toolButton
    property string imageName: ""
    
    width: 43
    height: 32
    
    property bool clicked: false
    property alias selectArea: selectArea
    
    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 35
        height: 20
        radius: 2
        visible: false
        
        color: "white"
        opacity: 0.2
    }
    
    Row {
        anchors.centerIn: parent
        
        Image {
            source: "../image/action/save.png"
        }
        
        Image {
            source: "../image/action/list.png"
        }
    }
    
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        
        onEntered: {
            selectArea.visible = true
        }
        
        onExited: {
            selectArea.visible = false
        }
    }
}

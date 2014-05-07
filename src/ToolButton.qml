import QtQuick 2.1

Item {
    id: toolButton
    property string imageName: ""
    
    width: 32
    height: 32
    
    property bool clicked: false
    property alias selectArea: selectArea
    
    Rectangle {
        id: selectArea
        anchors.centerIn: parent
        width: 24
        height: 20
        radius: 2
        visible: false
        
        color: "white"
        opacity: 0.2
    }
    
    Image {
        id: toolImage
        source: "../image/action/" + toolButton.imageName + ".png"
        
        anchors.centerIn: parent
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

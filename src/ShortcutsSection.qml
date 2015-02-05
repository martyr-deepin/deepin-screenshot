import QtQuick 2.1

Column {
    id: column
    width: 300
    property alias title: t_title.text

    Text {
        id: t_title
        color: "white"
        text: column.title
        font.bold: true
        font.pixelSize: 18
    }

    Item { width: parent.width; height: 10 }
}
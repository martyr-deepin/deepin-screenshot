import QtQuick 2.0
import Deepin.Widgets 1.0

Rectangle {
    id: root
    radius: 3
    color: "transparent"
    border.width: 1
    border.color: borderColor

    property alias min: textInput.min
    property alias max: textInput.max
    property alias step: textInput.step
    property alias precision: textInput.precision
    property alias initValue: textInput.initValue
    property alias value: textInput.value
    property alias maximumLength: textInput.maximumLength

    property color warningColor: "#FF8F00"
    property color modifiedColor: "#505050"
    property color borderColor: Qt.rgba(1, 1, 1, 0.2)

    function reset() {
        textInput.text = initValue
        warning_label.visible = false
    }

    function increase(){
        if(value <= max - step){
            textInput.setValue(value + step)
        }
        else{
            textInput.setValue(max)
        }
    }

    function decrease(){
        if(value >= min + step){
            textInput.setValue(value - step)
        }
        else{
            textInput.setValue(min)
        }
    }

    TextInput {
        id: textInput

        font.pixelSize: 12
        color: "#b4b4b4"
        selectByMouse: true
        selectionColor: "#01bdff"
        validator: RegExpValidator { regExp: /^-?([0-9]|\.)*$/ }

        anchors.fill: parent
        anchors.margins: 3

        property int min: 0
        property int max: 65535
        property int step: 1
        property int precision: 0

        property int initValue:0
        property int value

        Component.onCompleted: {
            if (textInput.text == ""){
                textInput.text = initValue.toFixed(precision)
            } else if (textInput._validate()) {
                value = parseFloat(textInput.text)
                initValue = value
            } else {
                initValue = min
                textInput.text = initValue.toFixed(precision)
            }
        }

        function setValue(i){
            textInput.value = i
            textInput.text = i.toFixed(precision)
        }

        function _validate() {
            var value =  parseFloat(textInput.text)
            return min <= value && value <= max
        }

        Connections{
            target: textInput

            onTextChanged: check_valid_timer.restart()

            onActiveFocusChanged: {
                if (!textInput.activeFocus) {
                    if (!textInput._validate()) {
                        reset()
                    } else {
                        textInput.initValue = value
                        warning_label.visible = false
                    }
                }
            }
        }

        Timer {
            id: check_valid_timer
            interval: 300

            onTriggered: {
                if (textInput._validate()) {
                    if (warning_label.visible) {
                        warning_label.color = modifiedColor
                    }

                    var textValue = parseFloat(textInput.text)
                    textInput.value = textValue.toFixed(textInput.precision)
                } else  {
                    warning_label.color = warningColor
                    warning_label.visible = true
                }
            }
        }

        Timer {
            id: holdTimer
            repeat: true
            interval: 50
            property bool isIncrease: true
            onTriggered: {
                if(isIncrease){
                    increase()
                }
                else{
                    decrease()
                }
            }
        }

        Text {
            id: warning_label
            visible: false
            font.pixelSize: 12
            text: "%1-%2".arg(min).arg(max)

            anchors.right: parent.right
            anchors.rightMargin: buttonBox.width + 5
            anchors.verticalCenter: parent.verticalCenter
        }

        Row {
            id: buttonBox
            height: parent.height
            anchors.right: parent.right
            anchors.rightMargin: -textInput.anchors.margins

            IncDecButton {
                id: increaseButton

                type: "+"
                anchors.verticalCenter: parent.verticalCenter

                onClicked: increase()
                onPressAndHold: {
                    holdTimer.isIncrease = true
                    holdTimer.restart()
                }
                onReleased: {
                    holdTimer.stop()
                }
            }

            IncDecButton{
                id: decreaseButton
                type: "-"
                anchors.verticalCenter: parent.verticalCenter

                onClicked: decrease()
                onPressAndHold: {
                    holdTimer.isIncrease = false
                    holdTimer.restart()
                }
                onReleased: {
                    holdTimer.stop()
                }
            }
        }
    }
}
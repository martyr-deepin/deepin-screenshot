import QtQuick 2.1
import Deepin.Widgets 1.0

Item {
    id: root
    width: 300
    height: 40
    state: "first_time"

    property alias wordCount: word_number_label.text

    signal nextButtonClicked()
    signal shareButtonClicked()
    signal okButtonClicked()

    states: [
        State {
            name: "first_time"

            PropertyChanges { target: row; visible: false }
            PropertyChanges { target: plz_choose_sns_label; visible: false }
            PropertyChanges { target: accounts_management_label; visible: false }
            PropertyChanges { target: word_number_label; visible: true }
            PropertyChanges { target: next_button; visible: true }
            PropertyChanges { target: share_button; visible: false }
            PropertyChanges { target: ok_button; visible: false }
        },
        State {
            name: "accounts_list"

            PropertyChanges { target: row; visible: false }
            PropertyChanges { target: plz_choose_sns_label; visible: true }
            PropertyChanges { target: accounts_management_label; visible: false }
            PropertyChanges { target: word_number_label; visible: false }
            PropertyChanges { target: next_button; visible: false }
            PropertyChanges { target: share_button; visible: true }
            PropertyChanges { target: ok_button; visible: false }
        },
        State {
            name: "share"

            PropertyChanges { target: row; visible: true }
            PropertyChanges { target: plz_choose_sns_label; visible: false }
            PropertyChanges { target: accounts_management_label; visible: false }
            PropertyChanges { target: word_number_label; visible: true }
            PropertyChanges { target: next_button; visible: false }
            PropertyChanges { target: share_button; visible: true }
            PropertyChanges { target: ok_button; visible: false }
        },
        State {
            name: "accounts_manage"

            PropertyChanges { target: row; visible: false }
            PropertyChanges { target: plz_choose_sns_label; visible: false }
            PropertyChanges { target: accounts_management_label; visible: true }
            PropertyChanges { target: word_number_label; visible: false }
            PropertyChanges { target: next_button; visible: false }
            PropertyChanges { target: share_button; visible: false }
            PropertyChanges { target: ok_button; visible: true }
        }
    ]

    // this function takes a list as its parameter which determines which
    // account will be shown on the interface.
    // for example: [1, 0] will show SinaWeibo and hide Twitter
    function lightUpIcons(filterMap) {
        sinaweibo_checkbox.visible = filterMap[0]
        filterMap.forEach(function (mapItem) {
            if (mapItem) state = "share"
        })
    }

    function getEnabledAccounts() {
        var result = []
        if (sinaweibo_checkbox.checked) result.push("sinaweibo")
        if (twitter_checkbox.checked) result.push("twitter")
        return result
    }

    Row {
        id: row
        height: parent.height
        spacing: 10

        anchors.left: parent.left
        anchors.leftMargin: 5

        DImageCheckBox {
            id: sinaweibo_checkbox
            visible: false
            imageSource :"../images/sinaweibo_small.png"

            anchors.verticalCenter: parent.verticalCenter
        }

        DImageCheckBox {
            id: twitter_checkbox
            visible: false
            imageSource :"../images/twitter_small.png"

            anchors.verticalCenter: parent.verticalCenter
        }
    }

    Text {
        id: plz_choose_sns_label
        text: "Please choose platforms"
        color: "#FDA825"
        font.pixelSize: 11
        visible: false

        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        id: accounts_management_label
        text: "Accounts management"
        color: "#FDA825"
        font.pixelSize: 11
        visible: false

        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
    }

    Text {
        id: word_number_label
        color: "#FDA825"
        font.pixelSize: 11

        anchors.right: next_button.left
        anchors.rightMargin: 10
        anchors.verticalCenter: parent.verticalCenter
    }

    DTextButton {
        id: next_button
        text: "Next"
        visible: false

        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter

        onClicked: root.nextButtonClicked()
    }

    DTextButton {
        id: share_button
        text: "Share"

        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter

        onClicked: root.shareButtonClicked()
    }

    DTextButton {
        id: ok_button
        text: "OK"
        visible: false

        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter

        onClicked: root.okButtonClicked()
    }
}
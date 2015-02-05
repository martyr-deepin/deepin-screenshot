import QtQuick 2.1
import QtGraphicalEffects 1.0
import Deepin.Widgets 1.0
import QtQuick.Window 2.1

DWindow {
    x: (Screen.desktopAvailableWidth - width) / 2
    y: (Screen.desktopAvailableHeight - height) / 2
    width: effect.width
    height: effect.height
    flags: Qt.Popup
    color: "transparent"
    shadowWidth: (width - content.width) / 2

    DRectangularGlow {
        id: effect
        glowRadius: 8.0
        spread: 0
        color: Qt.rgba(0, 0, 0, 0.6)

        anchors.fill: content
    }

    Rectangle {
        id: content
        width: 980
        height: 560
        radius: 3
        color: Qt.rgba(0, 0, 0, 0.8)
        border.width: 1
        border.color: Qt.rgba(1, 1, 1, 0.6)

        anchors.centerIn: parent

        Item {
            anchors.fill: parent
            anchors.margins: { 50, 50, 50, 50}

            Row {
                height: parent.height

                Column {
                    spacing: 30

                    ShortcutsSection {
                        title: dsTr("Launch/Screenshot")

                        ShortcutsLabel {
                            title: dsTr("Quick launch")
                            shortcut: "Ctrl+Alt+A"
                        }
                        ShortcutsLabel {
                            title: dsTr("Fullscreen screenshot")
                            shortcut: "Print"
                        }
                        ShortcutsLabel {
                            title: dsTr("Delay screenshot")
                            shortcut: "Ctrl+Print"
                        }
                        ShortcutsLabel {
                            title: dsTr("Smart window recognition")
                            shortcut: "Ctrl+Alt+Print"
                        }
                        ShortcutsLabel {
                            title: dsTr("Quit")
                            shortcut: "Esc"
                        }
                    }

                    ShortcutsSection {
                        title: dsTr("Save/Share")

                        ShortcutsLabel {
                            title: dsTr("Save")
                            shortcut: "Ctrl+S"
                        }
                        ShortcutsLabel {
                            title: dsTr("Share")
                            shortcut: "Ctrl+Enter"
                        }
                    }
                }

                Column {
                    ShortcutsSection {
                        title: dsTr("Painting")

                        ShortcutsLabel {
                            title: dsTr("Rectangle tool")
                            shortcut: "Alt+1"
                        }
                        ShortcutsLabel {
                            title: dsTr("Ellipse tool")
                            shortcut: "Alt+2"
                        }
                        ShortcutsLabel {
                            title: dsTr("Arrow tool")
                            shortcut: "Alt+3"
                        }
                        ShortcutsLabel {
                            title: dsTr("Pen tool")
                            shortcut: "Alt+4"
                        }
                        ShortcutsLabel {
                            title: dsTr("Text tool")
                            shortcut: "Alt+5"
                        }
                        ShortcutsLabel {
                            title: dsTr("Color tool")
                            shortcut: "Alt+6"
                        }

                    }
                }

                Column {
                    ShortcutsSection {
                        title: dsTr("Size adjust")

                        ShortcutsLabel {
                            title: dsTr("Expand selection top side")
                            shortcut: "Ctrl+Up"
                        }

                        ShortcutsLabel {
                            title: dsTr("Expand selection down side")
                            shortcut: "Ctrl+Down"
                        }

                        ShortcutsLabel {
                            title: dsTr("Expand selection left side")
                            shortcut: "Ctrl+Left"
                        }

                        ShortcutsLabel {
                            title: dsTr("Expand selection right side")
                            shortcut: "Ctrl+Right"
                        }
                    }
                }
            }
        }
    }
}
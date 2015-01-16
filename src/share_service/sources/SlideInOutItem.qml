import QtQuick 2.1

Item {
	id: rect
	width: 400
	height: 300

	Behavior on x {
		id: x_behavior
		NumberAnimation {
			duration: 500
			easing.type: Easing.OutCubic
		}
	}

	function leftIn() {
		x_behavior.enabled = false
		x = -width
		x_behavior.enabled = true
		x = 0
	}

	function leftOut() {
		x_behavior.enabled = false
		x = 0
		x_behavior.enabled = true
		x = -width
	}

	function rightIn() {
		x_behavior.enabled = false
		x = width
		x_behavior.enabled = true
		x = 0
	}

	function rightOut() {
		x_behavior.enabled = false
		x = 0
		x_behavior.enabled = true
		x = width
	}
}
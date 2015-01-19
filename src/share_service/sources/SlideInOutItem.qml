import QtQuick 2.1

Item {
	id: rect
	width: 400
	height: 300

	NumberAnimation {
		id: in_animation
		property: "x"
		target: rect
		duration: 500
		easing.type: Easing.OutCubic
		onStarted: rect.visible = true
	}

	NumberAnimation {
		id: out_animation
		property: "x"
		target: rect
		duration: 500
		easing.type: Easing.OutCubic
		onStopped: rect.visible = false
	}

	function leftIn() {
		rect.x = -width
		in_animation.to = 0
		in_animation.start()
	}

	function leftOut() {
		rect.x = 0
		out_animation.to = -width
		out_animation.start()
	}

	function rightIn() {
		rect.x = width
		in_animation.to = 0
		in_animation.start()
	}

	function rightOut() {
		rect.x = 0
		out_animation.to = width
		out_animation.start()
	}
}
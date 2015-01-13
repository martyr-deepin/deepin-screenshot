function isPointsSameX(points) {
	if (points.length < 2) {
		return true
	} else {
		for (var i = 1; i < points.length; i++) {
			if (points[i].x != points[0].x) {
				return false
			}
		}
		return true
	}
}

function isPointsSameY(points) {
	if (points.length < 2) {
		return true
	} else {
		for (var i = 1; i < points.length; i++) {
			if (points[i].y != points[0].y) {
				return false
			}
		}
		return true
	}
}
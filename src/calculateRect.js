// calculateRect.js

function swap(a,b) {
	var c = a
	a = b
	b = c
	return [a,b]
}
function square(p) {
    return ((p)*(p))
}

/* calculate the four points position */
function fourPoint_dir(point1, point2, point3, point4) {
	var points = [point1, point2, point3, point4]
	for (var i = 0; i < points.length; i++) {
		for (var j = i + 1; j < points.length; j++ ) {
			if (points[i].x > points[j].x) {
				var tmp = points[i].x
				points[i].x = points[j].x
				points[j].x = tmp
				tmp = points[i].y
				points[i].y = points[j].y
				points[j].y = tmp
			} else if(points[i].x == points[j].x) {
				if (points[i].y > points[j].y) {
				tmp = points[i].y
				points[i].y = points[j].y
				points[j].y = tmp
				}
			}
		}
	}
	return points
}
/* judge whether the point1 clicked on the point2 or not */
function pointClickIn(point2, point1) {
	if (point2.x >= point1.x -5 && point2.x <= point1.x + 5 &&
	point2.y >= point1.y - 5 && point2.y <= point1.y + 5) {
		return true
	} else {
		return false
	}
}
/* judge whether the point(point3) is on the line segment*/
function pointOnLine(point1, point2, point3) {
	if (point1.x == point2.x) {
		print("point3", point3)
		if (point3.x == point1.x && point3.y >= Math.min(point1.y, point2.y) && point3.y <= Math.max(point1.y, point2.y)) {
			return true
		} else { return false }
	} else {
		var k = (point1.y - point2.y) / (point1.x - point2.x)
		var b = point1.y - point1.x*k
		if (point3.y == k * point3.x + b && point3.y >= Math.min(point1.y, point2.y) && point3.y <= Math.max(point1.y, point2.y)) {
			return true
		} else {
			return false
		}
	}
}
/* the distance from a point(point3) to a line(point1, point2) */
function pointTolineDistance(point1, point2, point3) {
	if (point1.x == point2.x) {
		var distance = Math.abs(point3.x - point1.x)
	} else {
		var k = (point1.y - point2.y) / (point1.x - point2.x)
		var b = point1.y - point1.x*k
		var distance = Math.abs(point3.x * k + b - point3.y) / Math.sqrt(square(k) + 1)
	}
	return distance
}
/* get the point who splid a distance on a line */
function pointSplid(point1, point2, distance) {
	if (point1.x == point2.x) {
		var addx = 0
		var addy = distance
	} else {
		var k = (point1.y - point2.y) / (point1.x - point2.x)
		var b = point1.y - point1.x*k
		var addx = distance*Math.cos(Math.atan2(Math.abs(point1.y - point2.y), Math.abs(point1.x - point2.x)))
		var addy = distance*Math.sin(Math.atan2(Math.abs(point1.y - point2.y), Math.abs(point1.x - point2.x)))
	}
	var tmp = [addx, addy]
	return tmp
}
function resizePointOnClick(point1, point2, point3, point4, p) {
	if (p.x >= point1.x - 5 && p.x <= point1.y + 5 &&
	p.y >= point1.y - 5 && p.y <= point1.y + 5) {
		return 1
	}
	if (p.x >= point2.x - 5 && p.x <= point2.y + 5 &&
	p.y >= point2.y - 5 && p.y <= point2.y + 5) {
		return 2
	}
	if (p.x >= point3.x - 5 && p.x <= point3.y + 5 &&
	p.y >= point3.y - 5 && p.y <= point3.y + 5) {
		return 3
	}
	if (p.x >= point4.x - 5 && p.x <= point4.y + 5 &&
	p.y >= point4.y - 5 && p.y <= point4.y + 5) {
		return 4
	}
	return 0
}
/* judge the direction of point3 of line(point1, point2)*/
function pointLineDir(point1, point2, point3) {
	if (point1.x == point2.x) {
		if (point3.x <= point1.x) {
			return - 1
		} else {
			return  1
		}
	} else {
		var k = (point1.y - point2.y) / (point1.x - point2.x)
		var b = point1.y - point1.x*k
		if (point3.y > point3.x*k + b) {
			return - 1
		} else {
			return  1
		}
	}
}
/* point1 */
function pointResize1(point1, point2, point3, point4, p) {

	print("!", point1, point2, point3, point4)
	print("pointLineDir", pointLineDir(point1, point3, p), pointLineDir(point1, point2, p))
	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		print("*")
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)

		point2 = [point2.x - add[1], point2.y + add[0]]

		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = [point3.x - add[0], point3.y - add[1]]
	}
	if (pointDir(point2, point3, point1) == 1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x - add[0], point3.y - add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y + add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y + add[1])
	}
	print("!!!", point1, point2, point3, point4)
}
function pointResize2(point1, point2, point3, point4, p, clickedPoint) {

	if (pointDir(point2, point3, point1) == 1 && pointDir(point1, point2, point1) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y - add[1])
	}
	if (pointDir(point2, point3, point1) == 1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y - add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x - add[0], point3.y + add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y - add[1])
	}
}

function pointResize3(point1, point2, point3, point4, p, clickedPoint) {

	if (pointDir(point2, point3, point1) == 1 && pointDir(point1, point2, point1) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x - add[0], point3.y - add[1])
	}
	if (pointDir(point2, point3, point1) == 1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x - add[0], point3.y - add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y + add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y + add[1])
	}
}
function pointResize4(point1, point2, point3, point4, p, clickedPoint) {
	if (pointDir(point2, point3, point1) == 1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x - add[0], point3.y + add[1])
	}
	if (pointDir(point2, point3, point1) == 1 && pointDir(point1, point2, point1) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x - add[0], point3.y +add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y - add[1])
	}
	if (pointDir(point2, point3, point1) == -1 && pointDir(point1, point2, point1) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = (point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, piont4, distance)
		point3 = (point3.x + add[0], point3.y - add[1])
	}
}

function  pointDir(point1, point2, point3, point4) {
	if (point1.x - point2.x <= 0 && point1.y - point2.y <= 0 &&
	point1.x - point3.x >= 0 && point1.y - point3.y <= 0) {
		return 1
	}
	if (point1.x - point2.x >= 0 && point1.y - point2.y <=0 &&
	point1.x - point3.x <=0 && point1.y - point3.y <= 0) {
		return 2
	}
	if (point1.x - point2.x >= 0 && point1.y - point2.y <= 0 &&
	point1.x - point3.x <= 0 && point1.y - point3.y <= 0) {
		return 3
	}
	if (point1.x - point2.x <= 0 && point1.y - point2.y >= 0 &&
	point1.x - point3.x >= 0 && point1.y - point3.y >= 0) {
		return 4
	}
 }

/* the angle in point3 */
function calcutateAngle(point1, point2, point3) {

	var a = square(point1.x- point3.x) + square(point1.y - point3.y)
	var b = square(point2.x - point3.x) + square(point2.y - point3.y)
	var c = square(point1.x - point2.x) + square(point1.y - point2.y)

	var angle = Math.acos((a + b - c) / (2*Math.sqrt(a)*Math.sqrt(b)))
	return angle
}
/* point2 is the rotatePoint, point1 is the centerPoint, point3 is point2 who rotate */
function pointRotate(point1, point2, angele) {

	var middlePoint = Qt.point(point2.x - point1.x, point2.y - point1.y)
	var tmpPoint = Qt.point(middlePoint.x * Math.cos(angele) - middlePoint.y * Math.sin(angele), middlePoint.x * Math.sin(angele) + middlePoint.y * Math.cos(angele))
	var point3 = Qt.point(tmpPoint.x + point1.x, tmpPoint.y + point1.y)
	print("123",point1,point2,point3,angele)

	return point3
}
function getRotatePoint(point1, point2, point3, point4) {
	var d = 30
	/*   first position */
	if (point2.x - point4.x <= 0 && point2.y - point4.y >= 0 ) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point2.x + add[0], point2.y - add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point4.x + add[0], point4.y - add[1])
	}
	/* second position */
	if (point2.x - point4.x >= 0 && point2.y - point4.y <= 0) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point2.x + add[0], point2.y + add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point4.x + add[0], point4.y + add[1])
	}
	/* third position */
	if (point2.x - point4.x >= 0 && point2.y - point4.y >= 0) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point2.x - add[0], point2.y + add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point4.x - add[0], point4.y + add[1])
	}
	/* fourth position */
	if (point2.x - point4.x <= 0 && point2.y - point4.y <= 0) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point2.x - add[0], point2.y - add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point4.x - add[0], point4.y - add[1])
	}
	var rotatePoint = Qt.point((leftpoint.x + rightpoint.x) / 2, (leftpoint.y + rightpoint.y) / 2)
	return rotatePoint
}

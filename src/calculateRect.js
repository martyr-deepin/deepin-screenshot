/* calculateRect.js */

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
		if (point3.x >= point1.x - 5 && point3.x <= point1.x + 5 &&
		point3.y >= Math.min(point1.y, point2.y) - 5 && point3.y <= Math.max(point1.y, point2.y) + 5) {
			return true
		}
	} else {
		var k =  (point2.y - point1.y) / (point2.x - point1.x)
		var b = point1.y - point1.x*k

		if (point3.y >= k * point3.x + b - 5 && point3.y <= k * point3.x + b + 5) {
			return true
		}
	}
	return false
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
function resizePoint(point1, point2, point3, point4, p) {

	if (p.x >= point1.x - 5 && p.x <= point1.x + 5 &&
	p.y >= point1.y - 5 && p.y <= point1.y + 5) {
		return 1
	}
	if (p.x >= point2.x - 5 && p.x <= point2.x + 5 &&
	p.y >= point2.y - 5 && p.y <= point2.y + 5) {
		return 2
	}
	if (p.x >= point3.x - 5 && p.x <= point3.x + 5 &&
	p.y >= point3.y - 5 && p.y <= point3.y + 5) {
		return 3
	}
	if (p.x >= point4.x - 5 && p.x <= point4.x + 5 &&
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
		if (point3.y <= point3.x*k + b) {
			return  -1
		} else {
			return  1
		}
	}
}
function reSizePointPosititon(point1, point2, point3, point4, p, K) {
	var points = [point1, point2, point3, point4]
	switch (K) {
		case 1: {
			if (point1.x - point2.x <= 0 && point1.y - point2.y <= 0 &&
			point1.x - point3.x <= 0 && point1.y - point3.y >= 0) {
				points = point1Resize1(point1, point2, point3, point4, p)
				return points
			}
			if (point1.x - point2.x < 0 && point1.y - point2.y > 0 &&
			point1.x - point3.x > 0 && point1.y - point3.y > 0) {
				points = point1Resize2(point1, point2, point3, point4, p)
				return points
			}
			if (point1.x - point2.x > 0 && point1.y - point2.y < 0 &&
			point1.x - point3.x < 0 && point1.y - point3.y < 0) {
				points = point1Resize3(point1, point2, point3, point4, p)
				return points
			}
			if (point1.x - point2.x > 0 && point1.y - point2.y > 0 &&
			point1.x - point3.x > 0 && point1.y - point3.y < 0) {
				points = point1Resize4(point1, point2, point3, point4, p)
				return points
			}
			break
		}
		case 2: {
			if (point2.x - point1.x < 0 && point2.y - point1.y > 0 &&
			point2.x - point4.x < 0 && point2.y - point4.y < 0) {
				points = point2Resize1(point1, point2, point3, point4, p)
				return points
			}
			if (point2.x - point1.x >= 0 && point2.y - point1.y >= 0 &&
			point2.x - point4.x <= 0 && point2.y - point4.y >= 0) {
				points = point2Resize2(point1, point2, point3, point4, p)
				return points
			}
			if (point2.x - point1.x < 0 && point2.y - point1.y < 0 &&
			point2.x - point4.x > 0 && point2.y - point4.y < 0) {
				points = point2Resize3(point1, point2, point3, point4, p)
				return points
			}
			if (point2.x - point1.x > 0 && point2.y - point1.y < 0 &&
			point2.x - point4.x > 0 && point2.y - point4.y > 0) {
				points = point2Resize4(point1, point2, point3, point4, p)
				return points
			}
			break
		}
		case 3: {
			if (point3.x - point1.x < 0 && point3.y - point1.y < 0 &&
			point3.x - point4.x < 0 && point3.y - point4.y > 0) {
				points = point3Resize1(point1, point2, point3, point4, p)
				return points
			}
			if (point3.x - point1.x < 0 && point3.y - point1.y > 0 &&
			point3.x - point4.x > 0 && point3.y - point4.y > 0) {
				points = point3Resize2(point1, point2, point3, point4, p)
				return points
			}
			if (point3.x - point1.x >= 0 && point3.y - point1.y <= 0 &&
			point3.x - point4.x <= 0 && point3.y - point4.y <= 0) {
				points = point3Resize3(point1, point2, point3, point4, p)
				return points
			}
			if (point3.x - point1.x > 0 && point3.y - point1.y > 0 &&
			point3.x - point4.x > 0 && point3.y - point4.y < 0) {
				points = point3Resize4(point1, point2, point3, point4, p)
				return points
			}
			break
		}
		case 4: {
			if (point4.x - point2.x < 0 && point4.y - point2.y > 0 &&
			point4.x - point3.x < 0 && point4.y - point3.y < 0) {
				points = point4Resize1(point1, point2, point3, point4, p)
				return points
			}
			if (point4.x - point2.x > 0 && point4.y - point2.y > 0 &&
			point4.x - point3.x < 0 && point4.y - point3.y > 0) {
				points = point4Resize2(point1, point2, point3, point4, p)
				return points
			}
			if (point4.x - point2.x < 0 && point4.y - point2.y < 0 &&
			point4.x - point3.x > 0 && point4.y - point3.y < 0) {
				points = point4Resize3(point1, point2, point3, point4, p)
				return points
			}
			if (point4.x - point2.x >= 0 && point4.y - point2.y <= 0 &&
			point4.x - point3.x >= 0 && point4.y - point3.y >= 0) {
				points = point4Resize4(point1, point2, point3, point4, p)
				return points
			}
			break
		}
	}
}
/* first point1 */
/* point1 in the first position */
function point1Resize1(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [p, point2, point3, point4]
		return points
	}

	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	return points
}
/* point1 in the second position */
function point1Resize2(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}

	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x + add[0], point3.y - add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}
}
/* point1 in the third position */
function point1Resize3(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}

	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x + add[0], point3.y - add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}
}
/* point1 in the fourth position */
function point1Resize4(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}

	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == -1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [p, point2, point3, point4]
		return points
	}
	if (pointLineDir(point1, point3, p) == 1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point2, point4,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point3, point4, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [p, point2, point3, point4]
		return points
	}
}
/* point2 */
/* point2 in the first position */
function point2Resize1(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
}
/* point2 in the second position */
function point2Resize2(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point1, point2, p) == -1 && pointLineDir(point2, point4, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point1, point2, p) == 1 && pointLineDir(point2, point4, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point1, point2, p) == 1 && pointLineDir(point2, point4, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point1, point2, p) == -1 && pointLineDir(point2, point4, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
}
/* point2 in the third position */
function point2Resize3(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
}
/* point2 in the fourth position */
function point2Resize4(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point1, point2, p) == 1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		var points = [point1, p, point3, point4]
		return points
	}
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point1, point2, p) == -1) {
		var distance = pointTolineDistance(point1, point2, p)
		var add = pointSplid(point1, point3,distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		distance = pointTolineDistance(point2, point4, p)
		add = pointSplid(point3, point4, distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		var points = [point1, p, point3, point4]
		return points
	}
}
/* point3*/
/* point3 in the first position */
function point3Resize1(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == 1)  {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == 1)  {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
}
/* point3 in the second position */
function point3Resize2(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == 1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == 1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
}
/* point3 in the third position */
function point3Resize3(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == 1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == 1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
}
/* point3 in the fourth position */
function point3Resize4(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == 1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x + add[0], point4.y + add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == -1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x - add[0], point1.y + add[1])
		var points = [point1, point2, p, point4]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point1, point3, p) == 1) {
		var distance = pointTolineDistance(point3, point4, p)
		var add = pointSplid(point2, point4,distance)
		point4 = Qt.point(point4.x - add[0], point4.y - add[1])
		distance = pointTolineDistance(point1, point3, p)
		add = pointSplid(point1, point2, distance)
		point1 = Qt.point(point1.x + add[0], point1.y - add[1])
		var points = [point1, point2, p, point4]
		return points
	}
}
/* point4 */
/* point4 in the first position */
function point4Resize1(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point3, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point3, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y - add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point3, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point3, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
}
/* point4 in the second position */
function point4Resize2(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point3, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point3, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point3, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point3, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
}
/* point4 in the third position */
function point4Resize3(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point3, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == 1 && pointLineDir(point3, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point3, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y - add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point2, point4, p) == -1 && pointLineDir(point3, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
}
/* point4 in the fourth position */
function point4Resize4(point1, point2, point3, point4, p) {
	var points = [point1, point2, point3, point4]
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point2, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y - add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point2, point4, p) == 1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x + add[0], point2.y + add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point3, point4, p) == -1 && pointLineDir(point2, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x - add[0], point3.y + add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	if (pointLineDir(point3, point4, p) == 1 && pointLineDir(point2, point4, p) == -1) {
		var distance = pointTolineDistance(point2, point4, p)
		var add = pointSplid(point1, point2,distance)
		point2 = Qt.point(point2.x - add[0], point2.y - add[1])
		distance = pointTolineDistance(point3, point4, p)
		add = pointSplid(point1, point3, distance)
		point3 = Qt.point(point3.x + add[0], point3.y - add[1])
		var points = [point1, point2, point3, p]
		return points
	}
	return points
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

	return point3
}
function getRotatePoint(point1, point2, point3, point4) {
	var d = 30
	/*   first position */
	if (point2.x - point4.x <= 0 && point2.y - point4.y >= 0 ) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point1.x - add[0], point1.y - add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point3.x - add[0], point3.y - add[1])
	}
	/* second position */
	if (point2.x - point4.x >= 0 && point2.y - point4.y >= 0) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point1.x - add[0], point1.y + add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point3.x - add[0], point3.y + add[1])
	}
	/* third position */
	if (point2.x - point4.x <= 0 && point2.y - point4.y <= 0) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point1.x + add[0], point1.y - add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point3.x + add[0], point3.y - add[1])
	}
	/* fourth position */
	if (point2.x - point4.x >= 0 && point2.y - point4.y <= 0) {
		var add = pointSplid(point1, point2, d)
		var leftpoint = Qt.point(point1.x + add[0], point1.y + add[1])
		add = pointSplid(point3, point4, d)
		var rightpoint = Qt.point(point3.x + add[0], point3.y + add[1])
	}
	var rotatePoint = Qt.point((leftpoint.x + rightpoint.x) / 2, (leftpoint.y + rightpoint.y) / 2)
	return rotatePoint
}

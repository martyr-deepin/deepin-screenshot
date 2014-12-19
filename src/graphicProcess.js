/* the Image Processing Function*/
/* the GaussianBlur Function */
/* the Mosaic Processing Function*/
function gaussianBlur(imgData, amount) {

	var width = imgData.width;
	var width4 = width << 2;
	var height = imgData.height;
	var pixels = imgData;
	if (pixels) {
		var data = pixels.data;

		// compute coefficients as a function of amount
		var q;
		if (amount < 0.0) {
			amount = 0.0;
		}
		if (amount >= 2.5) {
			q = 0.98711 * amount - 0.96330;
		} else if (amount >= 0.5) {
			q = 3.97156 - 4.14554 * Math.sqrt(1.0 - 0.26891 * amount);
		} else {
			q = 2 * amount * (3.97156 - 4.14554 * Math.sqrt(1.0 - 0.26891 * 0.5));
		}

		//compute b0, b1, b2, and b3
		var qq = q * q;
		var qqq = qq * q;
		var b0 = 1.57825 + (2.44413 * q) + (1.4281 * qq ) + (0.422205 * qqq);
		var b1 = ((2.44413 * q) + (2.85619 * qq) + (1.26661 * qqq)) / b0;
		var b2 = (-((1.4281 * qq) + (1.26661 * qqq))) / b0;
		var b3 = (0.422205 * qqq) / b0;
		var bigB = 1.0 - (b1 + b2 + b3);


		// horizontal
		for (var c = 0; c <  5; c++) {
			for (var y = 0; y < height; y++) {
				// forward
				var index = y * width4 + c;
				var indexLast = y * width4 + ((width - 1) << 2) + c;
				var pixel = data[index];
				var ppixel = pixel;
				var pppixel = ppixel;
				var ppppixel = pppixel;
				// print("index, indexLast", index, indexLast)
				for (; index <= indexLast; index += 4) {
					pixel = bigB * data[index] + b1 * ppixel + b2 * pppixel + b3 * ppppixel;
					data[index] = pixel;
					ppppixel = pppixel;
					pppixel = ppixel;
					ppixel = pixel;
				}
				// backward
				index = y * width4 + ((width - 1) << 2) + c;
				indexLast = y * width4 + c;
				pixel = data[index];
				ppixel = pixel;
				pppixel = ppixel;
				ppppixel = pppixel;
				for (; index >= indexLast; index -= 4) {
					pixel = bigB * data[index] + b1 * ppixel + b2 * pppixel + b3 * ppppixel;
					data[index] = pixel;
					ppppixel = pppixel;
					pppixel = ppixel;
					ppixel = pixel;
					}
				}
			}

		// vertical
		for (var c = 0; c <  5; c++) {
			for (var x = 0; x < width; x++) {
				// forward
				var index = (x << 2) + c;
				var indexLast = (height - 1) * width4 + (x << 2) + c;
				var pixel = data[index];
				var ppixel = pixel;
				var pppixel = ppixel;
				var ppppixel = pppixel;
				for (; index <= indexLast; index += width4) {
					pixel = bigB * data[index] + b1 * ppixel + b2 * pppixel + b3 * ppppixel;
					data[index] = pixel;
					ppppixel = pppixel;
					pppixel = ppixel;
					ppixel = pixel;
				}
				// backward
				index = (height - 1) * width4 + (x << 2) + c;
				indexLast = (x << 2) + c;
				pixel = data[index];
				ppixel = pixel;
				pppixel = ppixel;
				ppppixel = pppixel;
				for (; index >= indexLast; index -= width4) {
					pixel = bigB * data[index] + b1 * ppixel + b2 * pppixel + b3 * ppppixel;
					data[index] = pixel;
					ppppixel = pppixel;
					pppixel = ppixel;
					ppixel = pixel;
				}
			}
		}
		return imgData;
	}
}

	function mosaic(imgData, radius) {

		var width = imgData.width;
		var height = imgData.height;
		var pixels = imgData;
		if (pixels) {
			var pixelArray = imgData.data
			for (var i = 0; i < height; i+= radius) {
				for (var j = 0; j < width; j+= radius) {
					var num = Math.random()
					var randomPixel = { x: Math.floor(num*radius + i), y: Math.floor(num*radius + j)}

					for(var k = j; k < j + radius; k++) {
						for (var l = i; l < i + radius; l++) {
							pixelArray[(l*width + k)*4] = pixelArray[(randomPixel.x*width + randomPixel.y)*4]
							pixelArray[(l*width + k)*4 + 1] = pixelArray[(randomPixel.x*width + randomPixel.y)*4 + 1]
							pixelArray[(l*width + k)*4 + 2] = pixelArray[(randomPixel.x*width + randomPixel.y)*4 + 2]
							pixelArray[(l*width + k)*4 + 3] = pixelArray[(randomPixel.x*width + randomPixel.y)*4 + 3]
						}
					}
				}
			}
			return imgData
		}
	}

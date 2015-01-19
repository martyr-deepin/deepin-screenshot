import QtQuick 2.2
import QtWebKit 3.0
import Deepin.Widgets 1.0

DWindow {
	id: root
    width: 800
    height: 500

    signal urlChanged(string url)

    function setUrl(url) { webview.url = url }

    WebView {
    	id: webview
    	anchors.fill: parent

	    onLoadingChanged: root.urlChanged(loadRequest.url)
    }
}
import QtQuick 2.2
import QtWebKit 3.0

WebView {
    id: webview
    width: 800
    height: 500

    signal urlChanged(url url)

    onLoadingChanged: urlChanged(loadRequest.url)

    function setUrl(url) { webview.url = url }
}
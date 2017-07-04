#include "tempfile.h"

#include <QTemporaryFile>
#include <QDebug>

TempFile* TempFile::m_tempFile = nullptr;
TempFile* TempFile::instance() {
    if (!m_tempFile) {
        m_tempFile = new TempFile();
    }

    return m_tempFile;
}

TempFile::TempFile(QObject *parent)
    : QObject(parent) {
    QTemporaryFile tmpFile;
    if (tmpFile.open()) {
        m_tmpFile = tmpFile.fileName();
    }

    QTemporaryFile fullscreenFile;
    if (fullscreenFile.open()) {
        m_fullscreenFile = fullscreenFile.fileName();
    }

    QTemporaryFile mosaicFile;
    if (mosaicFile.open()) {
        m_mosaicFile = mosaicFile.fileName();
    }

    QTemporaryFile blurFile;
    if (blurFile.open()) {
        m_blurFile = blurFile.fileName();
    }
    qDebug() << "ssss" << m_fullscreenFile;
}

TempFile::~TempFile() {}

QString TempFile::getTmpFileName() {
    if (!m_tmpFile.isEmpty()) {
        return QString("%1.png").arg(m_tmpFile);
    } else {
        return "/tmp/deepin-screenshot.png";
    }
}

QString TempFile::getFullscreenFileName() {
    if (!m_fullscreenFile.isEmpty()) {
        return QString("%1.png").arg(m_fullscreenFile);
    } else {
        return "/tmp/deepin-screenshot-fullscreen.png";
    }
}

QString TempFile::getMosaicFileName() {
    if (!m_mosaicFile.isEmpty()) {
        return QString("%1.png").arg(m_mosaicFile);
    } else {
        return "/tmp/deepin-screenshot-mosa.png";
    }
}

QString TempFile::getBlurFileName() {
    if (!m_blurFile.isEmpty()) {
        return QString("%1.png").arg(m_blurFile);
    } else {
        return "/tmp/deepin-screenshot-blur.png";
    }
}

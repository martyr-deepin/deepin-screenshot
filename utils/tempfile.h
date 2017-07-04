#ifndef TEMPFILE_H
#define TEMPFILE_H

#include <QObject>
#include <QWindow>

class TempFile : public QObject {
    Q_OBJECT
public:
    static TempFile *instance();

public slots:
    QString getTmpFileName();
    QString getFullscreenFileName();
    QString getMosaicFileName();
    QString getBlurFileName();

private:
     static TempFile* m_tempFile;
     TempFile(QObject* parent = 0);
     ~TempFile();

     QString m_tmpFile;
     QString m_fullscreenFile;
     QString m_mosaicFile;
     QString m_blurFile;
};
#endif // TEMPFILE_H

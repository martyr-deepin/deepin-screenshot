#ifndef CONFIGSETTINGS_H
#define CONFIGSETTINGS_H

#include <QObject>
#include <QSettings>
#include <QMutex>

class ConfigSettings : public QObject {
    Q_OBJECT
public:
    static ConfigSettings *instance();

    void setValue(const QString &group, const QString &key,
                  QVariant val);
    QVariant value(const QString &group, const QString &key,
                   const QVariant &defaultValue = QVariant());
    QStringList keys(const QString &group);

signals:
    void colorChanged();
    void shapeConfigChanged(const QString &shape,  const QString &key, int index);
    void straightLineConfigChanged(bool isStraightLine);

private:
    ConfigSettings(QObject* parent = 0);
    ~ConfigSettings();

    static ConfigSettings* m_configSettings;
    QSettings* m_settings;
    QMutex m_mutex;
};
#endif // CONFIGSETTINGS_H

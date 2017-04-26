#include "configsettings.h"

#include <QDir>
#include <QFileInfo>
#include <QDebug>

const QString CONFIG_PATH =   QDir::homePath() +
        "/.config/Deepin/DeepinScreenshot.conf";

ConfigSettings::ConfigSettings(QObject *parent)
    : QObject(parent) {
    m_settings = new  QSettings("Deepin","DeepinScreenshot", this);
    if (!QFileInfo(CONFIG_PATH).exists()) {
        setValue("common", "color_index", 3);
        setValue("common", "linewidth_index", 1);

        setValue("arrow", "color_index", 3);
        setValue("arrow", "linewidth_index", 1);
        setValue("oval", "color_index", 3);
        setValue("oval", "linewdith_index", 1);
        setValue("line", "color_index", 3);
        setValue("line", "linewidth_index", 1);
        setValue("rectangle", "color_index", 3);
        setValue("rectangle", "linewidth_index", 1);
        setValue("text", "color_index", 5);
        setValue("text", "fontsize", 12);

        setValue("save", "save_op", 1);
        setValue("showOSD", "show", true);
    }

    qDebug() << "Setting file:" << m_settings->fileName();
}

ConfigSettings* ConfigSettings::m_configSettings = nullptr;
ConfigSettings* ConfigSettings::instance() {
    if (!m_configSettings) {
        m_configSettings = new ConfigSettings();
    }

    return m_configSettings;
}

void ConfigSettings::setValue(const QString &group, const QString &key,
              const QVariant &value) {
    m_settings->beginGroup(group);
    m_settings->setValue(key, value);
    m_settings->endGroup();
}

QVariant ConfigSettings::value(const QString &group, const QString &key,
                               const QVariant &defaultValue) {
    QMutexLocker locker(&m_mutex);

    QVariant value;
    m_settings->beginGroup(group);
    value = m_settings->value(key, defaultValue);
    m_settings->endGroup();

    return value;
}

QStringList ConfigSettings::keys(const QString &group) {
    QStringList v;
    m_settings->beginGroup(group);
    v = m_settings->childKeys();
    m_settings->endGroup();

    return v;
}

ConfigSettings::~ConfigSettings() {
}

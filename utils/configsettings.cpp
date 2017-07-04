#include "configsettings.h"

#include <QDir>
#include <QFileInfo>
#include <QTemporaryFile>
#include <QDebug>

const QString CONFIG_PATH =   QDir::homePath() +
        "/.config/deepin/deepin-screenshot/tools.conf";

ConfigSettings::ConfigSettings(QObject *parent)
    : QObject(parent) {
    m_settings = new  QSettings("deepin","/deepin-screenshot/tools", this);

    if (!QFileInfo(CONFIG_PATH).exists()) {
        setValue("common", "color_index", 3);
        setValue ("common", "default_savepath", "");

        setValue("arrow", "color_index", 3);
        setValue("arrow", "arrow_linewidth_index", 1);
        setValue("arrow", "straightline_linewidth_index", 1);
        setValue("arrow", "is_straight", false);
        setValue("oval", "color_index", 3);
        setValue("oval", "linewidth_index", 1);
        setValue("line", "color_index", 3);
        setValue("line", "linewidth_index", 1);
        setValue("rectangle", "color_index", 3);
        setValue("rectangle", "linewidth_index", 1);
        setValue("text", "color_index", 3);
        setValue("text", "fontsize", 12);

        setValue("save", "save_op", 0);
        setValue("save", "save_quality", 100);
    }

    setValue("effect", "is_blur", false);
    setValue("effect", "is_mosaic", false);

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
              QVariant val) {
    m_settings->beginGroup(group);
    m_settings->setValue(key, val);
    m_settings->endGroup();
    m_settings->sync();

    if (val.type() == QVariant::Int) {
        emit shapeConfigChanged(group, key, val.toInt());
    }

    if (group == "arrow" && key == "is_straight") {
        emit straightLineConfigChanged(val.toBool());
    }

    qDebug() << "ConfigSettings:" << group << key << val;
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

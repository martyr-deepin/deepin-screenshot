/*
 * Copyright (C) 2017 ~ 2017 Deepin Technology Co., Ltd.
 *
 * Maintainer: Peng Hui<penghui@deepin.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

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

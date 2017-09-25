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

#include "menucontroller.h"
#include "utils/configsettings.h"

#include <QApplication>
#include <QStyleFactory>
#include <QDebug>

const QSize MENU_ICON_SIZE = QSize(14, 14);

MenuController::MenuController(QObject *parent)
    : QObject(parent)
    , m_ration(1)
{
    m_menu = new QMenu;
    m_menu->setFocusPolicy(Qt::StrongFocus);
    m_menu->setStyle(QStyleFactory::create("dlight"));

    QIcon rectIcon;
    rectIcon.addFile(":/image/menu_icons/rectangle-menu-norml.svg", MENU_ICON_SIZE,  QIcon::Normal);
    rectIcon.addFile(":/image/menu_icons/rectangle-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QAction* rectAct = new QAction(rectIcon, tr("Rectangle"), this);
    connect(rectAct, &QAction::triggered, [=] {
        emit shapePressed("rectangle");
    });

    QIcon ovalIcon;
    ovalIcon.addFile(":/image/menu_icons/ellipse-menu-norml.svg", MENU_ICON_SIZE,  QIcon::Normal);
    ovalIcon.addFile(":/image/menu_icons/ellipse-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QAction* ovalAct = new QAction(ovalIcon, tr("Ellipse"), this);
    connect(ovalAct, &QAction::triggered, [=]{
        emit shapePressed("oval");
    });

    QIcon arrowIcon;
    arrowIcon.addFile(":/image/menu_icons/arrow-menu-norml.svg", MENU_ICON_SIZE, QIcon::Normal);
    arrowIcon.addFile(":/image/menu_icons/arrow-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QAction* arrowAct = new QAction(arrowIcon, tr("Arrow"), this);
    connect(arrowAct, &QAction::triggered, [=]{
        emit shapePressed("arrow");
    });

    QIcon penIcon;
    penIcon.addFile(":/image/menu_icons/line-menu-norml.svg", MENU_ICON_SIZE, QIcon::Normal);
    penIcon.addFile(":/image/menu_icons/line-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QAction* penAct = new QAction(penIcon, tr("Pencil"), this);
    connect(penAct, &QAction::triggered, [=]{
        emit shapePressed("line");
    });

    QIcon textIcon;
    textIcon.addFile(":/image/menu_icons/text-menu-norml.svg", MENU_ICON_SIZE, QIcon::Normal);
    textIcon.addFile(":/image/menu_icons/text-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QAction* textAct = new QAction(textIcon, tr("Text"), this);
    connect(textAct, &QAction::triggered, [=]{
        emit shapePressed("text");
    });

    QIcon unDoIcon;
    unDoIcon.addFile(":/image/menu_icons/undo-menu-normal.svg", MENU_ICON_SIZE, QIcon::Normal);
    unDoIcon.addFile(":/image/menu_icons/undo-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QAction* unDoAct = new QAction(unDoIcon, tr("Undo"), this);
    connect(unDoAct, &QAction::triggered, [=]{
        emit unDoAction();
    });

    m_menu->addAction(rectAct);
    m_menu->addAction(ovalAct);
    m_menu->addAction(arrowAct);
    m_menu->addAction(penAct);
    m_menu->addAction(textAct);
    m_menu->addSeparator();
    m_menu->addAction(unDoAct);

    QIcon saveIcon;
    saveIcon.addFile(":/image/menu_icons/save-menu-norml.svg", MENU_ICON_SIZE, QIcon::Normal);
    saveIcon.addFile(":/image/menu_icons/save-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QMenu* saveMenu =  m_menu->addMenu(saveIcon, tr("Save"));

    saveMenu->setStyle(QStyleFactory::create("dlight"));
    QAction* saveAct1 = new QAction(tr("Save to desktop"), this);
    QAction* saveAct2 = new QAction(tr("Autosave"), this);
    QAction* saveAct3 = new QAction(tr("Save to specified folder"), this);
    QAction* saveAct4 = new QAction(tr("Copy to clipboard"), this);
    QAction* saveAct5 = new QAction(tr("Autosave and copy to clipboard"), this);
    QList<QAction*> actionList;
    actionList.append(saveAct1);
    actionList.append(saveAct2);
    actionList.append(saveAct3);
    actionList.append(saveAct4);
    actionList.append(saveAct5);
    for(int k = 0; k < actionList.length(); k++) {
        saveMenu->addAction(actionList[k]);
        connect(actionList[k], &QAction::triggered, [=]{
            emit saveBtnPressed(k);
        });
    }

    int saveOptionIndex = ConfigSettings::instance()->value("save", "save_op").toInt();
    actionList[saveOptionIndex]->setCheckable(true);
    actionList[saveOptionIndex]->setChecked(true);

    QIcon exitIcon;
    exitIcon.addFile(":/image/menu_icons/exit-menu-norml.svg", MENU_ICON_SIZE, QIcon::Normal);
    exitIcon.addFile(":/image/menu_icons/exit-menu-hover.svg", MENU_ICON_SIZE, QIcon::Active);
    QAction* closeAct = new QAction(exitIcon, tr("Exit"), this);
    m_menu->addAction(closeAct);
    connect(closeAct, &QAction::triggered, this, [=]{
        emit shapePressed("close");
    });

    connect(m_menu, &QMenu::aboutToHide, this, [=]{
        emit menuNoFocus();
    });
}

void MenuController::showMenu(QPoint pos) {
    m_menu->popup(pos);
}

MenuController::~MenuController() {

}

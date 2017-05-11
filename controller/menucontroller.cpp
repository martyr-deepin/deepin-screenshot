#include "menucontroller.h"
#include "utils/configsettings.h"

#include <QStyleFactory>

MenuController::MenuController(QObject *parent)
    : QObject(parent) {
    m_menu = new QMenu;
    m_menu->setStyle(QStyleFactory::create("dlight"));
    QIcon rectIcon;
    rectIcon.addPixmap(QPixmap(":/image/menu_icons/rectangle-menu-norml.png"), QIcon::Normal);
    rectIcon.addPixmap(QPixmap(":/image/menu_icons/rectangle-menu-hover.png"), QIcon::Active);
    QAction* rectAct = new QAction(rectIcon, tr("rectangle-tool"), this);

    QIcon ovalIcon;
    ovalIcon.addPixmap(QPixmap(":/image/menu_icons/ellipse-menu-norml.png"), QIcon::Normal);
    ovalIcon.addPixmap(QPixmap(":/image/menu_icons/ellipse-menu-hover.png"), QIcon::Active);
    QAction* ovalAct = new QAction(ovalIcon, tr("ellipse-tool"), this);

    QIcon arrowIcon;
    arrowIcon.addPixmap(QPixmap(":/image/menu_icons/arrow-menu-norml.png"), QIcon::Normal);
    arrowIcon.addPixmap(QPixmap(":/image/menu_icons/arrow-menu-hover.png"), QIcon::Active);
    QAction* arrowAct = new QAction(arrowIcon, tr("arrow-tool"), this);

    QIcon penIcon;
    penIcon.addPixmap(QPixmap(":/image/menu_icons/line-menu-norml.png"), QIcon::Normal);
    penIcon.addPixmap(QPixmap(":/image/menu_icons/line-menu-hover.png"), QIcon::Active);
    QAction* penAct = new QAction(penIcon, tr("line-tool"), this);

    QIcon textIcon;
    textIcon.addPixmap(QPixmap(":/image/menu_icons/text-menu-norml.png"), QIcon::Normal);
    textIcon.addPixmap(QPixmap(":/image/menu_icons/text-menu-hover.png"), QIcon::Active);
    QAction* textAct = new QAction(textIcon, tr("text-tool"), this);

    m_menu->addAction(rectAct);
    m_menu->addAction(ovalAct);
    m_menu->addAction(arrowAct);
    m_menu->addAction(penAct);
    m_menu->addAction(textAct);
    m_menu->addSeparator();

    QIcon saveIcon;
    saveIcon.addPixmap(QPixmap(":/image/menu_icons/save-menu-norml.png"), QIcon::Normal);
    saveIcon.addPixmap(QPixmap(":/image/menu_icons/save-menu-hover.png"), QIcon::Active);
    QMenu* saveMenu =  m_menu->addMenu(saveIcon, tr("save"));

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
    }

    int saveOptionIndex = ConfigSettings::instance()->value("save", "save_op").toInt();
    actionList[saveOptionIndex]->setCheckable(true);
    actionList[saveOptionIndex]->setChecked(true);

    QIcon exitIcon;
    exitIcon.addPixmap(QPixmap(":/image/menu_icons/exit-menu-norml.png"), QIcon::Normal);
    exitIcon.addPixmap(QPixmap(":/image/menu_icons/exit-menu-hover.png"), QIcon::Active);
    QAction* closeAct = new QAction(exitIcon, tr("close"), this);
    m_menu->addAction(closeAct);
}

void MenuController::showMenu(QPoint pos) {
    m_menu->show();
    m_menu->move(pos);
}

MenuController::~MenuController() {

}

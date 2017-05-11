#include "menucontroller.h"

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
    saveMenu->addAction(tr("Save to desktop"));
    saveMenu->addAction(tr("Autosave"));
    saveMenu->addAction(tr("Save to specified folder"));
    saveMenu->addAction(tr("Copy to clipboard"));
    saveMenu->addAction(tr("Autosave and copy to clipboard"));

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

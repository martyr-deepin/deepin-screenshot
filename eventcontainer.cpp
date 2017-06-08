#include "eventcontainer.h"

EventContainer::EventContainer(QWidget *parent)
    : QWidget(parent) {

}

EventContainer::~EventContainer() {

}

void EventContainer::handleEvent(QEvent *e) {
    Q_UNUSED(e);
}

#ifndef EVENTCONTAINER_H
#define EVENTCONTAINER_H

#include <QWidget>
#include <QEvent>

class EventContainer : public QWidget {
    Q_OBJECT
public:
    EventContainer(QWidget* parent = 0);
    ~EventContainer();

public slots:
    void handleEvent(QEvent* e);

};

#endif // EVENTCONTAINER_H

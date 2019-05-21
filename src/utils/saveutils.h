#ifndef SAVEUTILS_H
#define SAVEUTILS_H

#include <QObject>

enum SaveAction:unsigned int {
    SaveToDesktop,
    AutoSave,
    SaveToSpecificDir,
    SaveToClipboard,
    SaveToAutoClipboard
};

Q_DECLARE_METATYPE(SaveAction);

#endif // SAVEUTILS_H

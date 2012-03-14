#!/bin/bash
# Update translation.

MSGFMT=$(which msgfmt)
if [ -z "$MSGFMT" ]; then
    echo "You have 'gettext' installed to generate mo files."
    exit 1
fi

for pofile in po/*.po; do
    lang=$(basename $pofile .po)
    dest="locale/$lang/LC_MESSAGES"
    [[ -e "$dest" ]] || mkdir -p "$dest"
    echo "$pofile --> $dest/deepin-scrot.mo"
    msgfmt $pofile -o "$dest/deepin-scrot.mo"
done

## locale hack
ln -sf en_US locale/default

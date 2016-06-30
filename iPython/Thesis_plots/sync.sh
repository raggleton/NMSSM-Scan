#!/bin/bash -e

for f in *.pdf; do
    dest="/Users/robina/Dropbox/Thesis/thesis/Phenomenology/Figs/Scans/$f"
    if [ ! -e "$dest" ]; then
        cp "$f" "$dest"
    fi
    # need to remove and copy to make automator run its compression workflow
    cmp --silent "$f" "/Users/robina/Dropbox/Thesis/thesis/Phenomenology/Figs/Scans/$f"
    if [ "$?" -ne "0" ]; then
        echo "Replacing $f"
        rm /Users/robina/Dropbox/Thesis/thesis/Phenomenology/Figs/Scans/$f
        cp "$f" "$dest"
    fi
done

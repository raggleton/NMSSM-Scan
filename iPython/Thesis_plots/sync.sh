#!/bin/bash

for f in *.p*; do
    echo $f
    dest="/Users/robina/Dropbox/Thesis/thesis/Phenomenology/Figs/Scans/$f"

    if [ ! -e "$dest" ]; then
        echo "Copying $f"
        cp "$f" "$dest"
    else
        # need to remove and copy to make automator run its compression workflow
        cmp --silent "$f" "$dest"
        if [ "$?" -ne "0" ]; then
            echo "Replacing $f"
            rm "$dest"
            cp "$f" "$dest"
        else
            echo "Not replacing $f"
        fi
    fi
done

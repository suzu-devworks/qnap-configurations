#!/bin/sh
#
# erase macos dotfiles
#

patterns=".DS_Store;._*;.mediaartlocal"
target_dir="$1"

if [ ! -d "$target_dir" ]; then
        echo "> usage: $0 [target_dir]"
        exit 1
fi
echo "> current directory is $target_dir"

IFS=";"
for i in $patterns; do
        echo "> pattern is $i"
        find "$target_dir" -name "$i" | tr "\n" "\000" | xargs -0 rm -fr
done

exit 0
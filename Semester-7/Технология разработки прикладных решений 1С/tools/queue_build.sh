#!/bin/bash
# queue_build.sh <tag> <src-dir-win> <base-win> <dump-win> <cf-win>
set -e
R="$HOME/mnt/University/_runner"
T="$HOME/mnt/University/Semester-7/Технология разработки прикладных решений 1С/tools/build1c.ps1.tmpl"
tag="$1"
printf '\xEF\xBB\xBF' > "$R/in/$tag.ps1"
sed -e "s|@@TAG@@|$1|" -e "s|@@SRC@@|$2|" -e "s|@@BASE@@|$3|" -e "s|@@DUMP@@|$4|" -e "s|@@CF@@|$5|" "$T" >> "$R/in/$tag.ps1"
echo "queued $tag"

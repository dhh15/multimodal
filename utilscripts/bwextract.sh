#!/bin/sh
curl 'http://www.digipaper.fi/bluewings/?page=1' | grep -o '<a class="dplink" href="/bluewings/\(.*\)/" target="_blank"' | sed 's|<a class="dplink" href="/bluewings/\(.*\)/" target="_blank"|\1|' | sort | uniq > p1.txt
curl 'http://www.digipaper.fi/bluewings/?page=2' | grep -o '<a class="dplink" href="/bluewings/\(.*\)/" target="_blank"' | sed 's|<a class="dplink" href="/bluewings/\(.*\)/" target="_blank"|\1|' | sort | uniq > p2.txt
cat p1.txt | xargs -n 1 -I fn wget http://www.digipaper.fi/bluewings/fn/data.xml
cat p2.txt | xargs -n 1 -I fn wget http://www.digipaper.fi/bluewings/fn/data.xml
find ./ -name 'data.xml*' | xargs -n 1 grep '<File url="page.php?publication=' | sed 's|.*publication=\(.*\)&file=\(.*\)">|http://www.digipaper.fi/bluewings/\1/page.php?publication=\1\&file=\2|' | tr -d '\015' | xargs wget
find ./ -name '*.swf' | sed 's|.*publication=\(.*\)&file=\(.*\)|\1 \2|' | xargs -n 2 ./bwextract-swf.sh

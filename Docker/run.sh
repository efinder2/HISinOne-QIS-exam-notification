#!/bin/bash
if ! python3 /workingdir/crawl.py --config /data/myHisConfig.cfg; then
    exit 1
fi

while python3 /workingdir/crawl.py --config /data/myHisConfig.cfg; do
  var=$((60 * 60 * 1000));
  sleep $var

  current_date_time="$(date +%Y%m%d%H%M%S)";
  echo "$current_date_time";
done

echo "crawl missed"
exit 1
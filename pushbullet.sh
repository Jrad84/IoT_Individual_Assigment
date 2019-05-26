#! /bin/bash

API="o.sqsqGmTXwDFkFkPBGzfRvmgrpiT01xAx"
MSG="$1"

curl -u $API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Alert" -d body="$MSG"
#!/bin/sh

echo "Creating static bucket $STATIC_BUCKET"
mkdir -p /data/"$STATIC_BUCKET"

echo "Creating media bucket $MEDIA_BUCKET"
mkdir -p /data/"$MEDIA_BUCKET"

minio server /data

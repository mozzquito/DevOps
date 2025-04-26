#!/bin/bash

echo "=== ก่อนเคลียร์ ==="
free -h

sync
echo 3 > /proc/sys/vm/drop_caches

echo "=== หลังเคลียร์ ==="
free -h

#!/bin/bash

# ลบ unused Docker images
docker image prune -a -f

# ลบ unused builder cache
docker builder prune -a -f

# ลบ dangling builder cache
docker builder prune -f


sync && echo 3 | sudo tee /proc/sys/vm/drop_caches

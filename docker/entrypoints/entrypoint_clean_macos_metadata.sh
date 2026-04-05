#!/bin/bash

# Clean macOS metadata files from /music/ volumes.
# macOS creates these on external volumes and they can cause permission
# errors during inbox deletion inside the container.
# Runs as root during the entrypoint chain; errors are non-fatal.

if [ -f ./common.sh ]; then
    source ./common.sh
elif [ -f ./docker/entrypoints/common.sh ]; then
    source ./docker/entrypoints/common.sh
fi

log "Cleaning macOS metadata from /music/ ..."

# Remove AppleDouble resource fork files (._*) recursively
count=$(find /music/ -name '._*' -type f 2>/dev/null | wc -l)
if [ "$count" -gt 0 ]; then
    find /music/ -name '._*' -type f -delete 2>/dev/null || true
    log "  Removed $count AppleDouble (._*) files"
fi

# Remove .DS_Store files recursively
count=$(find /music/ -name '.DS_Store' -type f 2>/dev/null | wc -l)
if [ "$count" -gt 0 ]; then
    find /music/ -name '.DS_Store' -type f -delete 2>/dev/null || true
    log "  Removed $count .DS_Store files"
fi

# Remove top-level macOS system directories
for dir in .Spotlight-V100 .Trashes .fseventsd .TemporaryItems .DocumentRevisions-V100; do
    if [ -d "/music/$dir" ]; then
        rm -rf "/music/$dir" 2>/dev/null || true
        log "  Removed /music/$dir"
    fi
done

log "Done cleaning macOS metadata."

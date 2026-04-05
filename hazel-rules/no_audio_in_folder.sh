#!/bin/bash
# Hazel condition script: returns 0 (match) if a folder contains NO audio files.
# Used with a "Passes shell script" condition on folders, paired with a Trash action,
# to delete directories that don't contain any audio media.
#
# Audio extensions checked (case-insensitive):
#   mp3, flac, ogg, opus, m4a, aac, wav, aiff, aif, wma, alac, ape, wv, dsf, dff

folder="$1"

# Bail if not a directory (shouldn't happen if Hazel condition is "Kind is Folder")
[ -d "$folder" ] || exit 1

# Look for at least one audio file anywhere inside the folder tree.
# Using find with -iname for case-insensitive matching.
audio_extensions=(
    mp3 flac ogg opus m4a aac wav aiff aif wma alac ape wv dsf dff
)

# Build the find expression
find_args=( "$folder" -type f '(' )
first=true
for ext in "${audio_extensions[@]}"; do
    if $first; then
        first=false
    else
        find_args+=( -o )
    fi
    find_args+=( -iname "*.${ext}" )
done
find_args+=( ')' -print -quit )

match=$(find "${find_args[@]}" 2>/dev/null)

if [ -z "$match" ]; then
    # No audio files found → condition matches → Hazel should act (trash the folder)
    exit 0
else
    # Audio files exist → condition does NOT match → leave folder alone
    exit 1
fi

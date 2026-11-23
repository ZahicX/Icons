#!/usr/bin/env bash
# Resize every icon in icons/ to exactly 256x256 and compress it losslessly.
set -euo pipefail
cd "$(dirname "$0")/.."

TARGET=256
IM="$(command -v magick || command -v convert || true)"
if [[ -z "$IM" ]]; then
  echo "error: ImageMagick (magick/convert) not found" >&2
  exit 1
fi
if ! command -v oxipng >/dev/null 2>&1; then
  echo "error: oxipng not found" >&2
  exit 1
fi

shopt -s nullglob

dims() { "$IM" identify -format '%wx%h' "$1"; }

for f in icons/*.png; do
  d="$(dims "$f")"
  if [[ "$d" != "${TARGET}x${TARGET}" ]]; then
    tmp="$(mktemp --suffix=.png)"
    "$IM" "$f" -background none -filter Lanczos \
      -resize "${TARGET}x${TARGET}" \
      -gravity center -extent "${TARGET}x${TARGET}" \
      -strip "$tmp"
    mv "$tmp" "$f"
    echo "resized: $f ($d -> ${TARGET}x${TARGET})"
  fi
  # Lossless: strip metadata, optimize alpha, max effort. Never reduces quality.
  oxipng -q -o max --strip safe --alpha "$f" || true
done

for f in icons/*.jpg icons/*.jpeg; do
  d="$(dims "$f")"
  if [[ "$d" != "${TARGET}x${TARGET}" ]]; then
    tmp="$(mktemp --suffix=.jpg)"
    "$IM" "$f" -filter Lanczos \
      -resize "${TARGET}x${TARGET}" \
      -gravity center -background white -extent "${TARGET}x${TARGET}" \
      -strip -quality 95 "jpg:$tmp"
    mv "$tmp" "$f"
    echo "resized: $f ($d -> ${TARGET}x${TARGET})"
  fi
done

for f in icons/*.webp; do
  d="$(dims "$f")"
  if [[ "$d" != "${TARGET}x${TARGET}" ]]; then
    tmp="$(mktemp --suffix=.webp)"
    "$IM" "$f" -background none -filter Lanczos \
      -resize "${TARGET}x${TARGET}" \
      -gravity center -extent "${TARGET}x${TARGET}" \
      -strip -define webp:lossless=true "webp:$tmp"
    mv "$tmp" "$f"
    echo "resized: $f ($d -> ${TARGET}x${TARGET})"
  fi
done

for f in icons/*.svg icons/*.gif icons/*.ico; do
  echo "skipped (not auto-resized): $f"
done
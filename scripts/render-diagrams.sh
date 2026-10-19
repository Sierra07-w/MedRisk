#!/usr/bin/env bash
# Renders all Mermaid diagrams in docs/architecture/diagrams/*.mmd
# into readable SVG exports in docs/architecture/diagrams/export/.
#
# Requirements: Node.js >= 18
#   npm install -g @mermaid-js/mermaid-cli
# or, without global install (uses npx):
#   npx -y @mermaid-js/mermaid-cli -i <file> -o <file>
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/docs/architecture/diagrams"
OUT="$DIR/export"
mkdir -p "$OUT"
for f in "$DIR"/*.mmd; do
  name="$(basename "$f" .mmd)"
  echo "Rendering $name ..."
  npx -y @mermaid-js/mermaid-cli -i "$f" -o "$OUT/$name.svg" -b white
done
echo "Done. Exports in $OUT"

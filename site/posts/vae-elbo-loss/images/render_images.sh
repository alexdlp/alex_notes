#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../../.." && pwd)"

render_tikz() {
  local name="$1"
  local tmpdir
  tmpdir="$(mktemp -d)"

  {
    printf '%s\n' '\documentclass[tikz,border=2pt]{standalone}'
    printf '%s\n' '\usepackage{tikz}'
    printf '%s\n' '\begin{document}'
    cat "$script_dir/${name}.tex"
    printf '%s\n' '\end{document}'
  } > "$tmpdir/${name}.tex"

  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory "$tmpdir" \
    "$tmpdir/${name}.tex" >/dev/null

  inkscape --pdf-poppler "$tmpdir/${name}.pdf" \
    --export-filename="$script_dir/${name}.svg" >/dev/null

  if grep -Eq '<text|font-family' "$script_dir/${name}.svg"; then
    printf 'Generated %s.svg still depends on font-rendered text\n' "$name" >&2
    exit 1
  fi

  rm -rf "$tmpdir"
}

render_tikz vae1
render_tikz bayes_rule
render_tikz vae2

if [[ -x "$repo_root/.venv/bin/python" ]]; then
  "$repo_root/.venv/bin/python" "$script_dir/jensen_plot.py"
else
  python3 "$script_dir/jensen_plot.py"
fi

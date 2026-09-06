#!/bin/sh

# Synchronize canonical header and footer partials into every static page.
# Uses only POSIX shell and standard utilities so it runs on macOS and Linux.

set -eu

script_dir=$(CDPATH= cd -P "$(dirname "$0")" && pwd)
site_root=$(dirname "$script_dir")
partials_dir="$site_root/partials"
check_only=false

case "${1-}" in
  "") ;;
  --check) check_only=true ;;
  *)
    printf 'Usage: %s [--check]\n' "$0" >&2
    exit 2
    ;;
esac

work_dir=$(mktemp -d "${TMPDIR:-/tmp}/hcc-sync.XXXXXX")
trap 'rm -rf "$work_dir"' EXIT HUP INT TERM

render_partial() {
  template=$1
  root=$2
  current=$3

  awk -v root="$root" -v current="$current" '
    function replace_all(text, needle, replacement, position) {
      while ((position = index(text, needle)) != 0) {
        text = substr(text, 1, position - 1) replacement \
          substr(text, position + length(needle))
      }
      return text
    }

    FNR == NR {
      brand_lines[++brand_count] = $0
      next
    }

    {
      line = $0
      brand_token = "{{brand}}"
      brand_position = index(line, brand_token)
      if (brand_position) {
        prefix = substr(line, 1, brand_position - 1)
        suffix = substr(line, brand_position + length(brand_token))
        for (i = 1; i <= brand_count; i++) {
          ending = (i == brand_count ? suffix : "")
          brand_line = replace_all(brand_lines[i], "{{root}}", root)
          print prefix brand_line ending
        }
        next
      }

      line = replace_all(line, "{{root}}", root)
      split("home chiropractic naturopathic gpa atlas promise about contact", keys)
      for (i = 1; i <= 8; i++) {
        token = "{{" keys[i] "-current}}"
        value = (keys[i] == current ? " aria-current=\"page\"" : "")
        line = replace_all(line, token, value)
      }
      print line
    }
  ' "$partials_dir/brand.html" "$partials_dir/$template"
}

make_block() {
  kind=$1
  root=$2
  current=$3
  rendered="$work_dir/rendered"

  render_partial "$kind.html" "$root" "$current" > "$rendered"
  printf '    <!-- shared-%s:start; edit partials/%s.html -->\n' "$kind" "$kind"
  awk '{ print "    " $0 }' "$rendered"
  printf '    <!-- shared-%s:end -->\n' "$kind"
}

replace_block() {
  input_page=$1
  kind=$2
  block_file=$3
  output=$4
  start="    <!-- shared-$kind:start; edit partials/$kind.html -->"
  end="    <!-- shared-$kind:end -->"

  awk -v start="$start" -v end="$end" '
    FNR == NR {
      replacement = replacement (FNR == 1 ? "" : ORS) $0
      next
    }
    $0 == start {
      print replacement
      replacing = 1
      next
    }
    replacing && $0 == end {
      replacing = 0
      next
    }
    !replacing { print }
  ' "$block_file" "$input_page" > "$output"
}

drifted=0
page_count=0

while IFS='|' read -r relative_path root current; do
  page_count=$((page_count + 1))
  page_path="$site_root/$relative_path"
  header_block="$work_dir/header"
  footer_block="$work_dir/footer"
  with_header="$work_dir/with-header"
  synchronized="$work_dir/synchronized"

  make_block header "$root" "$current" > "$header_block"
  make_block footer "$root" "$current" > "$footer_block"
  replace_block "$page_path" header "$header_block" "$with_header"
  replace_block "$with_header" footer "$footer_block" "$synchronized"

  if cmp -s "$page_path" "$synchronized"; then
    continue
  fi

  if $check_only; then
    if [ "$drifted" -eq 0 ]; then
      printf 'Shared markup is out of sync:\n' >&2
    fi
    printf '  %s\n' "$relative_path" >&2
    drifted=1
  else
    mv "$synchronized" "$page_path"
  fi
done <<'PAGES'
index.html||home
chiropractic/index.html|../|chiropractic
naturopathic/index.html|../|naturopathic
GPA/index.html|../|gpa
atlas/index.html|../|atlas
promise/index.html|../|promise
about/index.html|../|about
contact/index.html|../|contact
PAGES

if [ "$drifted" -ne 0 ]; then
  printf 'Run: ./scripts/sync-shared.sh\n' >&2
  exit 1
fi

if $check_only; then
  printf 'Checked %s pages.\n' "$page_count"
else
  printf 'Synchronized %s pages.\n' "$page_count"
fi

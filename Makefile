.PHONY: serve stitch check

serve:
	python3 scripts/preview.py

stitch:
	python3 scripts/sync-shared.py

check:
	python3 scripts/sync-shared.py --check

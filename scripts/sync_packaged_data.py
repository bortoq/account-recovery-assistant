#!/usr/bin/env python3
"""Backward-compatible wrapper for scripts/check_data_source.py."""

from __future__ import annotations

from check_data_source import main


if __name__ == "__main__":
    raise SystemExit(main())

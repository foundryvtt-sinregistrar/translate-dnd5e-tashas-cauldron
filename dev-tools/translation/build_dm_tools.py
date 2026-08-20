#!/usr/bin/env python3
"""Build the Tasha DM-tools journal translation."""

from build_content import build_pack


if __name__ == "__main__":
    raise SystemExit(build_pack("tcoe-dm-tools", "dm-tools", "Herramientas del DM"))

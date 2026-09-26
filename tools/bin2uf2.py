#!/usr/bin/env python3
"""Convert a XIAO SAMD21 firmware .bin to .uf2 and optionally copy it to the
board's UF2 bootloader drive.

Useful where PlatformIO's upload tool (bossac) does not run, e.g. on Apple
Silicon Macs without Rosetta. The XIAO bootloader shows up as a USB drive
named "Arduino"; copying a .uf2 file onto it flashes the board.

Usage:
    python3 tools/bin2uf2.py [firmware.bin] [--flash [DRIVE]]
"""

import argparse
import os
import shutil
import struct
import sys

BASE_ADDRESS = 0x2000        # application start, after the 8 KB bootloader
FAMILY_SAMD21 = 0x68ED2B88
PAYLOAD = 256

DEFAULT_BIN = ".pio/build/seeed_xiao/firmware.bin"
DEFAULT_DRIVES = ["/Volumes/Arduino", "/media/" + os.environ.get("USER", "") + "/Arduino"]


def to_uf2(data):
    chunks = [data[i:i + PAYLOAD] for i in range(0, len(data), PAYLOAD)]
    out = bytearray()
    for n, chunk in enumerate(chunks):
        out += struct.pack(
            "<8I",
            0x0A324655,               # magic 0
            0x9E5D5157,               # magic 1
            0x00002000,               # flags: family ID present
            BASE_ADDRESS + n * PAYLOAD,
            PAYLOAD,
            n,
            len(chunks),
            FAMILY_SAMD21,
        )
        out += chunk.ljust(476, b"\0")
        out += struct.pack("<I", 0x0AB16F30)  # magic end
    return bytes(out)


def find_drive():
    for d in DEFAULT_DRIVES:
        if os.path.isfile(os.path.join(d, "INFO_UF2.TXT")):
            return d
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("bin", nargs="?", default=DEFAULT_BIN, help="input .bin (default: %(default)s)")
    p.add_argument("--flash", nargs="?", const="", metavar="DRIVE",
                   help="copy the .uf2 to the bootloader drive (auto-detected if omitted)")
    args = p.parse_args()

    with open(args.bin, "rb") as f:
        uf2 = to_uf2(f.read())
    out_path = os.path.splitext(args.bin)[0] + ".uf2"
    with open(out_path, "wb") as f:
        f.write(uf2)
    print(f"wrote {out_path} ({len(uf2) // 512} blocks)")

    if args.flash is None:
        return
    drive = args.flash or find_drive()
    if not drive or not os.path.isdir(drive):
        sys.exit("bootloader drive not found - double-tap RST on the XIAO and retry")
    shutil.copy(out_path, drive)
    print(f"copied to {drive}, the XIAO restarts with the new firmware")


if __name__ == "__main__":
    main()

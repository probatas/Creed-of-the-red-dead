"""Create a legal, locally patched Pokémon FireRed 1.0 ROM.

The program never contains or downloads Nintendo ROM data. It validates a
user-supplied US FireRed 1.0 dump, changes the GBA header title, repairs the
header checksum, and writes both the derived ROM and a tiny IPS patch.
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


FIRERED_10_SHA1 = "41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc"
EXPECTED_SIZE = 16 * 1024 * 1024
TITLE_OFFSET = 0xA0
CHECKSUM_OFFSET = 0xBD
CUSTOM_TITLE = b"CUBONE FIRE "
IPS_EOF_OFFSET = int.from_bytes(b"EOF", "big")
MAX_IPS_OFFSET = 0xFFFFFF
MAX_IPS_RECORD_SIZE = 0xFFFF


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def validate_firered_10(data: bytes) -> None:
    """Reject anything other than an unmodified US FireRed 1.0 ROM."""
    if len(data) != EXPECTED_SIZE or sha1(data) != FIRERED_10_SHA1:
        raise ValueError(
            "Filen er ikke en ren Pokemon FireRed (USA) v1.0-ROM "
            f"(forventet SHA-1 {FIRERED_10_SHA1})."
        )


def header_checksum(data: bytes | bytearray) -> int:
    """Calculate the standard GBA header complement byte."""
    return (-sum(data[TITLE_OFFSET:CHECKSUM_OFFSET]) - 0x19) & 0xFF


def apply_cubone_header(data: bytes) -> bytes:
    """Return a copy branded as the Cubone edition with a valid GBA header."""
    if len(data) < CHECKSUM_OFFSET + 1:
        raise ValueError("Filen er for liten til å være en GBA-ROM.")
    patched = bytearray(data)
    patched[TITLE_OFFSET : TITLE_OFFSET + len(CUSTOM_TITLE)] = CUSTOM_TITLE
    patched[CHECKSUM_OFFSET] = header_checksum(patched)
    return bytes(patched)


def _paths_match(first: Path, second: Path) -> bool:
    """Return whether two paths resolve to the same file or destination."""
    first_resolved = first.expanduser().resolve()
    second_resolved = second.expanduser().resolve()
    if first_resolved == second_resolved:
        return True
    try:
        return first_resolved.samefile(second_resolved)
    except OSError:
        return False


def validate_output_paths(rom: Path, output: Path, ips: Path) -> None:
    """Prevent any output from overwriting the input or another output."""
    if (
        _paths_match(rom, output)
        or _paths_match(rom, ips)
        or _paths_match(output, ips)
    ):
        raise ValueError(
            "ROM-, output- og IPS-filen må bruke tre forskjellige filstier."
        )


def make_ips(original: bytes, patched: bytes) -> bytes:
    """Build an IPS patch containing only contiguous changed byte ranges."""
    if len(original) != len(patched):
        raise ValueError("IPS-generatoren krever filer med samme størrelse.")

    output = bytearray(b"PATCH")
    position = 0
    while position < len(original):
        if original[position] == patched[position]:
            position += 1
            continue

        start = position
        while position < len(original) and original[position] != patched[position]:
            position += 1

        cursor = start
        while cursor < position:
            record_start = cursor

            # A record beginning at 0x454F46 serializes to b"EOF", which IPS
            # readers interpret as the end marker. Include the preceding byte
            # in this record so the encoded offset cannot collide with it.
            if record_start == IPS_EOF_OFFSET:
                record_start -= 1

            if record_start > MAX_IPS_OFFSET:
                raise ValueError(
                    "IPS-formatet støtter ikke endringer etter offset 0xFFFFFF."
                )

            record_end = min(position, record_start + MAX_IPS_RECORD_SIZE)
            chunk = patched[record_start:record_end]
            output.extend(record_start.to_bytes(3, "big"))
            output.extend(len(chunk).to_bytes(2, "big"))
            output.extend(chunk)
            cursor = record_end

    output.extend(b"EOF")
    return bytes(output)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lag Cubone-utgaven fra din egen FireRed (USA) v1.0-ROM."
    )
    parser.add_argument("rom", type=Path, help="sti til en ren FireRed v1.0 .gba-fil")
    parser.add_argument("-o", "--output", type=Path, default=Path("Cubone-FireRed.gba"))
    parser.add_argument("--ips", type=Path, default=Path("Cubone-FireRed.ips"))
    args = parser.parse_args()

    validate_output_paths(args.rom, args.output, args.ips)
    original = args.rom.read_bytes()
    validate_firered_10(original)
    patched = apply_cubone_header(original)
    args.output.write_bytes(patched)
    args.ips.write_bytes(make_ips(original, patched))
    print(f"Ferdig: {args.output} ({sha1(patched)})")
    print(f"IPS-patch: {args.ips}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from pathlib import Path
import unittest

import firered_cubone_patch as patcher


def apply_ips(original: bytes, ips: bytes) -> bytes:
    """Apply the subset of standard IPS records emitted by the patcher."""
    if not ips.startswith(b"PATCH"):
        raise ValueError("Ugyldig IPS-header.")

    output = bytearray(original)
    position = len(b"PATCH")
    while ips[position : position + 3] != b"EOF":
        offset = int.from_bytes(ips[position : position + 3], "big")
        position += 3
        size = int.from_bytes(ips[position : position + 2], "big")
        position += 2

        if size == 0:
            run_size = int.from_bytes(ips[position : position + 2], "big")
            value = ips[position + 2]
            position += 3
            output[offset : offset + run_size] = bytes([value]) * run_size
        else:
            output[offset : offset + size] = ips[position : position + size]
            position += size

    return bytes(output)


class FireRedCubonePatchTests(unittest.TestCase):
    def test_header_is_changed_and_checksum_is_valid(self):
        original = bytes(patcher.EXPECTED_SIZE)
        patched = patcher.apply_cubone_header(original)

        self.assertEqual(
            patched[patcher.TITLE_OFFSET : patcher.TITLE_OFFSET + 12],
            patcher.CUSTOM_TITLE,
        )
        self.assertEqual(patched[patcher.CHECKSUM_OFFSET], patcher.header_checksum(patched))
        self.assertEqual(len(patched), len(original))

    def test_ips_recreates_changes(self):
        original = bytes(512)
        patched = patcher.apply_cubone_header(original)
        ips = patcher.make_ips(original, patched)

        self.assertEqual(apply_ips(original, ips), patched)

    def test_ips_avoids_eof_offset_collision(self):
        original = bytes(patcher.IPS_EOF_OFFSET + 1)
        patched = bytearray(original)
        patched[patcher.IPS_EOF_OFFSET] = 0xA5

        ips = patcher.make_ips(original, bytes(patched))

        self.assertNotEqual(ips[len(b"PATCH") : len(b"PATCH") + 3], b"EOF")
        self.assertEqual(apply_ips(original, ips), bytes(patched))

    def test_output_paths_must_be_distinct(self):
        with self.assertRaisesRegex(ValueError, "forskjellige"):
            patcher.validate_output_paths(
                Path("FireRed.gba"),
                Path("./FireRed.gba"),
                Path("Cubone-FireRed.ips"),
            )

        with self.assertRaisesRegex(ValueError, "forskjellige"):
            patcher.validate_output_paths(
                Path("FireRed.gba"),
                Path("Cubone-FireRed.gba"),
                Path("./Cubone-FireRed.gba"),
            )

    def test_wrong_rom_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "FireRed"):
            patcher.validate_firered_10(bytes(patcher.EXPECTED_SIZE))


if __name__ == "__main__":
    unittest.main()

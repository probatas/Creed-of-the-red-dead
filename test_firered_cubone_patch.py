import unittest

import firered_cubone_patch as patcher


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

        self.assertTrue(ips.startswith(b"PATCH"))
        self.assertTrue(ips.endswith(b"EOF"))
        self.assertLess(len(ips), 64)

    def test_wrong_rom_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "FireRed"):
            patcher.validate_firered_10(bytes(patcher.EXPECTED_SIZE))


if __name__ == "__main__":
    unittest.main()

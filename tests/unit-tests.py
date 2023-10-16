import unittest

target = __import__("api-checksum")


class MyTestCase(unittest.TestCase):
    def test_checksum_different_order(self):
        data1 = "{A: 125, B: 42}"
        expected_checksum = sum(ord(c) for c in data1)
        data2 = "{B: 42, A: 125}"
        checksum1 = target.calculate_checksum(data1)
        checksum2 = target.calculate_checksum(data2)
        self.assertEqual(checksum1, checksum2)
        self.assertEqual(checksum1, expected_checksum)

    def test_checksum_same_order(self):
        data1 = "1234567890"
        expected_checksum = sum(ord(c) for c in data1)
        data2 = "1234567890"
        checksum1 = target.calculate_checksum(data1)
        checksum2 = target.calculate_checksum(data2)
        self.assertEqual(checksum1, checksum2)
        self.assertEqual(checksum1, expected_checksum)

    def test_checksum_different_values(self):
        data1 = "{A: 125, B: 42}"
        data2 = "{B: 42, A: 124}"
        checksum1 = target.calculate_checksum(data1)
        checksum2 = target.calculate_checksum(data2)
        self.assertNotEqual(checksum1, checksum2)


if __name__ == '__main__':
    unittest.main()

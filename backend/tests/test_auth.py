import unittest

from utils.auth import get_password_hash, verify_password


class AuthHashingTests(unittest.TestCase):
    def test_password_hashing_and_verification(self):
        password = "super-secret-password"
        hashed = get_password_hash(password)

        self.assertTrue(hashed)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong-password", hashed))


if __name__ == "__main__":
    unittest.main()

"""Interface-level tests for Hugo's loopback-only local demo server."""

import unittest

from hugo_integration.local_demo import build_server


class LocalDemoServerTests(unittest.TestCase):
    def test_server_binds_to_loopback_by_default(self):
        server = build_server(port=0)
        try:
            self.assertEqual(server.server_address[0], "127.0.0.1")
        finally:
            server.server_close()


if __name__ == "__main__":
    unittest.main()

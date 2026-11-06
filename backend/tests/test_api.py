"""Exercise the real HTTP API against an isolated database without cloud credentials."""

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import uuid


class APIIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backend = Path(__file__).resolve().parents[1]
        cls.log = tempfile.TemporaryFile(mode="w+")
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            cls.port = listener.getsockname()[1]
        env = dict(
            os.environ,
            DATABASE_URL=os.environ.get("TEST_DATABASE_URL", "sqlite://:memory:"),
            SECRET_KEY="ci-test-key-only",
            SANIC_DEBUG="False",
            SANIC_AUTO_RELOAD="False",
        )
        cls.process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "sanic",
                "app:app",
                "--host=127.0.0.1",
                "--port=" + str(cls.port),
                "--single-process",
                "--no-access-logs",
            ],
            cwd=cls.backend / "app",
            env=env,
            stdout=cls.log,
            stderr=subprocess.STDOUT,
        )
        cls.addClassCleanup(cls.stop_server)
        for _ in range(150):
            if cls.process.poll() is not None:
                break
            try:
                if cls.request("GET", "/")[0] == 200:
                    return
            except (URLError, ConnectionError):
                pass
            time.sleep(0.1)
        cls.log.seek(0)
        raise RuntimeError("API failed to start:\n" + cls.log.read())

    @classmethod
    def stop_server(cls):
        if cls.process.poll() is None:
            cls.process.terminate()
            try:
                cls.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                cls.process.kill()
                cls.process.wait()
        cls.log.close()

    @classmethod
    def request(cls, method, path, data=None, token=None):
        headers = {"Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json"
        if token:
            headers["Authorization"] = "Bearer " + token
        request = Request(
            "http://127.0.0.1:" + str(cls.port) + path,
            data=json.dumps(data).encode() if data is not None else None,
            method=method,
            headers=headers,
        )
        try:
            with urlopen(request, timeout=5) as result:
                return result.status, json.load(result)
        except HTTPError as error:
            return error.code, json.load(error)

    def register(self):
        email = str(uuid.uuid4()) + "@example.invalid"
        status, body = self.request(
            "POST",
            "/auth/register",
            {"username": "CI User", "email": email, "password": "test-password"},
        )
        self.assertEqual(status, 200, body)
        self.assertNotIn("password", body["user"])
        return email, body["token"]

    def test_health_and_authentication(self):
        self.assertEqual(self.request("GET", "/")[1]["message"], "TODO API")
        self.assertEqual(self.request("GET", "/tasks")[0], 401)
        self.assertEqual(self.request("GET", "/tasks", token="invalid-token")[0], 401)
        self.assertEqual(self.request("POST", "/auth/register", {})[0], 400)
        email, _ = self.register()
        self.assertEqual(
            self.request("POST", "/auth", {"email": email, "password": "wrong"})[0], 401
        )
        status, body = self.request(
            "POST", "/auth", {"email": email, "password": "test-password"}
        )
        self.assertEqual(status, 200, body)
        self.assertIn("token", body)
        self.assertEqual(
            self.request(
                "POST",
                "/auth/register",
                {"username": "Duplicate", "email": email, "password": "different"},
            )[0],
            400,
        )

    def test_task_lifecycle_and_cross_user_isolation(self):
        _, owner = self.register()
        _, stranger = self.register()
        self.assertEqual(
            self.request("GET", "/tasks", token=owner), (200, {"tasks": []})
        )
        self.assertEqual(self.request("POST", "/tasks", {}, owner)[0], 400)
        status, body = self.request(
            "POST",
            "/tasks",
            {"title": "CI task", "description": "Keep user data isolated"},
            owner,
        )
        self.assertEqual(status, 201, body)
        task = body["task"]
        self.assertEqual(task["title"], "CI task")
        self.assertEqual(self.request("GET", "/tasks", token=owner)[1]["tasks"], [task])
        self.assertEqual(self.request("GET", "/tasks", token=stranger)[1]["tasks"], [])
        endpoint = "/tasks/" + task["uuid"]
        self.assertEqual(self.request("DELETE", endpoint, token=stranger)[0], 404)
        self.assertEqual(self.request("DELETE", endpoint, token=owner)[0], 200)
        self.assertEqual(self.request("DELETE", endpoint, token=owner)[0], 404)
        self.assertEqual(
            self.request("DELETE", "/tasks/not-a-uuid", token=owner)[0], 400
        )
        self.assertEqual(self.request("GET", "/tasks", token=owner)[1]["tasks"], [])


if __name__ == "__main__":
    unittest.main()

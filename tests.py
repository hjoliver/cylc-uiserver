# -*- coding: utf-8 -*-
# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import tempfile
from unittest.mock import patch

from tornado.httpclient import HTTPResponse
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from cylc_singleuser import *


class MainHandlerTest(AsyncHTTPTestCase):
    """Test for the Main handler"""
    def get_app(self) -> Application:
        self.tempdir = tempfile.mkdtemp(suffix='mainhandlertest')
        return MyApplication(
            handlers=[
                ('/', MainHandler, {"path": self.tempdir})
            ]
        )

    def test_jupyterhub_version_returned(self):
        with patch.object(MainHandler, 'get_current_user') as mocked:
            mocked.return_value = {'name': 'yossarian'}
            with open(os.path.join(self.tempdir, "index.html"), "w+") as nf:
                nf.write("TESTING!")
                nf.flush()
                response = self.fetch("/")  # type: HTTPResponse
                assert response.body == b"TESTING!"
                assert "X-JupyterHub-Version" in response.headers

    def tearDown(self) -> None:
        if self.tempdir:
            shutil.rmtree(self.tempdir, ignore_errors=True)


class UserProfileHandlerTest(AsyncHTTPTestCase):
    """Test for UserProfile handler"""
    def get_app(self) -> Application:
        return MyApplication(
            handlers=[
                ('/userprofile', UserProfileHandler)
            ]
        )

    def test_user_profile_handler_cors_headers(self):
        with patch.object(UserProfileHandler, 'get_current_user') as mocked:
            mocked.return_value = {'name': 'yossarian'}
            response = self.fetch("/userprofile")  # type: HTTPResponse
            assert "Access-Control-Allow-Origin" in response.headers
            assert "Access-Control-Allow-Headers" in response.headers
            assert "Access-Control-Allow-Methods" in response.headers
            assert "Content-Type" in response.headers
            assert b'yossarian' in response.body


def test_my_application():
    """Test creating the Tornado app."""
    my_application = MyApplication(handlers=[])
    assert not my_application.is_closing
    my_application.signal_handler(None, None)
    assert my_application.is_closing


def test_cylcuiserver_absolute_path():
    """Test a Cylc UI server created with absolute path for static assets."""
    cylc_uiserver = CylcUIServer(8000, '/static/path', '/users/test')
    assert cylc_uiserver._port == 8000
    assert cylc_uiserver._static == '/static/path'
    assert cylc_uiserver._jupyter_hub_service_prefix == '/users/test'


def test_cylcuiserver_relative_path():
    """Test a Cylc UI server created with relative path for static assets."""
    cylc_uiserver = CylcUIServer(8000, './', '/users/test')
    assert cylc_uiserver._port == 8000
    assert cylc_uiserver._static == os.path.dirname(__file__)
    assert cylc_uiserver._jupyter_hub_service_prefix == '/users/test'

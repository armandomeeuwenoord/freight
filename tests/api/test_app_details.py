from __future__ import absolute_import

import json

from ds.models import App
from ds.testutils import TestCase


class AppDetailsBase(TestCase):
    def setUp(self):
        self.user = self.create_user()
        self.repo = self.create_repo()
        self.app = self.create_app(repository=self.repo)
        self.path = '/api/0/apps/{}/'.format(self.app.id)
        super(AppDetailsBase, self).setUp()


class AppUpdateTest(AppDetailsBase):
    def test_simple(self):
        resp = self.client.put(self.path, data={
            'name': 'foobar',
            'provider': 'shell',
            'provider_config': '{"command": "/usr/bin/true"}',
            'repository': 'git@example.com:repo-name.git',
        })
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['id'] == str(self.app.id)

        app = App.query.get(self.app.id)
        assert app.name == 'foobar'
        assert app.provider == 'shell'
        assert app.provider_config == {'command': '/usr/bin/true'}

    def test_no_params(self):
        resp = self.client.put(self.path)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['id'] == str(self.app.id)

        app = App.query.get(self.app.id)
        assert app.name == self.app.name
        assert app.provider == self.app.provider
        assert app.provider_config == self.app.provider_config

    def test_invalid_provider(self):
        resp = self.client.put(self.path, data={
            'name': 'foobar',
            'provider': 'dummy',
            'provider_config': '{"command": "/usr/bin/true"}',
            'repository': 'git@example.com:repo-name.git',
        })
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert data['error_name'] == 'invalid_provider'

    def test_invalid_provider_config(self):
        resp = self.client.put(self.path, data={
            'name': 'foobar',
            'provider': 'shell',
            'provider_config': '{}',
            'repository': 'git@example.com:repo-name.git',
        })
        assert resp.status_code == 400
        data = json.loads(resp.data)
        assert data['error_name'] == 'invalid_provider_config'
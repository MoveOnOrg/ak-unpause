import actionkit.api.user
import pytest
from _pytest.monkeypatch import MonkeyPatch

from unpause import unpause


sent_to_ak = []

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class MockAKAPI:

    def __init__(self, settings):
        return

    @staticmethod
    # Mock AK API call.
    def bulk_upload_rows(page, header, rows):
        sent_to_ak.append(rows)


class Test():
    monkeypatch = MonkeyPatch()

     # Mock what database would return for accounts to unpause.
    def mock_get_psql_results(self, args):
        return [{'user_id': 1}, {'user_id': 234, 'ignored': 'yes'}]

    def test_post_report(self):
        Test.monkeypatch.setattr("unpause.get_psql_results", self.mock_get_psql_results)
        Test.monkeypatch.setattr("unpause.AKUserAPI", MockAKAPI)
        # All args are mocked, but still required.
        args = {
            'AK_BASEURL': 'mock',
            'AK_USER': 'mock',
            'AK_PASSWORD': 'mock',
            'AK_IMPORT_PAGE': 'mock',
            'DB_HOST': 'mock',
            'DB_PORT': 'mock',
            'DB_USER': 'mock',
            'DB_PASS': 'mock',
            'DB_NAME': 'mock',
            'DB_QUERY': 'mock'
        }
        args = Struct(**args)
        unpause(args)
        assert sent_to_ak[0] == [[1], [234]]

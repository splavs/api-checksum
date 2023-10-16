import asyncio
import time
import unittest
import multiprocessing
import flask
import requests

PORT = '5050'
HOST = '127.0.0.1'
URL = f'http://{HOST}:{PORT}'
HEALTHCHECK_POSTFIX = '/healthcheck'
HEALTHCHECK_URL = f'{URL}{HEALTHCHECK_POSTFIX}'
target = __import__("api-checksum")


class MockServer:
    def __init__(self):
        multiprocessing.set_start_method("fork")
        self.server = None
        self.app = flask.Flask(__name__)
        self.app.add_url_rule(HEALTHCHECK_POSTFIX, view_func=self._healthcheck_callback)
        self.app.add_url_rule('/v1/test/1', view_func=self._one_callback)
        self.app.add_url_rule('/v1/test/2', view_func=self._two_callback)
        self.app.add_url_rule('/v1/test/3', view_func=self._three_callback)

    def _healthcheck_callback(self):
        return flask.jsonify(list())

    def _one_callback(self):
        return flask.jsonify({'A': 1, 'B': 1})

    def _two_callback(self):
        return flask.jsonify({'A': 2, 'B': 2})

    def _three_callback(self):
        return flask.jsonify({'A': 3, 'B': 3})

    def startup(self):
        self.server = multiprocessing.Process(target=self.app.run, args=(HOST, PORT))
        self.server.start()
        self.wait_for_flask()

    def shutdown(self):
        self.server.terminate()
        self.server.join()

    def wait_for_flask(self):
        response = requests.get(HEALTHCHECK_URL)
        while not response.ok:
            response = requests.get(HEALTHCHECK_URL)


class MyTestCase(unittest.TestCase):
    async def _test_integration_1api_3params_from_files(self):
        urls_values = await target.read_data('urls.txt')
        params_values = await target.read_data('parameter_values.txt')

        actual = await target.process_urls(params_values, urls_values)
        assert actual == [['1', 783], ['2', 785], ['3', 787]]
        assert actual != [['1', 0], ['2', 0], ['3', 0]]

    def test_integration_1api_3params_from_files(self):
        self.mock_server = MockServer()
        self.mock_server.startup()

        asyncio.run(self._test_integration_1api_3params_from_files())

    # async def _test_integration_100api_10params(self):
    #     urls_values = await target.read_data('urls.txt')
    #     params_values = await target.read_data('parameter_values.txt')
    #
    #     self.mock_server = MockServer()
    #     for i in range(100):
    #         self.mock_server.app.add_url_rule(f'/test{i}', view_func=)
    #     self.mock_server.startup()
    #
    #     actual = await target.process_urls(params_values, urls_values)
    #     assert actual == [['1', 783], ['2', 785], ['3', 787]]
    #     assert actual != [['1', 0], ['2', 0], ['3', 0]]

    # def test_integration_100api_10params(self):
    #     asyncio.run(self._test_integration_100api_10params())

    def tearDown(self):
        self.mock_server.shutdown()


if __name__ == '__main__':
    unittest.main()

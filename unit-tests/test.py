import unittest
from unittest.mock import patch
from io import StringIO
import requests
from health_check.health_check_solution import handler, check_health, calculate_availability, log_availability

class TestYourProgram(unittest.TestCase):

    # tests the check_health function when HTTP request returns 200 (OK, up)
    @patch('requests.request') # mocks the requests.request function
    def test_check_health_up(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.elapsed.total_seconds.return_value = 0.1
        endpoint = {'method': 'GET', 'url': 'https://example.com'}
        status, latency = check_health(endpoint)
        self.assertEqual(status, 'UP')
        self.assertEqual(latency, 100)

    # tests the check_health function when HTTP request is 500 (server error, down)
    @patch('requests.request')
    def test_check_health_down(self, mock_request):
        mock_request.return_value.status_code = 500
        mock_request.return_value.elapsed.total_seconds.return_value = 0.5
        endpoint = {'method': 'GET', 'url': 'https://example.com'}
        status, latency = check_health(endpoint)
        self.assertEqual(status, 'DOWN')
        self.assertEqual(latency, 500)

    # tests calculate_availability function given a set input
    def test_calculate_availability(self):
        health_results = {'example.com': [('UP', 100), ('DOWN', 500), ('UP', 200)]}
        availability = calculate_availability(health_results)
        self.assertEqual(availability, {'example.com': 67})

    # tests log_availability function given a set input
    @patch('sys.stdout', new_callable=StringIO)
    def test_log_availability(self, mock_stdout):
        availability = {'example.com': 67}
        log_availability(availability)
        output = mock_stdout.getvalue().strip()
        self.assertIn('example.com has 67% availability percentage', output)
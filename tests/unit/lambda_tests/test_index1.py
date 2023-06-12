import boto3
import pytest
from unittest import TestCase

from lambdas import index1


class TestSumOfTwoNumbers(TestCase):
    def test_sum(self):
        sum_input = {
            "first_number": "1",
            "second_number": "2"
        }
        output = index1.lambda_handler(sum_input, {})
        self.assertEqual(3, output["sum"])

import json
from requests import Response

class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecoder:
            assert False, f"Response is not in Json format. Respons text is {response.text}"

        assert name in response_as_dict, f"Response doesn't have key {name}"
        assert response_as_dict[name] == expected_value, error_message
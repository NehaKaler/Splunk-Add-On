import time
import json
import requests
from splunklib.modularinput import *

class JumpCloudAuthLogsInput(Script):
    def get_scheme(self):
        scheme = Scheme("JumpCloud Auth Logs")
        scheme.description = "Fetch authentication logs from JumpCloud"
        scheme.use_external_validation = True
        scheme.use_single_instance = False

        scheme.add_argument(Argument("api_key", title="API Key", required_on_create=True))
        scheme.add_argument(Argument("polling_interval", title="Polling Interval (seconds)", required_on_create=False))
        return scheme

    def validate_input(self, definition):
        api_key = definition.parameters["api_key"]
        if not api_key or not isinstance(api_key, str):
            raise ValueError("API key must be a non-empty string.")

    def stream_events(self, inputs, ew):
        for input_name, input_item in inputs.items():
            api_key = input_item["api_key"]
            polling_interval = int(input_item.get("polling_interval", 300))

            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json"
            }

            url = "https://console.jumpcloud.com/api/systemusers/authenticationattempts"

            while True:
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    data = response.json()

                    for event in data:
                        ew.write_event(Event(data=json.dumps(event)))
                except Exception as e:
                    ew.write_event(Event(data=json.dumps({"error": str(e)})))

                time.sleep(polling_interval)

if __name__ == "__main__":
    JumpCloudAuthLogsInput().run()

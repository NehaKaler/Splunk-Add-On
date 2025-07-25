import requests
import sys
import json
import time
import datetime
import os

def validate_input(helper, definition):
    required_fields = ['api_key', 'polling_interval']
    for field in required_fields:
        if not definition.get(field):
            raise ValueError(f"Missing required field: {field}")

def collect_events(helper, ew):
    api_key = helper.get_arg('api_key')
    polling_interval = int(helper.get_arg('polling_interval'))

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    # You can adjust this URL or params depending on what logs you want
    endpoint = "https://console.jumpcloud.com/api/systemusers"  # Example API
    params = {}

    helper.log_info(f"Polling JumpCloud API every {polling_interval} seconds.")

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            for item in data:
                event = json.dumps(item)
                ew.write_event(helper.new_event(source="jumpcloud", index=helper.get_output_index(), sourcetype="jumpcloud:auth", data=event))
        else:
            helper.log_warning("API did not return a list.")

    except Exception as e:
        helper.log_error(f"Error while fetching JumpCloud logs: {str(e)}")

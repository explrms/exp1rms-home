import json

import requests

from data import config
from utils.db_api import db


class IOT:
    def __init__(self) -> None:
        self.headers = {'Authorization': f'Bearer {config.YANDEX_TOKEN}'}

    async def get_device_list(self) -> dict:
        response = requests.get('https://api.iot.yandex.net/v1.0/user/info', headers=self.headers).json()
        return response['devices']

    async def get_rooms(self) -> dict:
        rooms = requests.get('https://api.iot.yandex.net/v1.0/user/info', headers=self.headers).json()['rooms']
        rooms_dict = {}
        for room in rooms:
            rooms_dict[str(room['id'])] = room['name']
        return rooms_dict

    async def toggle_off_device(self, device_id: str) -> int:
        params = {
            "devices": [{
                "id": str(device_id),
                "actions": [{
                    "type": "devices.capabilities.on_off",
                    "state": {
                        "instance": "on",
                        "value": False
                    }
                }]
            }]
        }
        response = requests.post('https://api.iot.yandex.net/v1.0/devices/actions', headers=self.headers, data=json.dumps(params))
        return response.status_code

    async def toggle_on_device(self, device_id: str) -> int:
        params = {
            "devices": [{
                "id": str(device_id),
                "actions": [{
                    "type": "devices.capabilities.on_off",
                    "state": {
                        "instance": "on",
                        "value": True
                    }
                }]
            }]
        }
        response = requests.post('https://api.iot.yandex.net/v1.0/devices/actions', headers=self.headers, data=json.dumps(params))
        return response.status_code

    async def color_setup(self, device_ids: list, color: str) -> int:
        color_code = await db.load_color_code_by_name(color)
        for device_id in device_ids:
            params = {
                "devices": [{
                    "id": str(device_id),
                    "actions": [{
                        "type": "devices.capabilities.color",
                        "state": {
                            "instance": "color",
                            "value": color_code
                        }
                    }]
                }]
            }
            response = requests.post('https://api.iot.yandex.net/v1.0/devices/actions', headers=self.headers, data=json.dumps(params))
            return response.status_code


iot = IOT()

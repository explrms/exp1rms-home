import json

import requests

from data import config


class IOT:
    def __init__(self) -> None:
        self.yandex_token = config.YANDEX_TOKEN

    async def get_device_list(self) -> dict:
        headers = {'Authorization': f'Bearer {self.yandex_token}'}
        response = requests.get('https://api.iot.yandex.net/v1.0/user/info', headers=headers).json()
        return response['devices']

    async def get_rooms(self) -> dict:
        headers = {'Authorization': f'Bearer {self.yandex_token}'}
        rooms = requests.get('https://api.iot.yandex.net/v1.0/user/info', headers=headers).json()['rooms']
        rooms_dict = {}
        for room in rooms:
            rooms_dict[str(room['id'])] = room['name']
        return rooms_dict

    async def toggle_off_device(self, device_id: str) -> int:
        headers = {'Authorization': f'Bearer {self.yandex_token}'}
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
        response = requests.post('https://api.iot.yandex.net/v1.0/devices/actions', headers=headers, data=json.dumps(params))
        return response.status_code

    async def toggle_on_device(self, device_id: str) -> int:
        headers = {'Authorization': f'Bearer {self.yandex_token}'}
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
        response = requests.post('https://api.iot.yandex.net/v1.0/devices/actions', headers=headers, data=json.dumps(params))
        return response.status_code


iot = IOT()

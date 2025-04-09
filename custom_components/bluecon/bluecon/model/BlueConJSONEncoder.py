from json import JSONEncoder

from .AccessDoor import AccessDoor
from .Pairing import Pairing
from .User import User
from .DeviceInfo import DeviceInfo

class BlueConJSONEncoder(JSONEncoder):
    def default(self, o):
        if type(o) is User:
            return {
                "email": o.email,
                "locale": o.locale
            }
        elif type(o) is Pairing:
            return {
                "id": o.id,
                "deviceId": o.deviceId,
                "accessDoorMap":o.accessDoorMap
            }
        elif type(o) is AccessDoor:
            return {
                'title': o.title,
                'accessId': {
                    'block': o.block,
                    'subblock': o.subBlock,
                    'number': o.number
                },
                'visible': o.visible
            }
        elif type(o) is DeviceInfo:
            return {
                'deviceId': o.deviceId,
                'connectionState': o.connectionState,
                'family': o.family,
                'type': o.type,
                'subType': o.subType,
                'photoCaller': o.photoCaller,
                'wirelessSignal': o.wirelessSignal
            }
        else:
            raise TypeError
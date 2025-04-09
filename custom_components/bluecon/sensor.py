from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .bluecon import BlueConAPI

from .const import DEVICE_MANUFACTURER, DOMAIN, HASS_BLUECON_VERSION

SIGNAL_TERRIBLE = "terrible"
SIGNAL_BAD = "bad"
SIGNAL_WEAK = "weak"
SIGNAL_GOOD = "good"
SIGNAL_EXCELENT = "excelent"
SIGNAL_UNKNOWN = "unknown"

async def async_setup_entry(hass, config, async_add_entities):
    bluecon: BlueConAPI = hass.data[DOMAIN][config.entry_id]

    pairings = await bluecon.getPairings()

    sensors = []

    for pairing in pairings:
        deviceInfo = await bluecon.getDeviceInfo(pairing.deviceId)

        sensors.append(
            BlueConWifiStrenghtSensor(
                bluecon,
                pairing.deviceId,
                deviceInfo
            )
        )
    
    async_add_entities(sensors)

class BlueConWifiStrenghtSensor(SensorEntity):
    _attr_should_poll = True

    def __init__(self, bluecon, deviceId, deviceInfo):
        self.__bluecon : BlueConAPI = bluecon
        self.deviceId = deviceId
        self._attr_unique_id = f'{self.deviceId}_connection_status'.lower()
        self.entity_id = f'{DOMAIN}.{self._attr_unique_id}'.lower()
        self._attr_options = [SIGNAL_TERRIBLE, SIGNAL_BAD, SIGNAL_WEAK, SIGNAL_GOOD, SIGNAL_EXCELENT, SIGNAL_UNKNOWN]
        self._attr_native_value = getWirelessSignalText(deviceInfo.wirelessSignal)
        self.__model = f'{deviceInfo.type} {deviceInfo.subType} {deviceInfo.family}'
        self._attr_translation_key = "wifi-state"

    @property
    def unique_id(self) -> str | None:
        return self.entity_id
    
    @property
    def device_class(self) -> SensorDeviceClass | None:
        return SensorDeviceClass.ENUM
    
    @property
    def device_info(self) -> DeviceInfo | None:
        return DeviceInfo(
            identifiers = {
                (DOMAIN, self.deviceId)
            },
            name = f'{self.__model} {self.deviceId}',
            manufacturer = DEVICE_MANUFACTURER,
            model = self.__model,
            sw_version = HASS_BLUECON_VERSION
        )

    async def async_update(self):
        deviceInfo = await self.__bluecon.getDeviceInfo(self.deviceId)
        self._attr_native_value = getWirelessSignalText(deviceInfo.wirelessSignal)

def getWirelessSignalText(wirelessSignal):
    if wirelessSignal == 0:
        return SIGNAL_TERRIBLE
    elif wirelessSignal == 1:
        return SIGNAL_BAD
    elif wirelessSignal == 2:
        return SIGNAL_WEAK
    elif wirelessSignal == 3:
        return SIGNAL_GOOD
    elif wirelessSignal == 4:
        return SIGNAL_EXCELENT
    else:
        SIGNAL_UNKNOWN

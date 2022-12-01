from dataclasses import KW_ONLY, dataclass
import pydantic
from typing import List, Dict, Any, Optional
from decimal import Decimal
from unicodedata import decimal


@dataclass
class EnvironmentConfig:
    __slots__ = ("base_url", "client_id", "client_secret")

    def __init__(
        self, 
        base_url: str, 
        client_id: str, 
        client_secret: str
    ) -> None:
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

@dataclass
class System:
    __slots__ = ("systemId", "name", "securityLevel", "hasAlarm", "country", "devices")

    def __init__(
        self,
        systemId: str,
        name: str,
        securityLevel: str,
        hasAlarm: bool,
        country: str,
        devices: List[Dict[str, Any]],
    ) -> None:
        self.systemId = systemId
        self.name = name
        self.securityLevel = securityLevel
        self.hasAlarm = hasAlarm
        self.country = country
        self.devices = [Device(**d) for d in devices]


@dataclass
class Device:
    __slots__ = ("id", "connectionState", "currentFwVersion", "product")

    def __init__(
        self,
        id: str,
        connectionState: int,
        currentFwVersion: str,
        product: Dict[str, Any],
    ) -> None:
        self.id = id
        self.connectionState = connectionState
        self.currentFwVersion = currentFwVersion
        #self.product = product
        self.product = Product(**product)


@dataclass
class Product:
    __slots__ = ("serialNumber", "name")

    def __init__(self, serialNumber: str, name: str) -> None:
        self.serialNumber = serialNumber
        self.name = name

@dataclass
class DeviceInfo:
    __slots__ = ("id", "connectionState", "firmware", "product", "availableFeatures")

    def __init__(
        self,
        id: str,
        connectionState: int,
        firmware: Dict[str, Any],
        product: Dict[str, Any],
        availableFeatures: Optional[str] = None,
    ) -> None:
        self.id = id
        self.connectionState = connectionState
        self.firmware = Firmware(**firmware)
        self.product = Product(**product)
        self.availableFeatures = availableFeatures #// ? insterted by Nathan.

@dataclass
class Firmware:
    __slots__ = ("currentFwVersion", "desiredFwVersion")

    def __init__(
        self,
        currentFwVersion: str,
        desiredFwVersion: str,
    ) -> None:
        self.currentFwVersion = currentFwVersion
        self.desiredFwVersion = desiredFwVersion


@dataclass
class SmartHomeCategories:
    __slots__ = (
        "sh_energyMetered",
        "sh_hwBoost",
        "sh_hwTemp",
        "sh_indoorCO2",
        "sh_indoorHumidity",
        "sh_indoorSpHeat",
        "sh_indoorSpCool",
        "sh_indoorTemp",
        "sh_outdoorTemp",
        "sh_poolTemp",
        "sh_smartMode",
        "sh_solarEnergyProducedDay",
        "sh_solarEnergyProducedWeek",
        "sh_solarEnergyProducedMonth",
        "sh_solarEnergyProducedYear",
        "sh_solarEnergyProducedTotal",
        "sh_ventBoost",
        "sh_ventMode",
        "sh_zones",
        "sh_zoneMode",
    )

    def __init__(
        self,
        sh_energyMetered: bool,
        sh_hwBoost: bool,
        sh_hwTemp: bool,
        sh_indoorCO2: bool,
        sh_indoorHumidity: bool,
        sh_indoorSpHeat: bool,
        sh_indoorSpCool: bool,
        sh_indoorTemp: bool,
        sh_outdoorTemp: bool,
        sh_poolTemp: bool,
        sh_smartMode: bool,
        sh_solarEnergyProducedDay: bool,
        sh_solarEnergyProducedWeek: bool,
        sh_solarEnergyProducedMonth: bool,
        sh_solarEnergyProducedYear: bool,
        sh_solarEnergyProducedTotal: bool,
        sh_ventBoost: bool,
        sh_ventMode: bool,
        sh_zones: bool,
        sh_zoneMode: bool,
    ) -> None:
        self.sh_energyMetered = sh_energyMetered
        self.sh_hwBoost = sh_hwBoost
        self.sh_hwTemp = sh_hwTemp
        self.sh_indoorCO2 = sh_indoorCO2
        self.sh_indoorHumidity = sh_indoorHumidity
        self.sh_indoorSpHeat = sh_indoorSpHeat
        self.sh_indoorSpCool = sh_indoorSpCool
        self.sh_indoorTemp = sh_indoorTemp
        self.sh_outdoorTemp = sh_outdoorTemp
        self.sh_poolTemp = sh_poolTemp
        self.sh_smartMode = sh_smartMode
        self.sh_solarEnergyProducedDay = sh_solarEnergyProducedDay
        self.sh_solarEnergyProducedWeek = sh_solarEnergyProducedWeek
        self.sh_solarEnergyProducedMonth = sh_solarEnergyProducedMonth
        self.sh_solarEnergyProducedYear = sh_solarEnergyProducedYear
        self.sh_solarEnergyProducedTotal = sh_solarEnergyProducedTotal
        self.sh_ventBoost = sh_ventBoost
        self.sh_ventMode = sh_ventMode
        self.sh_zones = sh_zones
        self.sh_zoneMode = sh_zoneMode


@dataclass
class SmartHomeZones:
    __slots__ = (
        "zoneId",
        "name",
        "commandOnly",
        "supportedModes",
        "mode",
        "temperature",
        "setpoint",
        "setpointHeat",
        "setpointCool",
        "setpointRangeMin",
        "setpointRangeMax",
        "isCelsius",
        "indoorCo2",
        "indoorHumidity",
    )

    def __init__(
        self,
        zoneId: str,
        name: str,
        commandOnly: bool,
        supportedModes: str,
        mode: str,
        temperature: decimal,
        setpoint: decimal,
        setpointHeat: decimal,
        setpointCool: decimal,
        setpointRangeMin: decimal,
        setpointRangeMax: decimal,
        isCelsius: bool,
        indoorCo2: decimal,
        indoorHumidity: decimal,
    ) -> None:
        self.zoneId = zoneId
        self.name = name
        self.commandOnly = commandOnly
        self.supportedModes = supportedModes
        self.mode = mode
        self.temperature = temperature
        self.setpoint = setpoint
        self.setpointHeat = setpointHeat
        self.setpointCool = setpointCool
        self.setpointRangeMin = setpointRangeMin
        self.setpointRangeMax = setpointRangeMax
        self.isCelsius = isCelsius
        self.indoorCo2 = indoorCo2
        self.indoorHumidity = indoorHumidity


#@dataclass(order=True, frozen=True)
class DevicePoint(pydantic.BaseModel):
    #sort_index: int = field(init=False, repr=False)
    category: str
    parameterId: str
    parameterName: str
    parameterUnit: str
    writable: bool
    timestamp: str
    value: Decimal
    strVal: str
    smartHomeCategories: Optional[List[str]]
    minValue: Optional[Decimal]
    maxValue: Optional[Decimal]
    enumValues: Optional[List[dict]] = []
    scaleValue: Optional[str]
    zoneId: Optional[int]

    #def __hash__(self):
    #    return hash((type(self), tuple(self.__dict__.values())))

    #def __post_init__(self):
    #    #self.sort_index = self.parameterId
    #    object.__setattr__(self, 'sort_index', self.parameterId)

@dataclass
class OriginalDevicePoint:
    __slots__ = (
        "category",
        "parameterId",
        "parameterName",
        "parameterUnit",
        "writable",
        "timestamp",
        "value",
        "strVal",
        "smartHomeCategories",
        "minValue",
        "maxValue",
        "enumValues",
        "scaleValue",
        "zoneId",
    )

    def __init__(
        self,
        category: str,
        parameterId: str,
        parameterName: str,
        parameterUnit: str,
        writable: bool,
        timestamp: str,
        value: decimal,
        strVal: str,
        smartHomeCategories: List[str],
        minValue: decimal,
        maxValue: decimal,
        enumValues: List[str],
        scaleValue: str,
        zoneId: int,
    ) -> None:
        self.category = category
        self.parameterId = parameterId
        self.parameterName = parameterName
        self.parameterUnit = parameterUnit
        self.writable = writable
        self.timestamp = timestamp
        self.value = value
        self.strVal = strVal
        self.smartHomeCategories = smartHomeCategories
        self.minValue = minValue
        self.maxValue = maxValue
        self.enumValues = enumValues
        self.scaleValue = scaleValue
        self.zoneId = zoneId


@dataclass
class AidMode:
    __slots__ = "aidMode"

    def __init__(
        self,
        aidMode: str,
    ) -> None:
        self.aidMode = aidMode


@dataclass
class Notifications:
    __slots__ = (
        "id",
        "alarmNumber",
        "deviceId",
        "severity",
        "status",
        "createdDatetime",
        "statusHistory",
        "header",
        "description",
        "equipName",
    )

    def __init__(
        self,
        id: str,
        alarmNumber: decimal,
        deviceId: str,
        severity: decimal,
        status: str,
        createdDatetime: str,
        statusHistory: List[Dict[str, Any]],
        header: str,
        description: str,
        equipName: str,
    ) -> None:
        self.id = id
        self.alarmNumber = alarmNumber
        self.deviceId = deviceId
        self.severity = severity
        self.status = status
        self.createdDatetime = createdDatetime
        self.statusHistory = [StatusHistory(**s) for s in statusHistory]
        self.header = header
        self.description = description
        self.equipName = equipName


@dataclass
class StatusHistory:
    __slots__ = ("status", "datetime")

    def __init__(
        self,
        status: str,
        datetime: int,
    ) -> None:
        self.status = status
        self.datetime = datetime


@dataclass
class Subscriptions:
    __slots__ = ("validUntil", "type")

    def __init__(
        self,
        validUntil: str,
        type: int,
    ) -> None:
        self.validUntil = validUntil
        self.type = type


@dataclass
class SmartHomeMode:
    __slots__ = "smartHomeMode"

    def __init__(
        self,
        smartHomeMode: str,
    ) -> None:
        self.smartHomeMode = smartHomeMode


@dataclass
class DeviceUpdate:
    __slots__ = "status", "payload"

    def __init__(
        self,
        status: int,
        payload: Dict[Any, Any],
    ) -> None:
        self.status = status
        self.payload = [DeviceUpdatePayload(**s) for s in payload]


@dataclass
class DeviceUpdatePayload:
    def __init__(self, _: KW_ONLY) -> None:
        self._

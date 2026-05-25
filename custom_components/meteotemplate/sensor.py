"""Sensor platform for Meteotemplate."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    DEGREE,
    PERCENTAGE,
    CONF_URL,
    UnitOfIrradiance,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfVolumetricFlux,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MeteotemplateCoordinator

MEASUREMENT = SensorStateClass.MEASUREMENT


@dataclass(frozen=True, kw_only=True)
class MTSensorDescription(SensorEntityDescription):
    """Describes a Meteotemplate sensor, incl. which JSON block it lives in."""

    section: str = "current_conditions"


def _temp(key: str, name: str) -> MTSensorDescription:
    return MTSensorDescription(
        key=key,
        name=name,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=MEASUREMENT,
    )


SENSORS: tuple[MTSensorDescription, ...] = (
    # --- Live current conditions ---
    _temp("temperature", "Temperature"),
    _temp("apparent_temperature", "Apparent temperature"),
    _temp("dewpoint", "Dew point"),
    MTSensorDescription(
        key="relative_humidity",
        name="Humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="pressure",
        name="Pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        native_unit_of_measurement=UnitOfPressure.HPA,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="wind_speed",
        name="Wind speed",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="wind_gust",
        name="Wind gust",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="bearing_degrees",
        name="Wind bearing",
        native_unit_of_measurement=DEGREE,
        state_class=MEASUREMENT,
        icon="mdi:compass",
    ),
    MTSensorDescription(
        key="wind_direction",
        name="Wind direction",
        icon="mdi:compass-outline",
    ),
    MTSensorDescription(
        key="rain_rate",
        name="Rain rate",
        device_class=SensorDeviceClass.PRECIPITATION_INTENSITY,
        native_unit_of_measurement=UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="solar_radiation",
        name="Solar radiation",
        device_class=SensorDeviceClass.IRRADIANCE,
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="UV",
        name="UV index",
        native_unit_of_measurement="UV index",
        state_class=MEASUREMENT,
        icon="mdi:weather-sunny-alert",
    ),
    _temp("temperature_indoor", "Indoor temperature"),
    MTSensorDescription(
        key="humidity_indoor",
        name="Indoor humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="leaf_wetness1",
        name="Leaf wetness",
        state_class=MEASUREMENT,
        icon="mdi:leaf",
    ),
    _temp("leaf_temperature1", "Leaf temperature"),
    # --- Daily roll-ups ---
    MTSensorDescription(
        key="precipitation",
        name="Rain today",
        section="today",
        device_class=SensorDeviceClass.PRECIPITATION,
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    MTSensorDescription(
        key="solar_radiation_max",
        name="Solar radiation max today",
        section="today",
        device_class=SensorDeviceClass.IRRADIANCE,
        native_unit_of_measurement=UnitOfIrradiance.WATTS_PER_SQUARE_METER,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="wind_gust_max",
        name="Wind gust max today",
        section="today",
        device_class=SensorDeviceClass.WIND_SPEED,
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="temperature_max", name="Temperature max today", section="today",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=MEASUREMENT,
    ),
    MTSensorDescription(
        key="temperature_min", name="Temperature min today", section="today",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS, state_class=MEASUREMENT,
    ),
)

# Soil moisture/temperature sensors 1..4, generated to avoid repetition.
SOIL_SENSORS: tuple[MTSensorDescription, ...] = tuple(
    sensor
    for i in range(1, 5)
    for sensor in (
        MTSensorDescription(
            key=f"soil_moisture{i}",
            name=f"Soil moisture {i}",
            device_class=SensorDeviceClass.MOISTURE,
            native_unit_of_measurement=PERCENTAGE,
            state_class=MEASUREMENT,
        ),
        _temp(f"soil_temperature{i}", f"Soil temperature {i}"),
    )
)

ALL_SENSORS = SENSORS + SOIL_SENSORS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create one sensor per field that is actually present in the feed."""
    coordinator: MeteotemplateCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = coordinator.data or {}
    station = data.get("station", {})

    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.title,
        manufacturer="Meteotemplate",
        model=(station.get("model") or "Weather Station"),
        configuration_url=entry.data.get(CONF_URL),
    )

    entities: list[MeteotemplateSensor] = []
    for desc in ALL_SENSORS:
        block = data.get(desc.section, {})
        if desc.key in block and block[desc.key] is not None:
            entities.append(
                MeteotemplateSensor(coordinator, entry, desc, device_info)
            )

    async_add_entities(entities)


class MeteotemplateSensor(
    CoordinatorEntity[MeteotemplateCoordinator], SensorEntity
):
    """A single Meteotemplate value."""

    _attr_has_entity_name = True
    entity_description: MTSensorDescription

    def __init__(
        self,
        coordinator: MeteotemplateCoordinator,
        entry: ConfigEntry,
        description: MTSensorDescription,
        device_info: DeviceInfo,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.section}_{description.key}"
        self._attr_device_info = device_info

    @property
    def native_value(self):
        block = self.coordinator.data.get(self.entity_description.section, {})
        return block.get(self.entity_description.key)

"""Data update coordinator for Tailwind."""
from datetime import timedelta

from gotailwind import Tailwind, TailwindDeviceStatus, TailwindError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER


class TailwindDataUpdateCoordinator(DataUpdateCoordinator[TailwindDeviceStatus]):
    """Class to manage fetching Tailwind data."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.tailwind = Tailwind(
            host=entry.data[CONF_HOST],
            token=entry.data[CONF_TOKEN],
            session=async_get_clientsession(hass),
        )
        super().__init__(
            hass,
            LOGGER,
            name=f"{DOMAIN}_{entry.data[CONF_HOST]}",
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self) -> TailwindDeviceStatus:
        """Fetch data from the Tailwind device."""
        try:
            return await self.tailwind.status()
        except TailwindError as err:
            raise UpdateFailed(err) from err

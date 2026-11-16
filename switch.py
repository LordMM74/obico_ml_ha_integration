from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Obico entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    # Create and add the ObicoSwitch entity
    async_add_entities([ObicoSwitch(coordinator, entry)])

class ObicoSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a switch to enable/disable communication with the API."""

    def __init__(self, coordinator, entry):
        """Initialize the switch."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "Obico ML Communication"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_api_communication"

    @property
    def is_on(self) -> bool:
        """Return the state of the switch directly from the coordinator."""
        return getattr(self.coordinator, "api_enabled", True)

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the API communication on."""
        self.coordinator.api_enabled = True
        await self.coordinator.async_request_refresh()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the API communication off."""
        self.coordinator.api_enabled = False
        self.async_write_ha_state()

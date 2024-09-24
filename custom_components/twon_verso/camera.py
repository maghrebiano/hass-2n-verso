from homeassistant.components.camera import Camera
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up 2N Verso camera based on a config entry."""
    verso = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([VersoCamera(verso)])

class VersoCamera(Camera):
    """Representation of a 2N Verso camera."""

    def __init__(self, verso):
        super().__init__()
        self._verso = verso

    @property
    def name(self):
        """Return the name of the camera."""
        return "2N Verso Camera"

    async def async_camera_image(self):
        """Return a still image response from the camera."""
        return await self._verso.get_camera_image()

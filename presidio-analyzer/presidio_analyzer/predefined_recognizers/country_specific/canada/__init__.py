"""Canada-specific recognizers package."""

from .ca_ohip_recognizer import CaOhipRecognizer
from .ca_postal_code_recognizer import CaPostalCodeRecognizer
from .ca_sin_recognizer import CaSinRecognizer

__all__ = [
    "CaOhipRecognizer",
    "CaPostalCodeRecognizer",
    "CaSinRecognizer",
]

"""Recognizer for Ontario Health Insurance Plan (OHIP) health card numbers."""

from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaOhipRecognizer(PatternRecognizer):
    """Recognize Ontario health card numbers using regex.

    An Ontario health card number is a 10-digit number followed by a
    2-letter version code. Cards show the number and version code together
    (for example "1234567890 AB"), and grouped forms such as
    "1234-567-890-AB" also appear in text. There is no public checksum for
    OHIP numbers, so detection relies on the shape of the value plus
    surrounding context words to keep confidence high.

    Reference: https://www.ontario.ca/page/health-cards

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    COUNTRY_CODE = "ca"

    PATTERNS = [
        Pattern(
            "OHIP (grouped)",
            r"\b\d{4}-\d{3}-\d{3}-[A-Z]{2}\b",
            0.6,
        ),
        Pattern(
            "OHIP (plain)",
            r"\b\d{10}[ -]?[A-Z]{2}\b",
            0.4,
        ),
    ]

    CONTEXT = [
        "ohip",
        "health card",
        "health card number",
        "ontario",
        "ontario health",
        "version code",
        # French equivalents
        "carte santé",
        "numéro de carte santé",
        "assurance-santé",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_OHIP",
        name: Optional[str] = None,
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
            name=name,
        )

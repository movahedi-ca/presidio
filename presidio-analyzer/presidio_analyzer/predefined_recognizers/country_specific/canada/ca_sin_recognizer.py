"""Recognizer for Canadian Social Insurance Number (SIN)."""

from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class CaSinRecognizer(PatternRecognizer):
    """Recognize Canadian Social Insurance Number (SIN) using regex + Luhn checksum.

    A SIN is a 9-digit number issued by Employment and Social Development Canada
    (ESDC) to administer various government programs. The last digit is a Luhn
    check digit computed over the first 8 digits. SINs beginning with 0 or 8
    are reserved or test numbers (for example the official ESDC test SIN
    046 454 286); detection relies on the Luhn checksum rather than the
    first digit, since a checksum failure already rejects false positives.

    Format: DDD DDD DDD or DDD-DDD-DDD or DDDDDDDDD

    Reference: https://www.canada.ca/en/employment-social-development/services/sin.html

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    """

    COUNTRY_CODE = "ca"

    PATTERNS = [
        Pattern("SIN (weak)", r"\b\d{9}\b", 0.05),
        Pattern("SIN (medium)", r"\b\d{3}([- ])\d{3}\1\d{3}\b", 0.5),
    ]

    CONTEXT = [
        "sin",
        "sin number",
        "social insurance",
        "social insurance number",
        "canada",
        # French equivalents
        "nas",
        "numéro nas",
        "numéro d'assurance sociale",
        "assurance sociale",
    ]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "en",
        supported_entity: str = "CA_SIN",
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

    def invalidate_result(self, pattern_text: str) -> bool:
        """
        Check if the pattern text cannot be validated as a CA_SIN entity.

        :param pattern_text: Text detected as pattern by regex
        :return: True if invalidated
        """
        only_digits = "".join(c for c in pattern_text if c.isdigit())
        return not self._luhn_valid(only_digits)

    @staticmethod
    def _luhn_valid(digits: str) -> bool:
        """Validate using the Luhn checksum."""
        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0

import pytest

from presidio_analyzer.predefined_recognizers import CaOhipRecognizer
from tests.assertions import assert_result_within_score_range


@pytest.fixture(scope="module")
def recognizer():
    return CaOhipRecognizer()


@pytest.fixture(scope="module")
def entities():
    return ["CA_OHIP"]


@pytest.mark.parametrize(
    "text, expected_len, expected_positions, expected_score_ranges",
    [
        # fmt: off
        # --- Valid: plain 10 digits + version code ---
        ("1234567890 AB", 1, ((0, 13),), ((0.4, 0.4),),),
        ("1234567890AB", 1, ((0, 12),), ((0.4, 0.4),),),
        ("1234567890-AB", 1, ((0, 13),), ((0.4, 0.4),),),
        ("1234567890 ab", 1, ((0, 13),), ((0.4, 0.4),),),
        # --- Valid: grouped 4-3-3 with hyphens ---
        ("1234-567-890-AB", 1, ((0, 15),), ((0.6, 0.6),),),
        ("1234-567-890-ab", 1, ((0, 15),), ((0.6, 0.6),),),
        # --- Valid: embedded in text ---
        ("my OHIP is 1234567890 AB", 1, ((11, 24),), ((0.4, 0.4),),),
        ("health card 1234-567-890-XY on file", 1, ((12, 27),), ((0.6, 0.6),),),

        # --- Invalid: no version code ---
        ("1234567890", 0, (), (),),
        ("call me at 1234567890 tomorrow", 0, (), (),),
        # --- Invalid: wrong digit counts ---
        ("123456789", 0, (), (),),
        ("123456789012 AB", 0, (), (),),
        ("1234-567-89-AB", 0, (), (),),
        # --- Invalid: version code missing or malformed ---
        ("1234567890 A", 0, (), (),),
        ("1234567890 123", 0, (), (),),
        # --- Invalid: other countries / formats ---
        ("90210", 0, (), (),),          # US ZIP
        ("K1A 0B1", 0, (), (),),        # Canadian postal code
        ("130 692 544", 0, (), (),),    # Canadian SIN
        # --- Invalid: attached to a larger token ---
        ("X1234567890 AB", 0, (), (),),
        ("1234567890ABC", 0, (), (),),
        # --- Invalid: empty string ---
        ("", 0, (), (),),
        # fmt: on
    ],
)
def test_when_ohip_in_text_then_all_ca_ohips_are_found(
    text,
    expected_len,
    expected_positions,
    expected_score_ranges,
    recognizer,
    entities,
):
    results = recognizer.analyze(text, entities)
    assert len(results) == expected_len

    for res, (st_pos, fn_pos), (st_score, fn_score) in zip(
        results, expected_positions, expected_score_ranges
    ):
        assert_result_within_score_range(
            res, entities[0], st_pos, fn_pos, st_score, fn_score
        )

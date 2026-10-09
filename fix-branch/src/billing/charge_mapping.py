"""Map interface FT1 segments to worklist charges."""

SUPPORTED_VERSIONS = {"2.5", "2.6"}  # 24.3.1: accept the 24.3 interface format

# 2.6 renamed two fields; map them back to the names the worklist expects.
FIELD_ALIASES_V26 = {"procedure_code": "ft1_procedure", "facility_id": "ft1_location"}


def _field(segment: dict, name: str):
    if segment.get("version") == "2.6":
        return segment.get(FIELD_ALIASES_V26.get(name, name))
    return segment.get(name)


def map_charge(segment: dict) -> dict | None:
    """Return a worklist charge, or None if the segment cannot be mapped."""
    if segment.get("version") not in SUPPORTED_VERSIONS:
        raise ValueError(f"Unsupported interface version: {segment.get('version')}")
    return {
        "cpt": _field(segment, "procedure_code"),
        "units": int(segment.get("units", 1)),
        "site": _field(segment, "facility_id"),
        "amount": float(segment["charge_amount"]),
    }


def map_batch(segments: list[dict]) -> list[dict]:
    return [map_charge(s) for s in segments]

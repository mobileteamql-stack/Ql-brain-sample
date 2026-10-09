from src.billing.charge_mapping import map_charge


def test_maps_v25_segment():
    seg = {"version": "2.5", "procedure_code": "71046", "units": 1,
           "facility_id": "SITE-01", "charge_amount": "120.00"}
    assert map_charge(seg)["cpt"] == "71046"


def test_maps_v26_segment_from_24_3_interface():
    seg = {"version": "2.6", "ft1_procedure": "71046", "units": 1,
           "ft1_location": "SITE-07", "charge_amount": "120.00"}
    charge = map_charge(seg)
    assert charge["cpt"] == "71046" and charge["site"] == "SITE-07"

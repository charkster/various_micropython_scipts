from ubeacon.ibeacon import IBeacon

beacon = IBeacon(
    uuid="acbdf5ff-d272-45f5-8e45-01672fe51c47",
    major=42,
    minor=21,
)

import bluetooth

ble = bluetooth.BLE()
ble.active(True)
ble.gap_advertise(250_000, adv_data=beacon.adv_data, resp_data=beacon.resp_bytes, connectable=False)

# EC:DA:3B:BF:50:FA ubeacon 50FA
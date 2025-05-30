import datetime

import pandas as pd
import re
from tqdm.auto import tqdm

from charges.models import PaymentMode

from locations.models import Location, LocationType, PinCode
from inventory.models import FloorPlan, ParkingSpotAvailability, VehicleType
from locations.get_pincode_from_lat_long import get_address_pincode_from_lat_long

BICYCLE = VehicleType.objects.get(name="BICYCLE")
PERSONAL_2 = VehicleType.objects.get(name="TWO_WHEELER")
PERSONAL_4 = VehicleType.objects.get(name="CAR_JEEP_VAN")


def set_values():
    df = pd.read_csv(
        "datadumps/Aug_11_2024/dmrc_station_details_with_coords_parking__w_contractor_contacts_lat_lon.tsv",
        sep="\t",
        header=0,
    )
    df = df.dropna()
    for i, row in tqdm(df.iterrows()):
        name = str(row["station_name"]).title()
        if not Location.objects.filter(name__iexact=name).exists():
            location = Location.objects.create(
                name=name,
                code=row["station_code"],
                type=LocationType.METRO_STATION,
                is_parking_available=row["parking_available"],
                latitude=row["parking_lat"],
                longitude=row["parking_lon"],
            )
            location.payment_mode.add(PaymentMode.objects.get(name="UPI"))
            location.payment_mode.add(PaymentMode.objects.get(name="CASH"))
            # location.payment_mode.add(PaymentMode.objects.get(name="WALLET"))
            # location.payment_mode.add(PaymentMode.objects.get(name="CREDIT_CARD"))
            # location.payment_mode.add(PaymentMode.objects.get(name="DEBIT_CARD"))
            # location.payment_mode.add(PaymentMode.objects.get(name="NET_BANKING"))

        location = Location.objects.get(name__iexact=name)

        if location.area is None:
            pincode, address = get_address_pincode_from_lat_long(
                str(location.latitude), str(location.longitude)
            )
            if pincode is not None:
                location.area = PinCode.objects.filter(code=pincode).first()
                location.save()
            if address is not None:
                location.address = address
                location.save()
        if location.address is None:
            _, address = get_address_pincode_from_lat_long(
                str(location.latitude), str(location.longitude)
            )
            if address is not None:
                location.address = address
                location.save()

        if location.is_parking_available:
            floor_name = str(row["gate_location"]).title()
            floors = FloorPlan.objects.filter(location=location, floor_name=floor_name)
            if not floors.exists():
                floor = FloorPlan.objects.create(
                    location=location,
                    floor_name=floor_name,
                    gate_num=0,
                    floor_num=0,
                    gate_location=row["gate_location"],
                    max_slots=row["parking_cycle"]
                    + row["parking_motorcycle"]
                    + row["parking_car"],
                    num_rows=1,
                    num_columns=1,
                    is_parking_paid=True,
                    is_parking_available=row["parking_available"],
                    is_divyang_friendly=True,
                    has_toilet=row["toilet"],
                    is_elevated=row["elevated"],
                    valid_from=datetime.time(0, 0, 0),
                    valid_till=datetime.time(23, 59, 59),
                )

            floor = FloorPlan.objects.get(location=location, floor_name=floor_name)
            _ = ParkingSpotAvailability.objects.filter(
                floor=floor, vehicle_type=BICYCLE
            ).update(total=row["parking_cycle"], available=row["parking_cycle"])
            _ = ParkingSpotAvailability.objects.filter(
                floor=floor, vehicle_type=PERSONAL_2
            ).update(
                total=row["parking_motorcycle"], available=row["parking_motorcycle"]
            )
            _ = ParkingSpotAvailability.objects.filter(
                floor=floor, vehicle_type=PERSONAL_4
            ).update(total=row["parking_car"], available=row["parking_car"])

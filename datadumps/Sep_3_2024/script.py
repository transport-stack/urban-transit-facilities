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
        "datadumps/Sep_3_2024/dmrc_station_details_with_coords_parking__w_contractor_contacts_lat_lon.tsv",
        sep="\t",
        header=0,
    )
    df = df.dropna()
    for i, row in tqdm(df.iterrows()):
        floors = FloorPlan.objects.filter(
            floor_name__iexact=row["gate_location"],
            location__name__iexact=row["station_name"],
        )
        if floors.exists():
            floor = floors.first()
            floor.latitude = row["parking_lat"]
            floor.longitude = row["parking_lon"]
            floor.save()
            print(floor)

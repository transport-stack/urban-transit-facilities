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
        "datadumps/Aug_13_2024/dmrc_lat_lon.tsv",
        sep="\t",
        header=0,
    )
    df = df.dropna()
    for i, row in tqdm(df.iterrows()):
        name = str(row["station_name"]).title()
        if Location.objects.filter(name__iexact=name).exists():
            location = Location.objects.get(
                name__iexact=name,
            )
            if row["parking_lat"]:
                location.latitude = row["parking_lat"]
            if row["parking_lon"]:
                location.longitude = row["parking_lon"]
            location.save()

        else:
            print(f"Error in {name}")

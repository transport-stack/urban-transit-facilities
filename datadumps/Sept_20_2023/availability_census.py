import pandas as pd
from locations.models import Location
from inventory.models import (
    VehicleType,
    FloorPlan,
    FloorPlanPrediction,
    FloorPlanPredictionVehicleWise,
)
from main.models import Days
from tqdm.auto import tqdm

BICYCLE = VehicleType.objects.get(name="BICYCLE")
PERSONAL_2 = VehicleType.objects.get(name="TWO_WHEELER")
PERSONAL_4 = VehicleType.objects.get(name="CAR_JEEP_VAN")


def add_census():
    df = pd.read_csv(
        "datadumps/Sept_20_2023/availability_census.csv",
        sep=",",
        header=0,
    )
    locations_observed = {}
    times = [
        "00:00",
        "01:00",
        "02:00",
        "03:00",
        "04:00",
        "05:00",
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
    ]
    for i, row in tqdm(df.iterrows()):
        locations = Location.objects.filter(code=row["station_code"])
        if locations.exists():
            location = locations.first()
            floors = FloorPlan.objects.filter(location=location)
            if floors.exists():
                if location.code not in locations_observed:
                    floor_objs = []
                    for floor in floors:
                        for day in Days.objects.all():
                            for time in times:
                                floor_objs.append(
                                    FloorPlanPrediction(day=day, floor=floor, time=time)
                                )
                    FloorPlanPrediction.objects.bulk_create(floor_objs)
                    locations_observed[location.code] = True
                for floor in floors:
                    day = Days.objects.get(day__icontains=row["day"])
                    prediction = FloorPlanPrediction.objects.get(
                        day=day, floor=floor, time=row["hour"]
                    )
                    objects_to_create = []
                    if float(row["BICYCLE"]) > 0:
                        objects_to_create.append(
                            FloorPlanPredictionVehicleWise(
                                prediction=prediction,
                                vehicle_type=BICYCLE,
                                value=float(row["BICYCLE"]),
                            )
                        )
                    if float(row["TWO_WHEELER"]) > 0:
                        FloorPlanPredictionVehicleWise(
                            prediction=prediction,
                            vehicle_type=PERSONAL_2,
                            value=float(row["TWO_WHEELER"]),
                        )
                    if float(row["CAR_JEEP_VAN"]) > 0:
                        FloorPlanPredictionVehicleWise(
                            prediction=prediction,
                            vehicle_type=PERSONAL_4,
                            value=float(row["CAR_JEEP_VAN"]),
                        )
                    FloorPlanPredictionVehicleWise.objects.bulk_create(
                        objects_to_create
                    )

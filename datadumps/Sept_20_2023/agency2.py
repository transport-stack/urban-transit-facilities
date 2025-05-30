from providers.models import ServiceProvider
import pandas as pd
from locations.models import Location, PinCode


def add_provider():
    df = pd.read_csv(
        "datadumps/Sept_20_2023/agency2.tsv",
        sep="\t",
        header=0,
    )
    for i, row in df.iterrows():
        provider, _ = ServiceProvider.objects.get_or_create(
            name=row["provider_name"], phone_num=str(row["provider_phone"])
        )
        if row["pincode"] and row["pincode"] > 0:
            pincodes = PinCode.objects.filter(code=row["pincode"])
            if pincodes.exists():
                pincode = pincodes.first()
                locations = Location.objects.filter(
                    name__icontains=str(row["name"]).lower(),
                    code__icontains=str(row["code"]).lower(),
                    area=pincode,
                )
                if locations.exists():
                    location = locations.first()
                    location.provider = provider
                    location.save()
        else:
            locations = Location.objects.filter(
                name__icontains=str(row["name"]).lower(),
                code__icontains=str(row["code"]).lower(),
            )
            if locations.exists():
                location = locations.first()
                location.provider = provider
                location.save()

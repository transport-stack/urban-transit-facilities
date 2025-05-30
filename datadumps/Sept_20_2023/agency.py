from providers.models import ServiceProvider
import pandas as pd


def add_provider():
    df = pd.read_csv(
        "datadumps/Sept_20_2023/agency.csv",
        sep=",",
        header=0,
    )
    for i, row in df.iterrows():
        ServiceProvider.objects.get_or_create(
            name=row["agency"], phone_num=str(row["phone"])
        )

from tqdm import tqdm

from src.data.loader import Database


def main():
    database = Database(
        name="vector_db",
        initialize=False,
    )

    data = [
        "Route Optimization carbon emissions reduction",
        "Vehicle Electrification carbon emissions reduction",
        "Public Transport Integration carbon emissions reduction",
        "Increased Frequency impact on carbon emissions",
        "Alternative Fuels reduce carbon emissions",
        "Infrastructure Development impact on carbon emissions",
        "Fuel Efficiency impact on carbon emissions",
        "Carbon Offsetting impact on carbon emissions",
        "Slow Steaming carbon emissions reduction",
        "Port Electrification carbon emissions reduction",
    ]

    for query in tqdm(data, desc="Processing keywords", total=len(data)):
        database.extend(query)


if __name__ == "__main__":
    main()

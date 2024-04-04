from src.data.loader import Database


def main():
    Database(
        name="vector_v2",
        initialize=True,
        queries=[
            "emission reduction public sector",
            "emissions in transportation",
            "co2 emissions",
            "climate change sustainibility",
        ],
    )
    print("Database initialized.")


if __name__ == "__main__":
    main()

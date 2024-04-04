from src.data.wrapper import KnowledgeBase
from src.utils.utils import generate_metadata

def main():
    data = generate_metadata(["Transport", "Cars", "EV"], type="action", previous_description="This is a test description")
    print(data)

if __name__ == "__main__":
    main()
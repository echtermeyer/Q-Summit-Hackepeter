from src.data.wrapper import KnowledgeBase


def test_inference():
    kb = KnowledgeBase()
    docs = kb.query("co2 emission", "which country has the highest co2 emission", k=1)
    print(docs)


if __name__ == "__main__":
    test_inference()

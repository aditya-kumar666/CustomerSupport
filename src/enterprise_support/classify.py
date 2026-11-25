import argparse

from .classifier import ComplaintClassifier
from .config import create_chat_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify a customer complaint")
    parser.add_argument("complaint", help="Customer complaint text")
    args = parser.parse_args()

    classifier = ComplaintClassifier(create_chat_model())
    print(classifier.classify(args.complaint).model_dump_json(indent=2))


if __name__ == "__main__":
    main()

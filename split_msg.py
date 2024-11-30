import argparse

from msg_split import split_message

MAX_LEN = 4096

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a message into fragments.")
    parser.add_argument(
        "--max_len",
        type=int,
        default=MAX_LEN,
        help=f"Maximum length of each fragment. (type: int, default: {MAX_LEN})",
    )
    parser.add_argument(
        "message_source_path", type=str, help="Path to the source file. (type: str)"
    )
    args = parser.parse_args()

    with open(args.message_source_path) as file:
        message = file.read()

    fragments_generator = split_message(message, max_len=args.max_len)

    for i, fragment in enumerate(fragments_generator):
        print(f"-------- fragment #{i + 1}: {len(fragment)} chars --------")
        print(fragment)

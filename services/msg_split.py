from typing import Generator

from bs4 import BeautifulSoup

MAX_LEN = 4096

ALLOWED_TO_SPLIT_TAGS = {
    "[document]",
    "p",
    "b",
    "strong",
    "i",
    "ul",
    "ol",
    "div",
    "span",
}


class SplitMessageException(Exception):
    pass


def split_plain_text(text: str, length=MAX_LEN):
    for i in range(0, len(text), length):
        yield text[i : i + length]


def split_message(source: str, max_len=MAX_LEN) -> Generator[str, None, None]:
    """Splits the original message (`source`) into fragments of the specified length
    (`max_len`)."""

    soup = BeautifulSoup(source, "html.parser")

    if soup.find() is None:
        yield from split_plain_text(source, max_len)
        return

    current_fragment = ""
    opened_tags_stack: list[str] = []

    def process_element(content):
        nonlocal current_fragment
        nonlocal opened_tags_stack

        if hasattr(content, "children") and content.name in ALLOWED_TO_SPLIT_TAGS:
            if content.name and content.name != "[document]":
                old_closing_tags = "".join(
                    f"</{tag}>" for tag in reversed(opened_tags_stack)
                )

                opened_tags_stack.append(content.name)

                closing_tags = "".join(
                    f"</{tag}>" for tag in reversed(opened_tags_stack)
                )

                if (
                    len(current_fragment) + len(str(content).split(">")[0] + ">")
                    > max_len
                    or len(current_fragment)
                    + len(str(content).split(">")[0] + ">")
                    + len(closing_tags)
                    > max_len
                ):
                    yield current_fragment + old_closing_tags
                    current_fragment = "".join(f"<{tag}>" for tag in opened_tags_stack)
                else:
                    current_fragment += str(content).split(">")[0] + ">"

            for child in content.children:
                yield from process_element(child)

            if content.name and content.name != "[document]":
                opened_tags_stack.pop()
                current_fragment += f"</{content.name}>"
            return

        element_html = str(content)
        opening_tags = "".join(f"<{tag}>" for tag in opened_tags_stack)
        closing_tags = "".join(f"</{tag}>" for tag in reversed(opened_tags_stack))

        predicted_length = len(current_fragment) + len(element_html) + len(closing_tags)

        if predicted_length > max_len:
            current_fragment += closing_tags

            if len(current_fragment) > max_len:
                raise SplitMessageException(
                    f"Element {current_fragment[:50]}... is too large to be split, length: {len(current_fragment)} > max_len: {max_len}"
                )

            yield current_fragment

            current_fragment = opening_tags + element_html
        else:
            current_fragment += element_html

    yield from process_element(soup)

    # add final fragment
    if current_fragment:
        current_fragment += "".join(f"</{tag}>" for tag in reversed(opened_tags_stack))
        yield current_fragment

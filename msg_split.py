from bs4 import BeautifulSoup

MAX_LEN = 4293
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


def split_message(source: str, max_len=MAX_LEN):
    soup = BeautifulSoup(source, "html.parser")
    current_fragment = ""
    fragments = []
    opened_tags_stack: list[str] = []

    def process_element(content):
        nonlocal current_fragment
        nonlocal opened_tags_stack

        if hasattr(content, "children") and content.name in ALLOWED_TO_SPLIT_TAGS:

            if content.name and content.name != "[document]":
                opened_tags_stack.append(content.name)
                current_fragment += str(content).split(">")[0] + ">"

            for child in content.children:
                process_element(child)

            if content.name and content.name != "[document]":
                opened_tags_stack.pop()
                current_fragment += f"</{content.name}>"

            return

        element_html = str(content)
        closing_tags = "".join(f"</{tag}>" for tag in reversed(opened_tags_stack))

        if len(current_fragment) + len(element_html) + len(closing_tags) > max_len:

            current_fragment += closing_tags
            fragments.append(current_fragment)

            current_fragment = ""
            for tag in opened_tags_stack:
                current_fragment += f"<{tag}>"
            current_fragment += element_html

        else:
            current_fragment += element_html

    process_element(soup)

    # add final fragment
    if current_fragment:
        for tag in reversed(opened_tags_stack):
            current_fragment += f"</{tag}>"
        fragments.append(current_fragment)

    return fragments


if __name__ == "__main__":

    with open("source.html") as file:
        message = file.read()

    fragments = split_message(message)

    for i, fragment in enumerate(fragments):
        print()
        print(f"-------- fragment #{i + 1}: {len(fragment)} chars --------")
        print()
        print(fragment)

import pytest

from services.msg_split import SplitMessageException, split_message

plain_text = "This is a long text that needs to be split into smaller fragments."

html = """<div>
<div>
<p>
Lorem ipsum dolor sit amet consectetur, adipisicing elit. Eius, excepturi!
<span> Lorem ipsum dolor sit amet. </span>
<span>
Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptates.
</span>
</p>
<p>
Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptates.
</p>
</div>
<p>
Lorem ipsum, dolor sit amet consectetur adipisicing elit. Recusandae, aperiam.
</p>
</div>"""


def test_split_plain_text():
    max_len = 10
    expected_fragments = [
        "This is a ",
        "long text ",
        "that needs",
        " to be spl",
        "it into sm",
        "aller frag",
        "ments.",
    ]
    result = list(split_message(plain_text, max_len))
    assert result == expected_fragments


def test_split_html_150():
    max_len = 150
    expected_fragments = [
        "<div>\n<div>\n<p>\nLorem ipsum dolor sit amet consectetur, adipisicing elit. Eius, excepturi!\n<span> Lorem ipsum dolor sit amet. </span>\n</p></div></div>",
        "<div><div><p><span>\nLorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptates.\n</span>\n</p>\n<p></p></div></div>",
        "<div><div><p>\nLorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptates.\n</p>\n</div>\n<p></p></div>",
        "<div><p>\nLorem ipsum, dolor sit amet consectetur adipisicing elit. Recusandae, aperiam.\n</p>\n</div>",
    ]
    result = list(split_message(html, max_len))
    assert result == expected_fragments


def test_split_html_200():
    max_len = 200
    expected_fragments = [
        "<div>\n<div>\n<p>\nLorem ipsum dolor sit amet consectetur, adipisicing elit. Eius, excepturi!\n<span> Lorem ipsum dolor sit amet. </span>\n<span></span></p></div></div>",
        "<div><div><p><span>\nLorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptates.\n</span>\n</p>\n<p></p></div></div>",
        "<div><div><p>\nLorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam, voluptates.\n</p>\n</div>\n<p>\nLorem ipsum, dolor sit amet consectetur adipisicing elit. Recusandae, aperiam.\n</p>\n</div>",
    ]
    result = list(split_message(html, max_len))
    assert result == expected_fragments


def test_split_html_exceeds_max_len():
    max_len = 100
    with pytest.raises(SplitMessageException):
        list(split_message(html, max_len))


if __name__ == "__main__":
    pytest.main()

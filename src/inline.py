import re
from textnode import TextNode
from project_types import TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        try:
            if node.text_type != "text":
                new_nodes.append(node)
                continue
        except AttributeError:
            new_nodes.append(node)
            continue
        if node.text == "":
            new_nodes.append(node)
            continue
        sub_string = node.text.split(delimiter)
        if len(sub_string) % 2 == 0:
            raise ValueError("matching delimiter not found, invalid markdown")
        sub_list: list[TextNode] = []

        for index, word in enumerate(sub_string):
            if word == "":
                continue
            if index % 2 == 0:
                sub_list.append(TextNode(word, "text"))
            else:
                sub_list.append(TextNode(word, text_type))

        new_nodes.extend(sub_list)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text == "":
            continue

        image_tups = extract_markdown_images(node.text)
        if not image_tups:
            new_nodes.append(node)
            continue

        working_nodes: list[TextNode] = []
        for image in image_tups:
            split_text = node.text.split(f"![{image[0]}]({image[1]})", 1)
            remainder_text = split_text[1]
            if split_text[0]:
                working_nodes.append(TextNode(split_text[0], "text"))
            working_nodes.append(TextNode(image[0], "image", image[1]))
            if remainder_text:
                working_nodes.append(TextNode(remainder_text, "text"))
            new_nodes.extend(working_nodes)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text == "":
            continue

        link_tups = extract_markdown_links(node.text)
        if not link_tups:
            new_nodes.append(node)
            continue

        working_nodes: list[TextNode] = []
        for link in link_tups:
            split_text = node.text.split(f"[{link[0]}]({link[1]})", 1)
            remainder_text = split_text[1]
            if split_text[0]:
                working_nodes.append(TextNode(split_text[0], "text"))
            working_nodes.append(TextNode(link[0], "link", link[1]))
            if remainder_text:
                working_nodes.append(TextNode(remainder_text, "text"))
            new_nodes.extend(working_nodes)

    return new_nodes

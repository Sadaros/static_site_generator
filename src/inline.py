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

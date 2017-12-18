from zutils.merge_util import merge_map
from zutils.timeit import TimeIt
import re

from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import requests


class HTMLUtil:

    @staticmethod
    def get_inner_text(element, clean=True):
        return "\n".join(HTMLUtil.get_inner_texts(element))

    @staticmethod
    def possible_tags_structure(tag):
        return [tag, tag + " ", " " + tag, " " + tag + " "]

    @staticmethod
    def remove_tags(string, tags_to_be_removed=["em", "br", "i"]):
        """
        Removes the desired tags from HTML content.
        params: string HTML content , args is list of desired tags
        """
        remove_tag_list = []
        for tag in tags_to_be_removed:
            for rm_tag in HTMLUtil.possible_tags_structure(tag):
                remove_tag_list.append(rm_tag)
        for tag in tags_to_be_removed:
            if string.find(tag) == 0:
                if tag is "br":
                    string = string.replace("<" + tag + ">", ".").replace("</" + tag + ">", ".")
                    return string.replace("<" + tag + " /", ".").replace("<" + tag + "/", ".")
                else:
                    return string.replace("<" + tag + ">", "").replace("</" + tag + ">", "")
        string = re.sub('\.\s+\.', ".", string)
        return string

    @staticmethod
    def restructure_html(soup):
        """
        Restructure the BeautifulSoup object by adjusting the position of
        certain tags.
        eg input: <p><b>e1</b> Text1 <strong>Text2 </strong>Text3</p>
        output: <p><b>e1</b><strong>Text1 Text2 Text3</strong></p>
        """
        strong_elements = soup.findAll("strong")
        for element in strong_elements:
            if not element.parent:
                continue
            content_elements = element.parent.contents
            for content_element in content_elements:
                if type(content_element) is Tag and content_element.name == "strong" and content_element.string:
                    if type(content_element.previousSibling) is NavigableString:
                        content_element.string.replace_with(unicode(content_element.previousSibling) + " " + unicode(content_element.string))
                        content_element.previousSibling.extract()
                    if type(content_element.previousSibling) is Tag and content_element.previousSibling.name == "strong" and content_element.previousSibling.string:
                        content_element.string.replace_with(unicode(content_element.previousSibling.string) + " " + unicode(content_element.string))
                        content_element.previousSibling.extract()
                    if type(content_element.nextSibling) is NavigableString:
                        content_element.string.replace_with(unicode(content_element.string) + " " + unicode(content_element.nextSibling))
                        content_element.nextSibling.extract()
        return soup

    @staticmethod
    def get_inner_texts(element, clean=True):
        """
        Extracts the inner text from a BeautifulSoup object of any html page.
        """
        texts = []
        if element is not None:
            tags = element.stripped_strings
            if tags:
                for tag in tags:
                    value = tag.strip()
                    if clean:
                        value = re.sub(re.compile(r'\s+'), " ", value)
                        value = re.sub(re.compile(r'\n'), ". ", value)
                        value = re.sub(re.compile(r'\\n'), "", value)
                        value = value.replace("\\n", "")
                        value = value.replace("\n", "")
                        value = value.replace("\\", "")
                    if value:
                        texts.append(value)
        return texts

    @staticmethod
    def get_inner_texts_with_parents(element, clean=True):
        """
        Extracts the inner text from a BeautifulSoup object of any html page.
        """
        texts = []
        if element is not None:
            tags = element.strings
            if tags:
                for tag in tags:
                    value = tag.strip()
                    parent = tag.parent.name
                    if clean:
                        value = re.sub(re.compile(r'\s+'), " ", value)
                        value = re.sub(re.compile(r'\n'), ". ", value)
                        value = re.sub(re.compile(r'\\n'), "", value)
                        value = value.replace("\\n", "")
                        value = value.replace("\n", "")
                        value = value.replace("\\", "")
                    if value:
                        texts.append((value, parent))
        return texts

    @staticmethod
    def get_soup(url):
        html_string = requests.get(url, timeout=360).content
        return BeautifulSoup(HTMLUtil.remove_tags(html_string))

    @staticmethod
    def get_soup_from_html(html):
        return BeautifulSoup(HTMLUtil.remove_tags(html))


class HTMLFlattener(object):

    @staticmethod
    @TimeIt("HTMLFlattener.flatten_html")
    def flatten_html(html):

        """
        Create a flat new html soup using the class_corrected thing above

        So if we have:
        <div class="A1 B1">
            <div class="A2 C2">inner1</div>
            <span class="A2 D2">inner2</span>
        </div>

        then we create:

        [
            {
                "class": [
                    "A1",
                    "C2",
                    "A2",
                    "B1"
                ],
                "data": "inner1",
                "name": "div"
            },
            {
                "class": [
                    "A1",
                    "A2",
                    "D2",
                    "B1"
                ],
                "data": "inner2",
                "name": "span"
            }
        ]

        """
        soup = HTMLUtil.get_soup_from_html(html)
        output = []
        index = 0
        for ch in soup.body.recursiveChildGenerator():
            if isinstance(ch, NavigableString):
                if ch.strip():
                    x = Tag(name=ch.parent.name)
                    x.attrs = ch.parent.attrs
                    x.string = ch
                    if ch.parent.name == "style" or \
                            ch.parent.name == "script" or \
                            ch.parent.name == "code":
                        continue
                    output.append({"data": ch,
                                   "name": ch.parent.name,
                                   "class": ch.parent.attrs.get("class", []),
                                   "index": index
                                   })
                    index = index + 1
            else:
                ch.attrs = merge_map(ch.attrs, ch.parent.attrs)
        return output

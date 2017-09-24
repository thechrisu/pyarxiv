"""
Scrapes the categories of arXiv.org and saves them into enums.
DO NOT USE THIS FILE IF YOU ARE NO MAINTAINER.
THIS FILE WILL GENERATE PYTHON CODE.
"""

from lxml import html
import os
import requests
import re

ARXIV_CATEGORIES_PAGE = "https://arxiv.org/help/api/user-manual"
ARXIV_CATEGORIES_FILE_PATH = "../pyarxiv/arxiv_categories.py"
ARXIV_CATEGORIES_TESTS_FILE_PATH = "../tests/test_arxiv_categories.py"
AUTOGENERATED_DISCLAIMER = "\"\"\"\n" \
                           "THIS FILE IS AUTOGENERATED.\n" \
                           "DO NOT MODIFY.\n" \
                           "INSTEAD, RUN scripts/scrape_categories.py\n" \
                           "\"\"\"\n\n"


def scrape_categories():
    p = requests.get(ARXIV_CATEGORIES_PAGE)
    content = html.fromstring(p.content)
    categories_table_caption = content.xpath(
        './/div/table/caption[text()="Table: Subject Classifications"]')
    assert len(categories_table_caption) == 1, \
        "Invalid length of categories table"
    categories_table = categories_table_caption[0].getparent()
    categories_trs = categories_table.findall('.//tr')
    category_list = []
    for e in categories_trs[1:]:
        category_name = re.sub('^\s+|\s+$|\n', '',
                               e.getchildren()[0].text)
        category_explanation = re.sub('^\s+|\s+$|\n', '',
                                      e.getchildren()[1].text)
        category_list.append((category_name, category_explanation))
    return category_list


def create_category_enum(categories):
    enum_file = AUTOGENERATED_DISCLAIMER + "from enum import Enum\n\n\n" \
                                           "class ArxivCategory(Enum):\n"
    category_mapping_dict = "arxiv_category_map = {\n"
    category_map_dict_items = []
    test_class = AUTOGENERATED_DISCLAIMER + \
        "import unittest\n\n" \
        "from pyarxiv.arxiv_categories import *\n\n\n" \
        "class TestArxivCategories(unittest.TestCase):\n"
    test_class += "    def test_categories(self):\n"
    for i, e in enumerate(categories):
        escaped_name = re.sub('-|\.', '_', e[0])
        enum_file += "    %s = %i  # %s\n" % (escaped_name,
                                              i + 1,
                                              e[1])
        category_map_dict_items.append("    ArxivCategory.%s: '%s'"
                                       % (escaped_name, e[0]))
        test_class += \
            "        self.assertEqual(\n" \
            "            arxiv_category_map[ArxivCategory.%s],\n" \
            "            '%s')\n" % (
                escaped_name, e[0])
    enum_file += "\n\n"
    category_mapping_dict += ',\n'.join(category_map_dict_items)
    category_mapping_dict += '\n}\n'
    usage_comment = "\n# print(arxiv_category_map[ArxivCategory.cs_AI])\n"

    if os.path.isfile(ARXIV_CATEGORIES_FILE_PATH):
        os.remove(ARXIV_CATEGORIES_FILE_PATH)
    f = open(ARXIV_CATEGORIES_FILE_PATH, 'w')
    f.write(enum_file + category_mapping_dict + usage_comment)
    f.close()

    main_func = "if __name__ == \"__main__\":\n    unittest.main()\n"
    if os.path.isfile(ARXIV_CATEGORIES_TESTS_FILE_PATH):
        os.remove(ARXIV_CATEGORIES_TESTS_FILE_PATH)
    f = open(ARXIV_CATEGORIES_TESTS_FILE_PATH, 'w')
    f.write(test_class + "\n" + main_func)
    f.close()


if __name__ == "__main__":
    categories = scrape_categories()
    create_category_enum(categories)

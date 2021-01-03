import pytest

# CMPT 370 Group 6 - Search Engine Test
# The tests right now consist of testing for all the possible inputs in the
# following functions: get_gender(), get_category, and get_subcategory().


def search(gender, category, subcategory):
    """
    This file takes in user input for gender, category, and subcategory from the GUI
    and returns all items that match all three of these filters in a list format.
    :param gender: The user's gender input
    :param category: The user's category input
    :param subcategory: The user's subcategory input
    :return: A list of all items that matched the sort filters
    """
    database = ["search_engine_test_data/accessories_men_cache.csv",
                "search_engine_test_data/accessories_women_cache.csv",
                "search_engine_test_data/bottoms_men_cache.csv",
                "search_engine_test_data/bottoms_women_cache.csv",
                "search_engine_test_data/footwear_men_cache.csv",
                "search_engine_test_data/footwear_women_cache.csv",
                "search_engine_test_data/overall_men_cache.csv",
                "search_engine_test_data/overall_women_cache.csv",
                "search_engine_test_data/tops_men_cache.csv",
                "search_engine_test_data/tops_women_cache.csv"]

    result_list = []
    for file in database:
        if gender.lower() in file:
            result_list.append(file)
            if category.lower() not in file:
                result_list.remove(file)

    results = []
    f = open(result_list[0], "r")
    eof = False
    while not eof:
        current_line = f.readline()
        if current_line == "":
            eof = True
        if subcategory.lower() in current_line.lower() or subcategory[0:-1].lower() in current_line.lower():
            results.append(current_line)

    return results


test_input = [("Men", "Tops", "Hoodies", 2),
              ("Men", "Bottoms", "Shorts", 24),
              ("Men", "Accessories", "Socks", 24),
              ("Women", "Overall", "Dress", 17),
              ("Women", "Accessories", "Bras", 24),
              ("Women", "Overall", "Jumpsuits", 5),
              ("Women", "Tops", "Crew", 19),
              ("Women", "Overall", "Skirt", 7),
              ("Men", "Bottoms", "Trousers", 18),
              ("Men", "Tops", "Shirts", 5)
              ]


@pytest.mark.parametrize("inputs", test_input)
def test_search(inputs):
    """
    Unit test some of the more common inputs for the search function.
    These tests are being ran on permanent data, so they should not fail
    should the cache storage files be updated.
    :param inputs: A tuple of three strings, ex. ("Men", "Tops", "Hoodies")
    :return: None
    """
    assert len(search(inputs[0], inputs[1], inputs[2])) == inputs[3], "Search returned the wrong amount of items."

# 370 Fall 2020: Scraper Software

# This file tests sorting_system.py

import pytest
import sorting_system

sample_input = [
    ["Aloha Long Sleeve T-Shirt", "Men", 35.95, 10.00, "WHITE (wht)", "https://www.billabong.com/en-ca/aloha-long-sleeve-t-shirt-194843166303.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4053bao_billabong,f_wht_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Geo Hawaii T-Shirt", "Men", 29.95, "N/A", "BLACK (blk) || DARK GREY HEATH (dgr)", "https://www.billabong.com/en-ca/geo-hawaii-t-shirt-194843057380.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4043bgh_billabong,f_blk_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Walled Long Sleeve T-Shirt", "Men", 37.95, "N/A", "COASTAL BLUE (cbu)", "https://www.billabong.com/en-ca/walled-long-sleeve-t-shirt-194843061080.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4053bwa_billabong,f_cbu_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Flamingo Palm T-Shirt", "Men", 29.95, "N/A", "LIGHT AQUA (laq) || OFF WHITE (ofw)", "https://www.billabong.com/en-ca/flamingo-palm-t-shirt-194843057182.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4043bfp_billabong,f_laq_frt1.jpg", "mens_tshirts", "Zillabong"],
    ["Lines Short Sleeve T-Shirt", "Men", 31.95, "N/A", "CHARCOAL (chr) || SILVER (sil)", "https://www.billabong.com/en-ca/lines-short-sleeve-t-shirt-194843174599.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4603bvh_billabong,f_chr_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Palm Grinch Short Sleeve T-Shirt", "Women", 39.95, 15.00, "OFF WHITE (ofw)", "https://www.billabong.com/en-ca/palm-grinch-short-sleeve-t-shirt-194843454288.html", "https://images.boardriders.com/global/billabong-products/all/default/small/abyzt00637_billabong,m_ofw_frt1.jpg", "mens_tshirts", "Billabong"]
]


def test_data_as_csv():
    """
    Tests that sorting_system.retrieve_data_as_csv() returns a filname
    and that all content is accounted for (excluding header)
    """
    filename = sorting_system.retrieve_data_as_csv(sample_input)
    assert filename == "results.csv"

    # Check contents
    f = open(filename)
    assert(len(list(f)) == 6)


def test_sort_results():
    """

    :return:
    """
    keys = ["Name", "Gender", "Price", "Sale Price", "Store"]

    for key in keys:
        if key == "Name":
            # Non reversed
            sorted_list = sorting_system.sort_results("results.csv", key, False)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[0] == "Aloha Long Sleeve T-Shirt"
            last_product = sorted_list[5]
            assert last_product[0] == "Walled Long Sleeve T-Shirt"

            # Reversed
            sorted_list = sorting_system.sort_results("results.csv", key, True)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[0] == "Walled Long Sleeve T-Shirt"
            last_product = sorted_list[5]
            assert last_product[0] == "Aloha Long Sleeve T-Shirt"

        elif key == "Gender":
            # Non reversed
            sorted_list = sorting_system.sort_results("results.csv", key, False)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[1] == "Men"
            last_product = sorted_list[5]
            assert last_product[1] == "Women"

            # Reversed
            sorted_list = sorting_system.sort_results("results.csv", key, True)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[1] == "Women"
            last_product = sorted_list[5]
            assert last_product[1] == "Men"

        elif key == "Price":
            # Non reversed
            sorted_list = sorting_system.sort_results("results.csv", key, False)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[2] == 29.95
            last_product = sorted_list[5]
            assert last_product[2] == 39.95

            # Reversed
            sorted_list = sorting_system.sort_results("results.csv", key, True)
            # Check first and last item after sort
            first_product = sorted_list[0]

            assert first_product[2] == 39.95
            last_product = sorted_list[5]
            assert last_product[2] == 29.95

        elif key == "Sale Price":
            # Non reversed
            sorted_list = sorting_system.sort_results("results.csv", key, False)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[3] == 10.00
            last_product = sorted_list[5]
            assert last_product[3] == "N/A"

            # Reversed
            sorted_list = sorting_system.sort_results("results.csv", key, True)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[3] == 15.0
            last_product = sorted_list[5]
            assert last_product[3] == "N/A"

        elif key == "Store":
            # Non reversed
            sorted_list = sorting_system.sort_results("results.csv", key, False)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[8] == "Billabong"
            last_product = sorted_list[5]
            assert last_product[8] == "Zillabong"

            # Reversed
            sorted_list = sorting_system.sort_results("results.csv", key, True)
            # Check first and last item after sort
            first_product = sorted_list[0]
            assert first_product[8] == "Zillabong"
            last_product = sorted_list[5]
            assert last_product[8] == "Billabong"


test_sort_results()
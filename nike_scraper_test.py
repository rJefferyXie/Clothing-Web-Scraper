from bs4 import BeautifulSoup
import nike_scraper as ns
import requests
import pytest

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/63.0.3239.132 Safari/537.36 "
}

# CMPT 370 Group 6 - Nike Scraper Test File
# This file performs unit tests along with a system test to make sure that
# the functions and website links are still valid and are behaving properly.

links_to_test = ["https://www.nike.com/ca/w/mens-tops-t-shirts-9om13znik1",
                 "https://www.nike.com/ca/w/mens-hoodies-sweatshirts-6riveznik1",
                 "https://www.nike.com/ca/w/mens-jackets-gilets-50r7yznik1",
                 "https://www.nike.com/ca/w/mens-shorts-38fphznik1",
                 "https://www.nike.com/ca/w/mens-trousers-tights-2kq19znik1",
                 "https://www.nike.com/ca/w/mens-tracksuits-1ll2wznik1",
                 "https://www.nike.com/ca/w/mens-jumpsuits-rompers-4w2rmznik1",
                 "https://www.nike.com/ca/w/mens-compression-baselayer-4pwbznik1",
                 "https://www.nike.com/ca/w/mens-socks-7ny3qznik1",
                 "https://www.nike.com/ca/w/womens-tops-t-shirts-5e1x6z9om13",
                 "https://www.nike.com/ca/w/womens-hoodies-sweatshirts-5e1x6z6rive",
                 "https://www.nike.com/ca/w/womens-jackets-gilets-50r7yz5e1x6",
                 "https://www.nike.com/ca/w/womens-trousers-tights-2kq19z5e1x6",
                 "https://www.nike.com/ca/w/womens-shorts-38fphz5e1x6",
                 "https://www.nike.com/ca/w/womens-bodysuits-2a768z5e1x6",
                 "https://www.nike.com/ca/w/womens-skirts-dresses-5e1x6z8y3qp",
                 "https://www.nike.com/ca/w/womens-tracksuits-1ll2wz5e1x6",
                 "https://www.nike.com/ca/w/womens-compression-baselayer-4pwbz5e1x6",
                 "https://www.nike.com/ca/w/womens-jumpsuits-rompers-4w2rmz5e1x6",
                 "https://www.nike.com/ca/w/womens-sports-bras-40qgmz5e1x6",
                 "https://www.nike.com/ca/w/womens-socks-5e1x6z7ny3q"
                 ]


@pytest.mark.parametrize('link', links_to_test)
def test_links(link):
    """
    Unit Test all of the links currently being used in the scraper to see if they are still valid.
    :param link: The current link being tested
    :return: None
    """
    assert requests.get(link, headers=header).status_code == 200, "Website not found."


def test_get_title():
    """
    With a pre downloaded html file, test the get_title() function.
    :return: title should be Nike F.C. Men's Sweatshirt Football Hoodie
    """
    with open("nike_data.html", "r", encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        first_item_container = soup.find("div", {"class": "product-card__body"})
        assert ns.get_title(first_item_container) == "Nike F.C. Men's Sweatshirt Football Hoodie", \
            "get_title() returned the wrong title."


def test_get_gender():
    """
    With a pre downloaded html file, test the get_gender() function.
    :return: gender should be Men
    """
    with open("nike_data.html", "r", encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        first_item_container = soup.find("div", {"class": "product-card__body"})
        title = ns.get_title(first_item_container)
        assert ns.get_target_gender(title) == "Men", "get_gender() returned the wrong gender."


def test_get_subcategory():
    """
    With a pre downloaded html file, test the get_subcategory() function.
    :return: subcategory should be Hoodie
    """
    with open("nike_data.html", "r", encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        first_item_container = soup.find("div", {"class": "product-card__body"})
        title = ns.get_title(first_item_container)
        assert ns.get_subcategory(title) == "Hoodie", "get_subcategory() returned the wrong subcategory."


def test_get_prices():
    """
    With a pre downloaded html file, test the get_title() function.
    :return: prices are $70.99, $100.00
    """
    with open("nike_data.html", "r", encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        first_item_container = soup.find("div", {"class": "product-card__body"})
        current_price, old_price = ns.get_prices(first_item_container)
        assert (current_price, old_price) == ("$70.99", "$100.00"), "get_prices() returned the wrong prices"


def test_get_image_link():
    """
    With a pre downloaded html file, test the get_item_image_link() function.
    :return: image link should be https://static.nike.com/a/images/t_PDP_1280_v1/f_auto/i1-e574055b-c204-4934-8068-ff90faef2ac3/fc-pullover-football-hoodie-nVN5ZF.jpg
    """
    with open("nike_item_data.html", "r", encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        assert ns.get_item_image_link(soup) == "https://static.nike.com/a/images/t_PDP_1280_v1/f_auto/i1-e574055b-c204-4934-8068-ff90faef2ac3/fc-pullover-football-hoodie-nVN5ZF.jpg", \
            "get_item_image_link did not return the correct link."


def test_get_colors():
    """
    With a pre downloaded html file, test the get_colors() function.
    :return: colors should be Black/White/White || Dark Atomic Teal/Black/Electric Orange || Game Royal/White/White
    """
    with open("nike_item_data.html", "r", encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, "lxml")
        assert ns.get_colors(soup) == "Black/White/White || Dark Atomic Teal/Black/Electric Orange || Game Royal/White/White", "get_colors did not return the correct colors."
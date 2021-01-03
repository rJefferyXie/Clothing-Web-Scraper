import requests
from bs4 import BeautifulSoup
import time

# CMPT 370 Group 6 - Nike Scraper
# This file uses BeautifulSoup and requests to scrape the Nike website
# for important information such as title, price, available colors, etc
# and writes them all to .csv files for easier consumption of the user.


def get_title(container):
    """
    Combine the title and subtitle for the current
    item and return it in string format.
    :param container: An item container that holds the item's information
    :return: A string of the item's Title and Subtitle.
    """
    try:
        title_container = container.findAll("div", {"class": "product-card__title"})
        subtitle_container = container.findAll("div", {"class": "product-card__subtitle"})
        title = title_container[0].text + " " + subtitle_container[0].text
    except (IndexError, AttributeError):
        title = "N/A"

    return title


def get_target_gender(title):
    """
    Check if the given item title contains keywords "Men" or "Women"
    and return target gender as the one that appears.
    :param title: A string of the item's Title and Subtitle.
    :return: The target gender of the item.
    """
    if "Men's" in title:
        return "Men"
    elif "Women's" in title:
        return "Women"
    else:
        return "Unisex"


def get_subcategory(title):
    """
    Compare each word in the title with a list of subcategories and return
    the first match to get subcategory.
    :param title: The title of the product as gathered by get_title().
    :return: subcategory as a string
    """
    categories = ["sweaters", "hoodies", "t-shirts", "jackets", "shirts", "crews", "jerseys", "tops", "polos", "tanks",
                  "compression", "baselayer", "jeans", "shorts", "skirts", "tights", "parkas", "gilets",
                  "pants", "leggings", "trousers", "joggers", "sweatpants",
                  "dresses", "rompers", "jumpsuits", "onesies", "overalls", "tracksuits",
                  "sneakers", "slippers", "sunglasses", "bras", "socks", "hats", "bags", "backpacks"]
    category = ""
    title_words = title.split(" ")
    for word in title_words:
        if word.lower() in categories or (word.lower() + "s") in categories:
            category = word

    return category


def get_prices(container):
    """
    Find the current price and if the item is on sale, also find the old price.
    Converts all prices into floats if they are not already in that format.
    :param container: An item container that holds the item's information
    :return: The current_price and old_price as a tuple
    """

    try:
        # The price(s) for each item
        price_container = container.findAll("div", {"class": "product-price__wrapper"})
        current_price = price_container[0].text
        old_price = "N/A"

        # Item is on sale
        if current_price.count("$") == 2:
            prices = current_price.split("$")
            # Convert prices to float if not already
            if "." not in prices[1]:
                current_price = prices[1] + ".00"
            else:
                current_price = "$" + prices[1]
            if "." not in prices[2]:
                old_price = "$" + prices[2] + ".00"

        # Item is not on sale
        else:
            # Convert each integer price to a float
            if "." not in current_price:
                current_price = current_price + ".00"
    except (IndexError, AttributeError):
        current_price = "N/A"
        old_price = "N/A"

    return current_price, old_price


def get_item_image_link(item_soup):
    """
    Find the url for the first image of the current item and return it.
    :param item_soup: An item's html information that was formatted by BeautifulSoup
    :return: The url of the first image of the current item
    """
    # The direct link to the item image
    try:
        item_image = item_soup.find("img", {"class": "css-viwop1 u-full-width u-full-height css-m5dkrx"})
        return item_image.get("src")
    except (IndexError, AttributeError):
        return "Click on item link for pictures."


def get_colors(item_soup):
    """
    Find the available colors for the given item and return them as a list.
    :param item_soup: An item's html information that was formatted by BeautifulSoup
    :return: A list of all available colors for the item
    """
    try:
        # If there is more than one color available
        # Add the current chosen color to list
        current_color_container = item_soup.findAll("div", {
            "class": "colorway-product-overlay colorway-product-overlay"
                     "--active colorway-product-overlay--selected css-sa2cc9"})
        if len(current_color_container) > 0:
            colors = current_color_container[0].findAll("img", alt=True)[0].get("alt")

            # A list of all color containers
            color_container = item_soup.findAll("div", {"class": "colorway-product-overlay css-sa2cc9"})
            for color_item in color_container:
                color_string = color_item.findAll("img", alt=True)
                if color_string[0].get("alt") != "Design your own Nike By You product":
                    colors = colors + " || " + (color_string[0].get("alt"))

        # If there is only one color available
        else:
            color_string = item_soup.findAll("li", {"class": "description-preview__color-description ncss-li"})
            colors = str(color_string).split(": ")[1].replace("</li>]", "")

    except (IndexError, AttributeError):
        colors = "Click on item link for available colors."

    return colors


def get_all_info(container):
    """
    Calls get_title, get_target_gender, get_prices, get_item_image_link, get_colors
    to get the important information for the current item.
    :param container: The item container for the current item
    :return: title, gender, current_price, old_price, item_link, image_link, and colors
    """

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    # Go through each item container
    title = get_title(container)
    gender = get_target_gender(title)
    current_price, old_price = get_prices(container)
    item_link = container.findAll("a", {"class": "product-card__link-overlay"})[0].get("href")
    subcategory = get_subcategory(title)

    # Getting item image and colors requires clicking on each item
    item_client = requests.get(item_link, headers=header)
    item_soup = BeautifulSoup(item_client.content, "lxml")
    item_image_link = get_item_image_link(item_soup)
    colors = get_colors(item_soup)

    return title, gender, current_price, old_price, colors, item_link, item_image_link, subcategory


def write_to_csv(category_links, categories):
    """
    Given the list of links for the subcategories of the men and women's clothing section of Nike,
    grab the product information such as price, colors available, item name, discounts, and item link.
    Then, write the information to a .csv file for easier reading and storage.

    :param category_links: A list of links for the subcategories of the men and women's clothing sections
    :param categories: A list of strings of all category names that will be used for naming the csv files
    :return: None, but the program should have created a .csv file for each subcategory of clothing.
    """

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }

    category_index = 0
    # Go through every sub category related to men and women's clothing
    for category in category_links:
        print("Starting section: " + categories[category_index])

        # Creating each .csv file
        category_name = categories[category_index]
        category_split = category_name.split("_")
        with open("nike_" + category_split[1] + "_" + category_split[0] + ".csv", "w") as f:
            headers = "Name, Gender, Price, Sale Price, Colors, Item Link, Image Link, Subcategory, Brand \n"
            f.write(headers)
            for link in category:
                category_client = requests.get(link, headers=header)
                category_soup = BeautifulSoup(category_client.content, "lxml")
                item_containers = category_soup.findAll("div", {"class": "product-card__body"})

                for container in item_containers:
                    title, gender, current_price, old_price, \
                        colors, item_link, image_link,  subcategory = get_all_info(container)

                    f.write(title + "," + gender + "," + str(current_price) + "," + str(old_price) +
                            "," + colors + ", " + item_link + ", " + image_link + "," + subcategory +
                            "," + "Nike" + "\n")

        print("Finished section: " + categories[category_index])
        category_index = category_index + 1


def main():
    """
    Using modules requests and BeautifulSoup, scrape the Nike website for the clothing sections
    of both men and women, creating a .csv file for each subcategory of the clothing sections.
    The program currently only grabs the lazily loaded products, and creates 21 different .csv files.

    :return: None
    """
    start_time = time.time()

    print("Starting to scrape Nike's website. Average runtime is around twenty minutes.")

    # A list of all of the clothing categories / links that will be searched
    clothing_links = ["https://www.nike.com/ca/w/mens-tops-t-shirts-9om13znik1",
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

    # A version of the links where they are grouped into similar categories,
    # this list correlates to the list below: categories
    clothing_category_links = [clothing_links[0:3],
                               clothing_links[3:5],
                               clothing_links[5:8],
                               [clothing_links[8]],
                               clothing_links[9:12],
                               clothing_links[12:14],
                               clothing_links[14:19],
                               clothing_links[19:21]
                               ]

    # A list of the generalized groups of categories. The indexes of this list
    # match with the index of the items in the above list: clothing_category_links
    categories = ["men_tops",
                  "men_bottoms",
                  "men_overall",
                  "men_accessories",
                  "women_tops",
                  "women_bottoms",
                  "women_overall",
                  "women_accessories"]

    write_to_csv(clothing_category_links, categories)

    time_taken = round(time.time() - start_time)
    time_minutes = time_taken // 60
    time_seconds = time_taken % 60
    print("Finished scraping Nike in", str(time_minutes) + " minutes and " + str(time_seconds) + " seconds.")


if __name__ == "__main__":
    main()

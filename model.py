# Model for Scraper GUI

import search_engine as se
import sorting_system
import view_product


class Model:
    """
    Stores all relevant data for the Scraper GUI
    """

    def __init__(self):
        """
        Constructor
        """
        # Data
        self.subscribers = []
        self.gender = ""
        self.category = ""
        self.subcategory = ""
        self.latest_sort_category = ""
        self.results = []
        self.favourites = []
        # iModel Content
        self.view_root = None
        self.view_limit = 15
        self.page = 0

    def add_subscriber(self, new_subscriber):
        """
        Assign new subscriber
        """
        self.subscribers.append(new_subscriber)

    def notify_subscribers(self):
        """
        Prompt subscribers to update
        """
        for subscriber in self.subscribers:
            subscriber.update()

    def set_view_root(self, frame):
        """
        Store root from which all GUI element descend
        """
        self.view_root = frame

    def set_gender(self, gender_selection):
        """
        Store gender selected by user in search
        """
        self.gender = gender_selection

    def set_category(self, category_selection):
        """
        Store category selected by user in search
        """
        self.category = category_selection

    def set_subcategory(self, subcategory_selection):
        """
        Store subcategory selected by user in search
        """
        self.subcategory = subcategory_selection

    def get_gender(self):
        """
        Retrieve stored search parameter: gender
        :return: string
        """
        return self.gender

    def get_category(self):
        """
        Retrieve stored search parameter: category
        :return: string
        """
        return self.category

    def get_subcategory(self):
        """
        Retrieve stored search parameter: subcategory
        :return: string
        """
        return self.subcategory

    def get_latest_sort_category(self):
        """
        Retrieve stored search parameter: latest sort key
        :return: string
        """
        return self.latest_sort_category

    def get_view_root(self):
        """
        Retrieve GUI root
        :return: tk.TK
        """
        return self.view_root

    def get_items_per_page(self):
        """
        Retrieve how many items are to be displayed on each page
        :return: int
        """
        return self.view_limit

    def get_favourites(self):
        """
        Retrieve list of favourite products
        :return: tuple where len(tuple) = 9
        """
        return self.favourites

    def get_results(self):
        """
        Retrieve products that resulted from searching from the
        stored search parameters
        :return: list of products, each product is a list
        """
        return self.results

    def get_page_number(self):
        """
        Retrieve current page number
        :return: int
        """
        return self.page

    def fetch_results(self):
        """
        Use stored search parameters to find relevant products from data
        :result: stores products that fit parameters in self.results
        """
        results = se.search(self.gender, self.category, self.subcategory)
        list_of_results = []

        for result in results:
            result = result.rstrip("\n")
            result = result.split(",")

            self.clean_data(result)

            if "Not Found" not in result:
                list_of_results.append(result)

        # Update stored results
        self.results = list_of_results

        for subscriber in self.subscribers:
            if isinstance(subscriber, view_product.ProductView):
                subscriber.run()

    def clean_data(self, result):
        """
        Takes a product result and cleans up data;
        e.g. remove spaces, concatenate link pieces, concatenate name pieces,
        and convert prices into floats after removing the $.
        :param result: (list) product attributes
        :return: clean result
        """
        # Account for image links containing commas
        if len(result) > 9:

            # Adjustment for Billabong
            if result[-1] == "Billabong":
                result[6] += ',' + result[7]
                result[6] = result[6][1:-1]
                result.pop(7)

            # Adjustment for H&M
            if result[-1] == "H&M":
                image_link_components = []
                # Get pieces of image url
                for i in range(6, 12):
                    image_link_components.append(result[i])
                # Stitch url
                for component in image_link_components:
                    result[6] += ',' + component
                # Adjust result
                first_half = result[0:7]
                second_half = result[12:]
                first_half.extend(second_half)
                result = first_half
                result[6] = result[6][1:-1]

        # Clean up spaces
        for i in range(len(result)):
            # Remove spaces
            if not isinstance(result[i], float):
                term = result[i].lstrip()
                result[i] = term

        # Check for commas in names
        result_length = len(result)
        if result_length > 9:
            # This check exists due to names like "But first, coffee"
            shifted = result_length - 9
            # Collect and stitch pieces of the name
            name_pieces = []
            for i in range(0, shifted + 1):
                name_pieces.append(result[i])
            # Stitch name
            name = ""
            for component in name_pieces:
                name += " " + component
                result.remove(component)
            # Adjust result
            result.insert(0, name)

        # Remove dollar signs and convert prices to floats
        if not isinstance(result[2], float):
            result[2] = result[2].lstrip("$")
            result[2] = float(result[2])
        if not isinstance(result[3], float):
            try:
                result[3] = result[3].lstrip("$")
                result[3] = float(result[3])
            except ValueError:
                pass

        return result

    def sort_data(self, sort_option):
        """
        This employs the sorting_system function sort_results()
        :param sort_option: (tuple) category to sort by, reversed (True or False)
        :return: N/A
        """
        # filename will always be "results.csv" as specified in sorting_system,py
        filename = sorting_system.retrieve_data_as_csv(self.results)
        for i in self.results:
            self.clean_data(i)

        self.results = sorting_system.sort_results(filename, sort_option[0], sort_option[1])
        self.latest_sort_category = sort_option[0]

        # Return to 1st page
        self.page = 0

        self.notify_subscribers()

    def add_to_favourites(self, item_info):
        """
        Add item information into favorite list
        :param item_info: tuple of three strings: Name, price, and item link of the product
        :return: N/A
        """
        information = []

        for item in item_info:
            information.append(str(item))
        # if item is not already in favorites list, append it
        if information not in self.favourites:
            self.favourites.append(information)
            return True
        else:
            return False

    def delete_from_favourites(self, item_link):
        """
        Delete an item from favorites list.
        Calls the check_favorites() function.
        :param item_link: The link for the item that is to be deleted
        :return: Boolean, describes whether item was in list and deleted
        """
        for item in self.favourites:
            if item_link in item:
                item_name = item[0]
                self.favourites.remove(item)
                return item_name

        return None

    def search_to_front(self):
        """
        Bring the root view (the search view) to the front
        :return: N/A
        """
        self.view_root.attributes("-topmost", True)
        self.view_root.attributes("-topmost", False)

    def increment_page(self):
        """
        Update page number to next page
        :return: N/A
        """
        if len(self.results) // self.view_limit > self.page:
            self.page += 1
            self.notify_subscribers()

    def decrement_page(self):
        """
        Update page number to previous page
        :return: N/A
        """
        if self.page > 0:
            self.page -= 1
            self.notify_subscribers()

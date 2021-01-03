# Controller for Scraper GUI


class Controller:
    """
    Passes information to model when relevant actions are taken
    in ProductView.
    """

    def __init__(self):
        """
        Constructor
        """
        self.model = None

    def add_model(self, new_model):
        """
        Assign model
        """
        self.model = new_model

    def update_search_parameters(self, selected_gender, selected_category, selected_subcategory):
        """
        Pass parameters selected by user to the model
        :return: N/A
        """
        self.model.set_gender(selected_gender)
        self.model.set_category(selected_category)
        self.model.set_subcategory(selected_subcategory)
        self.model.fetch_results()

    def sort_results(self, sort_option):
        """
        Prompts model to sort results by specified sort parameters
        param: sort_option: (tuple) category to sort by, reversed (True or False)
        :return: N/A
        """
        self.model.sort_data(sort_option)

    def update_favourites(self, item_info, status):
        """
        Alert model that user can indicated a change in favourite items
        :param item_info: (product_name, product_gender, product_price,
        product_sale_price, product_colors, product_link, product_image_link, product_store)
        :param status: (String) Add or Remove
        :return: Boolean: success status of the operation
        """
        if status == "Add":
            return self.model.add_to_favourites(item_info)
        elif status == "Remove":
            return self.model.delete_from_favourites(item_info)

    def change_page(self, direction):
        """
        Alert model that user had indicated a change in page
        :param direction: (str) "right" (for next) or "left" (for previous)
        :return: N/A
        """
        if direction == "right":
            self.model.increment_page()
        else:
            self.model.decrement_page()

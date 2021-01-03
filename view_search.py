# Search View for Scraper GUI

import listener
import tkinter as tk
import tkinter.font as tkFont


class SearchView(listener.Listener):
    """
    Display search parameter selection fields for user
    """

    def __init__(self):
        """
        Constructor
        """
        listener.Listener.__init__(self)
        self.model = None
        self.controller = None
        self.frame = None
        self.gender_identifier = ""
        self.category_identifier = ""
        self.subcategory_identifier = ""
        self.subcategory_button = None

    def submit_selections(self):
        """
        Pass values currently stored in selectors to controller
        to update model.
        :return: N/A
        """
        # Check for any unselected items; they default to "All"
        if self.gender_identifier.get() == "Select Gender.":
            self.gender_identifier.set("All")
        if self.category_identifier.get() == "Select Category.":
            self.category_identifier.set("All")
        if self.subcategory_identifier.get() == "Select Subcategory.":
            self.subcategory_identifier.set("All")
        self.controller.update_search_parameters(self.gender_identifier.get(),
                                                 self.category_identifier.get(),
                                                 self.subcategory_identifier.get())

    def create_buttons(self, parent_frame):
        """
        Build dropdown buttons to be used in selecting search parameters.
        Buttons are stored on self.parent_frame.
        :return: N/A
        """
        genders = ["Men", "Women", "All"]
        categories = ["Tops", "Bottoms", "Overall", "Footwear", "Accessories", "All"]
        subcategories = ["All"]

        self.gender_identifier = tk.StringVar(parent_frame)
        self.gender_identifier.set("Select Gender.")
        gender_choices = tk.OptionMenu(parent_frame, self.gender_identifier, *genders)
        gender_choices.pack()

        self.category_identifier = tk.StringVar(parent_frame)
        self.category_identifier.set("Select Category.")
        self.category_identifier.trace("w", lambda name, index, mode, var=self.category_identifier: self.set_subcategory_button())
        category_choices = tk.OptionMenu(parent_frame, self.category_identifier, *categories)
        category_choices.pack()

        self.subcategory_identifier = tk.StringVar(parent_frame)
        self.subcategory_identifier.set("Select Subcategory.")
        subcategory_choices = tk.OptionMenu(parent_frame, self.subcategory_identifier, *subcategories)
        self.subcategory_button = subcategory_choices
        subcategory_choices.pack()

        submit_button = tk.Button(parent_frame, text='Submit', command=self.submit_selections)
        submit_button.pack()

    def set_subcategory_button(self):
        """
        Set subcategory button in accordance with what is displayed in
        the category button.
        :return: N/A
        """
        # .get() required to retrieve value from tk.StringVar
        selected_category = self.category_identifier.get()

        # Reset display on button
        self.subcategory_identifier.set("Select Subcategory.")

        if selected_category == "Tops":
            subcategories = ["Sweaters", "Hoodies", "T-Shirts", "Jackets", "Shirts",
                             "Crews", "Jerseys", "Tops", "Polos", "Tanks", "Parkas", "Gilets"]
        elif selected_category == "Bottoms":
            subcategories = ["Jeans", "Shorts", "Skirts", "Tights", "Pants",
                             "Leggings", "Trousers", "Joggers", "Sweatpants"]
        elif selected_category == "Overall":
            subcategories = ["Dresses", "Rompers", "Jumpsuits", "Onesies",
                             "Overalls", "Tracksuits", "Compression and Baselayer"]
        elif selected_category == "Footwear":
            subcategories = ["Sneakers", "Slippers", "Socks"]
        elif selected_category == "Accessories":
            subcategories = ["Sunglasses", "Bras", "Socks", "Hats", "Bags", "Backpacks"]
        elif selected_category == "All":
            subcategories = ["Sweaters", "Hoodies", "T-Shirts", "Jackets", "Shirts",
                             "Crews", "Jerseys", "Tops", "Polos", "Tanks", "Parkas",
                             "Gilets", "Jeans", "Shorts", "Skirts", "Tights", "Pants",
                             "Leggings", "Trousers", "Joggers", "Sweatpants", "Dresses",
                             "Rompers", "Jumpsuits", "Onesies", "Overalls", "Tracksuits",
                             "Compression and Baselayer", "Sneakers", "Slippers", "Socks",
                             "Sunglasses", "Bras", "Socks", "Hats", "Bags", "Backpacks",
                             "All"]
        else:
            subcategories = []

        self.subcategory_button['menu'].delete("0", tk.END)
        for item in subcategories:
            self.subcategory_button['menu'].add_command(label=item, command=tk._setit(self.subcategory_identifier, item))

    def add_model(self, new_model):
        """
        Assign model
        """
        self.model = new_model

    def add_controller(self, new_controller):
        """
        Assign controller
        """
        self.controller = new_controller

    def draw(self, parent_frame):
        """
        Build SearchView
        """
        # if self.active:
        self.frame = parent_frame

        # Add product label
        font_style = tkFont.Font(family="Times", size=50)
        name = tk.Label(self.frame, text="370 Scraper", font=font_style, padx=10, pady=10)
        name.pack()

        self.create_buttons(parent_frame)
        self.frame.mainloop()


if __name__ == "__main__":
    search_view = SearchView()
    search_view.update()

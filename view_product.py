# Product View for Scraper GUI

import listener
from tkinter import messagebox
import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import view_feedback


class ProductView(listener.Listener):
    """
    Display products that match the user's search parameters
    """
    def __init__(self):
        """
        Constructor
        """
        listener.Listener.__init__(self)
        # MVC Components
        self.model = None
        self.controller = None
        # Size variables
        self.x_window_dimension = 900
        self.y_window_dimension = 600
        self.x_frame_dimension = 300
        self.y_frame_dimension = 200
        self.padding = 10
        self.items_per_row = self.x_window_dimension // self.x_frame_dimension
        # Window variables
        self.local_root = None
        self.interior_frame = None
        self.display_canvas = None
        self.favorite_root = None
        self.favorite_frame = None
        self.favorite_canvas = None
        # Track extend of update necessary when model notifies subscribers
        self.latest_sort = ""

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

    def menu_sort_data(self, sort_option):
        """
        This employs the sorting_system function sort_results()
        :param sort_option: The way that the information is being sorted
        :return: N/A
        """
        self.controller.sort_results(sort_option)

    def menu_new_search(self):
        """
        When fully merged, this function will initiate the previous view
        :return: closes results window and opens search window
        """
        self.model.search_to_front()

    def open_link(self, link):
        """
        This function correlates to the button object created for each item.
        If the user clicks on an image, it opens the website associated with the image.
        """
        webbrowser.open(link)

    def create_result_row(self, parent_frame, results, screen):
        """
        Creates a frame to demonstrate a row of three products
        :param parent_frame: canvas for GUI element
        :param results: (list) of results to be included in frame
        :param screen: Either the main screen or the favorites screen
        :return: populated frame
        """
        # Create frame
        row_frame = tk.Frame(parent_frame, width=self.x_window_dimension, height=self.y_frame_dimension)
        row_frame.pack()

        position = 0
        for product in results:
            self.create_result_frame(row_frame, product, position, screen)
            position += 1

    def create_result_frame(self, parent_frame, product, row_position, screen):
        """
        Creates new frame and populates it with result data
        :param parent_frame: canvas for GUI element
        :param product:
        :param row_position:
        :param screen: Either the main screen or the favorites screen
        :return: populated frame
        """
        # Create frame
        frame = tk.Frame(parent_frame, width=self.x_frame_dimension, height=self.y_frame_dimension,
                         bd=2, highlightbackground="black", highlightthickness=1)
        frame.grid(row=0, column=row_position)

        # Get attributes
        product_name = product[0]
        product_gender = product[1]
        product_price = product[2]
        # Add $ for display, but do not add it again if adding to favourites
        if screen != "favorites":
            if not str(product_price)[0] == "$":
                product_price = "$" + str(product[2])
            else:
                product_price = str(product[2])
        product_sale_price = product[3]
        if product_sale_price != "N/A":
            if not str(product_sale_price)[0] == "$":
                product_sale_price = "$" + str(product_sale_price)

        product_colors = product[4].replace("||", ", ")
        product_store = product[-1]
        product_link = product[5]
        product_image_link = product[6]
        if product_image_link[0] == '"':
            product_image_link = product_image_link[1:-1]

        photo_frame = tk.Frame(frame, width=self.x_frame_dimension, height=self.y_frame_dimension)
        # Create the PhotoImage object
        image1 = requests.get(product_image_link)
        pil_image = Image.open(BytesIO(image1.content))
        pil_image = pil_image.resize((100, 100), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(pil_image)

        # Create labels
        name_label = tk.Label(frame, text=product_name)
        gender_label = tk.Label(frame, text=product_gender)
        price_label = tk.Label(frame, text=product_price)
        sale_label = tk.Label(frame, text=product_sale_price)
        colors_label = tk.Label(frame, text=product_colors)
        store_label = tk.Label(frame, text=product_store)

        image_frame = tk.Button(photo_frame, image=image, command=lambda item_url=product_link: self.open_link(item_url))
        image_frame.image = image

        if screen == "favorites":
            favorite_button = tk.Button(frame, text="Remove from Favorite",
                                        command=lambda item_info=product_link: self.delete_from_favorites(item_info))
            favorite_button.place(x=self.x_frame_dimension / 2 - 10, y=135)
        else:
            favorite_button = tk.Button(frame, text="Add to Favorite", command=lambda item_info=(
                product_name, product_gender, product_price, product_sale_price, product_colors, product_link,
                product_image_link, product_store): self.add_to_favorite(item_info))
            favorite_button.place(x=self.x_frame_dimension / 2 + 5, y=135)

        # Position labels
        name_label.place(x=0, y=0)
        gender_label.place(x=0, y=self.y_frame_dimension / 6)
        store_label.place(x=0, y=self.y_frame_dimension / 6 * 2)
        price_label.place(x=0, y=self.y_frame_dimension / 6 * 3)
        sale_label.place(x=0, y=self.y_frame_dimension / 6 * 4)
        colors_label.place(x=0, y=self.y_frame_dimension / 6 * 5)
        image_frame.place(x=self.x_frame_dimension / 2, y=25)

        photo_frame.pack()

    def populate_screen(self, frame):
        """
        Creates the window frames and rows for the current screen. Data is
        housed in the model.
        :param frame: The master frame that the information is being put on.
        :return: None
        """
        page_number = self.model.get_page_number()
        current_data = self.model.get_results()
        items_per_page = self.model.get_items_per_page()

        # Get relevant data for page
        try:
            data_on_page = current_data[page_number * items_per_page: (page_number + 1) * items_per_page]
        except IndexError:
            data_on_page = current_data[page_number * items_per_page: len(current_data)]

        # Group products in sets of 3
        for i in range(0, len(data_on_page), self.items_per_row):
            if i < items_per_page:
                results_section = data_on_page[i:i + self.items_per_row]
                self.create_result_row(frame, results_section, "Main")

    def clear_frame(self, frame):
        """
        Clears the current frame and destroys all children + forgets its frames
        :param frame: The current frame to be cleared
        :return: None
        """
        for f in tk.Frame(frame).winfo_children():
            f.destroy()

        tk.Frame(frame).pack_forget()

    def add_to_favorite(self, item_info):
        """
        Add item information into favorite list
        :param item_info: tuple of three strings: Name, price, and item link of the product
        :return: None
        """
        success_status = self.controller.update_favourites(item_info, "Add")

        if success_status is True:
            messagebox.showinfo("Notification", f"{item_info[0]} added to favorite list!", parent=self.local_root)
            # If the favorites window is open while user is attempting
            # to add to favorites, close and update the screen.
            try:
                if "normal" == self.favorite_root.state():
                    self.favorite_root.destroy()
                    self.display_favorites()
            # If the window is closed, just add to favorites list
            except:
                pass
        else:
            messagebox.showinfo("Notification", f"{item_info[0]} already in favorite list!", parent=self.local_root)

    def delete_from_favorites(self, item_link):
        """
        Send notification to model to delete an item from favorites list.
        Update the display as necessary. Calls the display_favorites() function.
        :param item_link: The link for the item that is to be deleted
        :return: None
        """
        item_name = self.controller.update_favourites(item_link, "Remove")
        if item_name is not None:
            messagebox.showinfo("Notification", f"{item_name} removed from favorite list!", parent=self.local_root)

        favorite_list = self.model.get_favourites()
        # Manage favourites popup
        if len(favorite_list) > 0:
            self.favorite_root.destroy()
            self.display_favorites()
        else:
            self.favorite_root.destroy()

    def display_favorites(self):
        """
        Creating a new window when accessing Favorites.
        Calls a modified version of the populate_screen() function.
        :return: None
        """
        self.favorite_root = tk.Toplevel()
        self.favorite_root.title("Your Favorites")
        self.favorite_root.minsize(self.x_window_dimension, self.y_window_dimension)
        self.favorite_root.geometry(f"{self.x_window_dimension}x{self.y_window_dimension}")

        self.favorite_frame = tk.Frame(self.favorite_root)
        self.favorite_frame.pack(fill=tk.BOTH, expand=1)

        self.favorite_canvas = tk.Canvas(self.favorite_frame)
        self.favorite_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Add scrollbar
        scrollbar = tk.Scrollbar(self.favorite_frame, orient=tk.VERTICAL, command=self.favorite_canvas.yview)
        scrollbar.configure(command=self.favorite_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas
        self.favorite_canvas.configure(yscrollcommand=scrollbar.set)
        # (e): passing mouse event
        self.favorite_canvas.bind('<Configure>',
                                  lambda e: self.favorite_canvas.configure
                                  (scrollregion=self.favorite_canvas.bbox("all")))

        # Create the window for the canvas
        interior_favorite_frame = tk.Frame(self.favorite_canvas)
        self.favorite_canvas.create_window((0, 0), window=interior_favorite_frame, anchor="nw")

        # Create the screen and separate the data into their own columns
        favorite_list = self.model.get_favourites()
        for i in range(0, len(favorite_list), self.items_per_row):
            results_section = favorite_list[i:i + self.items_per_row]
            self.create_result_row(interior_favorite_frame, results_section, "favorites")

        self.favorite_root.mainloop()

    def next_page(self):
        """
        Alert controller that user want to go to the next page
        """
        self.controller.change_page("right")

    def prev_page(self):
        """
        Alert controller that user want to go to the next page
        """
        self.controller.change_page("left")

    def user_feedback(self):
        """
        Creates new window with feedback GUI
        """
        feedback_window = view_feedback.FeedbackView()
        feedback_window.open(tk.Toplevel())

    def update(self):
        """
        Refresh view
        """
        most_recent_sort = self.model.get_latest_sort_category()
        if most_recent_sort != self.latest_sort:
            for f in self.interior_frame.winfo_children():
                f.pack_forget()
            self.populate_screen(self.interior_frame)
            messagebox.showinfo("Notification", f"Items has been sorted by {str(most_recent_sort).lower()}",
                                parent=self.local_root)
            self.latest_sort = most_recent_sort
        else:
            for f in self.interior_frame.winfo_children():
                f.pack_forget()
            self.populate_screen(self.interior_frame)
        self.display_canvas.yview_moveto(0.0)

    def run(self):
        """
        Start building the ProductView
        """
        parent_frame = self.model.get_view_root()
        self.draw(parent_frame)

    def draw(self, parent_frame):
        """
        Builds components associated with the product display
        :param parent_frame: GUI root to which the search view is tied.
        """
        if self.local_root is not None:
            self.local_root.destroy()

        self.local_root = tk.Toplevel(parent_frame)
        root = self.local_root
        root.title("Search Results")
        root.minsize(self.x_window_dimension, self.y_window_dimension)
        root.geometry(f"{self.x_window_dimension}x{self.y_window_dimension}")
        # Create menu
        menu = tk.Menu(root)
        root.config(menu=menu)
        # Previous Page
        prev_page_menu = tk.Menu(menu)
        menu.add_cascade(label="Previous Page", menu=prev_page_menu)
        prev_page_menu.add_command(label="Previous Page", command=self.prev_page)
        # Next Page
        next_page_menu = tk.Menu(menu)
        menu.add_cascade(label="Next Page", menu=next_page_menu)
        next_page_menu.add_command(label="Next Page", command=self.next_page)
        # Create menu items
        main_menu = tk.Menu(menu)
        menu.add_cascade(label="Options", menu=main_menu)
        main_menu.add_command(label="New Search", command=lambda: self.menu_new_search())
        # Create menu items
        sort_menu = tk.Menu(menu)
        menu.add_cascade(label="Sort", menu=sort_menu)
        sort_menu.add_command(label="Name - a-z", command=lambda option=("Name", False): self.menu_sort_data(option))
        sort_menu.add_command(label="Name - z-a", command=lambda option=("Name", True): self.menu_sort_data(option))
        # sort_menu.add_command(label="Gender", command=lambda option=("Gender", False): self.menu_sort_data(option))
        sort_menu.add_command(label="Price - Lowest to Highest",
                              command=lambda option=("Price", False): self.menu_sort_data(option))
        sort_menu.add_command(label="Price - Highest to Lowest",
                              command=lambda option=("Price", True): self.menu_sort_data(option))
        sort_menu.add_command(label="Discount Price - Lowest to Highest",
                              command=lambda option=("Sale Price", False): self.menu_sort_data(option))
        sort_menu.add_command(label="Discount Price - Highest to Lowest",
                              command=lambda option=("Sale Price", True): self.menu_sort_data(option))
        # sort_menu.add_command(label="Store", command=lambda option=("Store", False): self.menu_sort_data(option))
        favorite_menu = tk.Menu(menu)
        menu.add_cascade(label="Favorites", menu=favorite_menu)
        favorite_menu.add_command(label="Favorites List", command=self.display_favorites)
        # Feedback
        feedback_menu = tk.Menu(menu)
        menu.add_cascade(label="Feedback", menu=feedback_menu)
        feedback_menu.add_command(label="Submit Feedback", command=self.user_feedback)

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)
        # Create canvas
        display_canvas = tk.Canvas(main_frame)
        self.display_canvas = display_canvas
        display_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        # Add scrollbar
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar.configure(command=display_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Configure canvas
        display_canvas.configure(yscrollcommand=scrollbar.set)
        # (e): passing mouse event
        display_canvas.bind('<Configure>',
                            lambda e: display_canvas.configure
                            (scrollregion=display_canvas.bbox("all")))
        # Populate canvas (requires additional frame for all contents)
        self.interior_frame = tk.Frame(display_canvas)
        display_canvas.create_window((0, 0), window=self.interior_frame, anchor="nw")
        self.populate_screen(self.interior_frame)

        self.local_root.mainloop()

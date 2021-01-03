# Main file to run Scraper GUI

import model
import controller
import view_feedback
import view_product
import view_search
import tkinter as tk


def main():
    """
    Run this file to run the program
    """
    # Create elements
    model_main = model.Model()
    controller_main = controller.Controller()
    feedback_view = view_feedback.FeedbackView()
    product_view = view_product.ProductView()
    search_view = view_search.SearchView()

    # Connect elements
    model_main.add_subscriber(product_view)

    controller_main.add_model(model_main)

    product_view.add_model(model_main)
    search_view.add_model(model_main)

    feedback_view.add_controller(controller_main)
    product_view.add_controller(controller_main)
    search_view.add_controller(controller_main)

    # Create root
    root = tk.Tk()
    root.title("Scraper")
    # Window dimensions
    root.minsize(900, 600)
    root.geometry("900x600")
    model_main.set_view_root(root)

    # Create menu
    # menu = tk.Menu(root)
    # root.config(menu=menu)
    #
    # # Create menu items
    # main_menu = tk.Menu(menu)
    # menu.add_cascade(label="Options", menu=main_menu)
    #main_menu.add_command(label="New Search", command=menu_new_search())

    # Create a frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # Open search view
    search_view.draw(main_frame)

    root.mainloop()


if __name__ == "__main__":
    main()

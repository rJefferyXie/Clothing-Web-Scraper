# Feedback View for Scraper GUI

import listener
import user_feedback
import tkinter as tk
import tkinter.messagebox


class FeedbackView(listener.Listener):
    """
    Display fields for user to submit feedback
    """

    def __init__(self):
        """
        Constructor
        """
        listener.Listener.__init__(self)
        self.model = None
        self.controller = None
        self.local_root = None
        self.email_var = None
        self.subject_var = None

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

    def set_window_position(self, window):
        """
        Specify location of window upon build
        :param window: tk.Frame, root for FeedbackView
        """
        window_width = 400
        window_height = 200
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2) - 100
        window.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))

    def submit_feedback(self, text_holder):
        """
        Pass data from user to user_feedback to handle transfer of data
        by email to theh admin account.
        :param text_holder: tk.Text, holds feedback message
        :return: N/A
        """
        email = self.email_var.get()
        subject = self.subject_var.get()
        message = text_holder.get("1.0", tk.END).strip()
        if message != "":
            user_feedback.send_mail_GUI(email, subject, message, to_emails=["370scraper2020@gmail.com"])
            tk.messagebox.showinfo('Notifications', 'Feedback submitted successfully', parent=self.local_root)
            self.email_var.set("")
            self.subject_var.set("")
            text_holder.delete("1.0", tk.END)
        else:
            tk.messagebox.showinfo('Error', 'Please enter your feedback.', parent=self.local_root)

    def open(self, parent_frame):
        """
        Builds FeedbackView
        :param parent_frame: tk.Frame passed in as root for FeedbackView
        """
        if parent_frame is not None:
            root = parent_frame
        else:
            root = tk.Tk()
            root.title("Submit Feedback")

        # Update variables in init
        self.local_root = root
        self.email_var = tk.StringVar()
        self.subject_var = tk.StringVar()

        email_frame = tk.Frame(root)
        subject_frame = tk.Frame(root)
        message_frame = tk.Frame(root)
        submit_button = tk.Button(root, text="Submit")
        # needed to add more here
        email_label = tk.Label(email_frame, text="Enter Email").grid(row=0, column=0, padx=15, pady=10)
        subject_label = tk.Label(subject_frame, text="Enter Subject").grid(row=0, column=0, padx=13, pady=10)
        message_label = tk.Label(message_frame, text="Enter Message\n(required)").grid(row=0, column=0, padx=10,
                                                                                       pady=10)
        email_text_box = tk.Entry(email_frame, textvariable=self.email_var).grid(row=0, column=1, padx=15, pady=10, ipadx=76)
        subject_text_box = tk.Entry(subject_frame, textvariable=self.subject_var).grid(row=0, column=1, padx=10, pady=10,
                                                                                  ipadx=76)
        message_text_box = tk.Text(message_frame, width=34, height=4)
        submit_button.configure(command=lambda: self.submit_feedback(message_text_box))
        message_text_box.grid(row=0, column=1, padx=10, pady=10)
        email_frame.pack(fill='x')
        subject_frame.pack(fill='x')
        message_frame.pack(fill='x')
        submit_button.pack()

        self.set_window_position(root)
        root.mainloop()

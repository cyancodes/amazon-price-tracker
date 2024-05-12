from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Constants
BG_COLOUR_1 = "white"
COLOR_1 = "#B3C8CF"
COLOR_2 = "#BED7DC"
COLOR_3 = "#F1EEDC"
COLOR_4 = "#E5DDC5"

FONT_FAMILY = "Calibri"

BUTTONS_FONT = (FONT_FAMILY, 12, "bold")  # Headings
NORMAL_TEXT_FONT = (FONT_FAMILY, 10, "normal")  # Text
LABELS_FONT = (FONT_FAMILY, 15, "bold")  # Buttons


class GUI:
    def __init__(self, item_manager):
        self.item_manager = item_manager

        # Window
        self.window = Tk()
        self.window.title("Price Tracker")
        self.window.config(bg=COLOR_3, padx=20, pady=20)

        # ------------------Left Canvas------------------ #
        self.canvas_left = self.canvas_maker(width=400, height=520, column=0, row=0)

        # --- Items --- #
        # Items Label
        self.current_items_label = self.canvas_left.create_text(25, 25, anchor=NW, font=LABELS_FONT, text="Items")

        # Items List Box
        self.current_listbox_item = ""  # Sets to noting, to prevent anything being deleted when the script is first run
        self.current_items_listbox = Listbox(self.canvas_left, selectmode=SINGLE, height=10,
                                             highlightthickness=3, highlightcolor=COLOR_3, highlightbackground=COLOR_3)
        self.populate_listbox()

        # This code is triggered when an entry in the list is selected, triggering the update price function
        self.current_items_listbox.bind(
            "<<ListboxSelect>>",
            lambda e: self.listbox_select()
        )
        self.current_items_listbox_window = self.canvas_left.create_window(25, 60, height=190, width=335, anchor=NW,
                                                                           window=self.current_items_listbox)

        # --- Manage Items --- #
        # Manage Items Label
        self.manage_items_label = self.canvas_left.create_text(25, 275, anchor=NW, font=LABELS_FONT,
                                                               text="Manage Items")

        # Name Entry
        self.name_entry_label, self.name_entry, self.canvas_left_edit_name_window = (
            self.entry_maker(canvas=self.canvas_left, label_x=25, label_y=305, anchor=NW, label_font=NORMAL_TEXT_FONT,
                             label_text="Name",
                             entry_bg="white", entry_font=NORMAL_TEXT_FONT,
                             window_x=25, window_y=325, window_height=0, window_width=335))

        # URL Entry
        self.url_entry_label, self.url_entry, self.canvas_left_edit_url_window = (
            self.entry_maker(canvas=self.canvas_left, label_x=25, label_y=355, anchor=NW, label_font=NORMAL_TEXT_FONT,
                             label_text="URL",
                             entry_bg="white", entry_font=NORMAL_TEXT_FONT,
                             window_x=25, window_y=375, window_height=0, window_width=335))

        # Cutoff Entry
        self.cutoff_entry_label, self.cutoff_entry, self.canvas_left_edit_cutoff_window = (
            self.entry_maker(canvas=self.canvas_left, label_x=25, label_y=405, anchor=NW, label_font=NORMAL_TEXT_FONT,
                             label_text="Cutoff",
                             entry_bg="white", entry_font=NORMAL_TEXT_FONT,
                             window_x=25, window_y=425, window_height=0, window_width=335))
        # Update Button
        self.update_button, self.update_button_window = (
            self.button_maker(text="Update", font=BUTTONS_FONT, padx=3, pady=3, command=self.update_button,
                              canvas=self.canvas_left, window_x=27, window_y=475, anchor=NW))

        # Delete Button
        self.delete_button, self.delete_button_window = (
            self.button_maker(text="Delete", font=BUTTONS_FONT, padx=3, pady=3, command=self.delete_button,
                              canvas=self.canvas_left, window_x=125, window_y=475, anchor=NW))

        # Add Button
        self.add_button, self.add_button_window = (
            self.button_maker(text="Add", font=BUTTONS_FONT, padx=3, pady=3, command=self.add_button,
                              canvas=self.canvas_left, window_x=225, window_y=475, anchor=NW))

        # Clear Button
        self.clear_button, self.clear_button_window = (
            self.button_maker(text="Clear", font=BUTTONS_FONT, padx=3, pady=3, command=self.clear_entries,
                              canvas=self.canvas_left, window_x=310, window_y=475, anchor=NW))

        # ------------------Right Canvas------------------ #
        self.canvas_right = self.canvas_maker(width=400, height=520, column=1, row=0)

        # Current Prices
        self.current_prices_label = self.canvas_right.create_text(25, 25, anchor=NW, font=LABELS_FONT,
                                                                  text="Current Prices")

        # Check Price Button
        self.check_prices_button, self.check_prices_button_window = (
            self.button_maker(text="Check Prices", font=BUTTONS_FONT, padx=3, pady=3, command=self.check_prices_button,
                              canvas=self.canvas_right, window_x=260, window_y=18, anchor=NW))

        # Current Price Text Field
        self.current_prices, self.current_prices_window = self.text_box_maker(
            start_text=self.item_manager.return_current_prices(),
            font=NORMAL_TEXT_FONT, canvas=self.canvas_right, window_x=25, window_y=60, anchor=NW, window_height=190, window_width=333)

        # --- Price History
        self.price_history_label = self.canvas_right.create_text(25, 275, anchor=NW, font=LABELS_FONT,
                                                                 text="Price History")

        self.price_history, self.price_history_window = self.text_box_maker(
            start_text="",
            font=NORMAL_TEXT_FONT, canvas=self.canvas_right, window_x=25, window_y=300, anchor=NW, window_height=190, window_width=333)

        self.window.mainloop()


    def populate_listbox(self):
        self.current_items_listbox.delete(0, END)  # empties the listbox first
        for product in self.item_manager.tracked_items.keys():
            self.current_items_listbox.insert("end", product)

    def listbox_select(self):  # This function is called every time an item in the listbox is selected
        if self.current_items_listbox.curselection():  # This if statement only triggers if an item is selected
            self.current_listbox_item = self.current_items_listbox.get(self.current_items_listbox.curselection()[0])

            self.update_text_box(text_box=self.price_history, text=self.item_manager.return_price_history(self.current_listbox_item))  # repopulates price history

            self.replace_text(  # Populates name field
                item=self.name_entry,
                new_text=self.current_listbox_item)
            self.replace_text(  # Populates url field
                item=self.url_entry,
                new_text=self.item_manager.tracked_items[self.current_listbox_item]["url"])
            self.replace_text(  # Populates cutoff field
                item=self.cutoff_entry,
                new_text=self.item_manager.tracked_items[self.current_listbox_item]["cutoff"])

    # ---- Maker Functions ---- #

    def canvas_maker(self, width, height, column, row):
        canvas = Canvas(self.window, bg=COLOR_1, width=width, height=height, highlightthickness=5, highlightbackground=COLOR_2, highlightcolor=COLOR_2)
        canvas.grid(column=column, row=row, padx=5)
        return canvas

    def entry_maker(self, canvas, label_x, label_y, anchor, label_font, label_text,
                    entry_bg, entry_font,
                    window_x, window_y, window_height, window_width):
        text = canvas.create_text(label_x, label_y, anchor=anchor, font=label_font, text=label_text)
        entry = Entry(canvas, bg=entry_bg, font=entry_font, highlightthickness=2, highlightcolor=COLOR_3, highlightbackground=COLOR_3)
        widget_window = canvas.create_window(window_x, window_y, height=window_height, width=window_width, anchor=NW,
                                             window=entry)

        return text, entry, widget_window

    def button_maker(self, text, font, padx, pady, command, canvas, window_x, window_y, anchor):
        button = Button(text=text, font=font, padx=padx, pady=pady, command=command)
        window = canvas.create_window(window_x, window_y, anchor=anchor, window=button)
        return button, window

    def text_box_maker(self, font, canvas, window_height, window_width, start_text, window_x, window_y, anchor):
        text = Text(canvas, font=font, highlightthickness=2, highlightcolor=COLOR_3, highlightbackground=COLOR_3)
        text.insert('1.0', start_text)
        text.config(state=DISABLED)
        window = canvas.create_window(window_x, window_y, anchor=anchor, window=text, height=window_height, width=window_width)
        return text, window

    # ---- Listbox Functions ---- #
    def check_prices_button(self):
        # Scrapes the prices
        self.item_manager.check_items_price()
        self.update_text_box(text_box=self.current_prices, text=self.item_manager.return_current_prices())


    # ---- Button Functions ---- #
    def update_button(self):
        if self.name_entry.get():
            self.item_manager.update_item(
                new_item=self.name_entry.get(),
                old_item=self.current_listbox_item,
                url=self.url_entry.get(),
                cutoff=float(self.cutoff_entry.get()))
            self.reset()

    def delete_button(self):
        self.item_manager.delete_item(item=self.current_listbox_item)

        # Clears all the entry fields
        self.clear_entries()

        # Clears price history
        self.update_text_box(text_box=self.price_history, text="")

        # Resets remaining UI elements
        self.reset()

    def add_button(self):
        if self.name_entry.get():  # Returns true if it's not empty
            self.current_listbox_item = self.name_entry.get()
            self.item_manager.add_items(
                item=self.name_entry.get(),
                url=self.url_entry.get(),
                cutoff=self.cutoff_entry.get())
            self.update_text_box(text_box=self.price_history, text=self.item_manager.return_price_history(self.current_listbox_item))
            self.reset()

    # ---- Reset Functions ---- #

    def reset(self):  # Resets the listbox and current prices field
        self.item_manager.update_json()  # Updates the JSON
        self.populate_listbox()  # repopulates the listbox
        self.update_text_box(text_box=self.current_prices, text=self.item_manager.return_current_prices()) # Updates the current prices field to reflect any name changes

    def clear_entries(self):
        for item in [
            self.name_entry,
            self.url_entry,
            self.cutoff_entry
        ]:
            self.replace_text(item=item, new_text="")

    def update_text_box(self, text_box, text):
        # Displays the current prices
        text_box.config(state=NORMAL)
        text_box.delete('1.0', END)
        text_box.insert('1.0', text)
        text_box.config(state=DISABLED)

    def replace_text(self, item, new_text):
        item.delete(0, END)
        item.insert(0, new_text)

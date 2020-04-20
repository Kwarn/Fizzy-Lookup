import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np


class FizzyLookup(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        def get_df_from_excel():
            df = pd.read_excel('examples.xlsx')
            return df

        def destroy_labels():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

        def scrollable_frame_grid_config():
            for i in range(8):
                scrollable_frame.columnconfigure(i, weight=1)

        def top_frame_grid_config():
            for i in range(7):
                top_frame.columnconfigure(i, weight=1)

        def set_search_options():
            loc_dict = {"Canning Town": "CT", "Poplar": "PO", "Epsom": "EP", "Lewisham": "LE", "Walthamstow": "WA",
                        "Hayes": "HA", "Stepney Green": "SG"}
            fur_dict = {"Furnished": "Y", "Unfurnished": "N"}
            price_dict = {"£1000-£1499": [1000, 1499], "£1500-£1799": [1500, 1799], "£1800+": [1800, 10000]}

            location = loc_dict[loc_var.get()] if loc_var.get() != "Any" else 0
            bedroom = int(bed_var.get()) if bed_var.get() != "Any" else 0
            bathroom = int(bath_var.get()) if bath_var.get() != "Any" else 0
            furnished = fur_dict[fur_var.get()] if fur_var.get() != "Any" else 0
            price = price_dict[price_var.get()] if price_var.get() != "Any" else 0
            available = avail_var.get() if avail_var.get() != "Any" else 0

            if not any([location] + [bedroom] + [bathroom] + [furnished] + [price] + [available]):
                create_labels_from_df(None, True)
            else:
                search_df(location, bedroom, bathroom, furnished, price, available)

        def search_df(location, bedroom, bathroom, furnished, price, available):
            search = []
            if location:
                search.append("(df['Unique code'].str.contains(location))")
            if bedroom:
                search.append("(df['Bedroom'] == bedroom)")
            if bathroom:
                search.append("(df['Bathroom'] == bathroom)")
            if furnished:
                search.append("(df['Fur/Unf'] == furnished)")
            if price:
                search.append("((df['Price'] >= price[0]) & (df['Price'] <= price[1]))")
            if available:
                search.append("(df['Available'] ")

            df = get_df_from_excel()
            search_str = " & ".join(search)
            idx = np.where(eval(search_str))
            destroy_labels()
            create_labels_from_df(df.loc[idx])

        def create_labels_from_df(df, load_all=False):
            if load_all:
                df = get_df_from_excel()

            headers = [ttk.Label(scrollable_frame, text=label) for label in df.columns[:-1]]
            unique_code = [ttk.Label(scrollable_frame, text=row["Unique code"]) for index, row in df.iterrows()]
            flat_num = [ttk.Label(scrollable_frame, text=row["Flat #"]) for index, row in df.iterrows()]
            bedroom = [ttk.Label(scrollable_frame, text=row["Bedroom"]) for index, row in df.iterrows()]
            sqft = [ttk.Label(scrollable_frame, text=row["Sq Ft"]) for index, row in df.iterrows()]
            bathroom = [ttk.Label(scrollable_frame, text=row["Bathroom"]) for index, row in df.iterrows()]
            fur_unf = [ttk.Label(scrollable_frame, text=row["Fur/Unf"]) for index, row in df.iterrows()]
            price = [ttk.Label(scrollable_frame, text=row["Price"]) for index, row in df.iterrows()]
            balcony = [ttk.Label(scrollable_frame, text=row["Balcony"]) for index, row in df.iterrows()]
            available_from = [ttk.Label(scrollable_frame, text=row["Available from"]) for index, row in df.iterrows()]
            data_labels = [unique_code, flat_num, bedroom, sqft, bathroom, fur_unf, price, balcony, available_from]

            grid_labels(headers, 0, True)
            [grid_labels(data_labels[i], i) for i in range(len(data_labels))]

        def grid_labels(labels, col, is_first_row=False):
            if is_first_row:
                for i in range(len(labels)):
                    labels[i].grid(row=0, column=i, rowspan=1, columnspan=1, sticky="nsew")
            else:
                for i in range(len(labels)):
                    labels[i].grid(row=i+1, column=col, rowspan=1, columnspan=1, sticky="nsew")

        tk.Frame.__init__(self, parent)

        """TOP FRAME"""

        top_frame = tk.Frame(self, bg='black')
        top_frame_grid_config()
        top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        loc_label = ttk.Label(top_frame, text="Location", anchor="center")
        loc_label.grid(row=0, column=0, sticky="nsew")
        bed_label = ttk.Label(top_frame, text="Bedrooms", anchor="center")
        bed_label.grid(row=0, column=1, sticky="nsew")
        bath_label = ttk.Label(top_frame, text="Bathrooms", anchor="center")
        bath_label.grid(row=0, column=2, sticky="nsew")
        fur_label = ttk.Label(top_frame, text="Furnished", anchor="center")
        fur_label.grid(row=0, column=3, sticky="nsew")
        price_label = ttk.Label(top_frame, text="Price", anchor="center")
        price_label.grid(row=0, column=4, sticky="nsew")
        avail_label = ttk.Label(top_frame, text="Available", anchor="center")
        avail_label.grid(row=0, column=5, sticky="nsew")

        loc_var = tk.StringVar(top_frame)
        loc_var.set("Any")
        loc_option = tk.OptionMenu(top_frame, loc_var, "Any", "Canning Town", "Poplar", "Epsom", "Lewisham","Walthamstow",
                                   "Hayes", "Stepney Green")
        loc_option.grid(row=1, column=0, sticky="nsew")

        bed_var = tk.StringVar(top_frame)
        bed_var.set("Any")
        bed_option = tk.OptionMenu(top_frame, bed_var, "Any", "1", "2", "3")
        bed_option.grid(row=1, column=1, sticky="nsew")

        bath_var = tk.StringVar(top_frame)
        bath_var.set("Any")
        bath_option = tk.OptionMenu(top_frame, bath_var, "Any", "1", "2", "3")
        bath_option.grid(row=1, column=2, sticky="nsew")

        fur_var = tk.StringVar(top_frame)
        fur_var.set("Any")
        fur_option = tk.OptionMenu(top_frame, fur_var, "Any", "Furnished", "Unfurnished")
        fur_option.grid(row=1, column=3, sticky="nsew")

        price_var = tk.StringVar(top_frame)
        price_var.set("Any")
        price_option = tk.OptionMenu(top_frame, price_var, "Any", "£1000-£1499", "£1500-£1799", "£1800+")
        price_option.grid(row=1, column=4, sticky="nsew")

        avail_var = tk.StringVar(top_frame)
        avail_var.set("Any")
        avail_option = tk.OptionMenu(top_frame, avail_var, "Any", "January", "Febuary", "March", "April", "May", "June",
                                     "July", "August", "September", "October", "November", "December")
        avail_option.grid(row=1, column=5, sticky="nsew")

        search_button = tk.Button(top_frame, text="Search", command=lambda: set_search_options())
        search_button.grid(row=0, column=6, rowspan=2, columnspan=2, sticky="nsew")

        """CENTER FRAME"""

        center_frame = tk.Frame(self, bg="green")
        center_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

        container = tk.Frame(center_frame, bg="red")
        canvas = tk.Canvas(container, bg="yellow")

        scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame_grid_config()

        canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        canvas.configure(yscrollcommand=scrollbar.set)
        container.pack(fill="both", expand=True)
        canvas.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scrollable_frame.pack(fill="both", expand=True)

        """BOTTOM FRAME"""
        bottom_frame = tk.Frame(self, bg='black')
        bottom_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
        load_button = tk.Button(bottom_frame, text="Load", command=lambda: create_labels(0, True))
        load_button.place(relx=0, rely=0.0, relwidth=0.2, relheight=0.8)


HEIGHT = 500
WIDTH = 800

app = FizzyLookup()

app.geometry('{}x{}'.format(WIDTH, HEIGHT))
app.mainloop()

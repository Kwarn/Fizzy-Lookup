import tkinter as tk
from tkinter import ttk
import pandas
import re


""" 
    TODO



"""


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
            df = pandas.read_excel('examples.xlsx')
            return df

        def search():
            loc_dict = {"Canning Town": "CT", "Poplar": "PO", "Epsom": "EP", "Lewisham": "LE", "Walthamstow": "WA", "Hayes": "HA", "Stepney Green": "SG"}
            fur_dict = {"Furnished": "Y", "Unfurnished": "N"}
            price_dict = {"£1000-£1499": [1000, 1499], "£1500-£1799": [1500, 1799], "£1800+": [1800, 10000]}

            location = loc_dict[loc_var.get()] if loc_var.get() != "Location" else 0
            print("Location: {}".format(location))
            bedroom = bed_var.get() if bed_var.get() != "Bedrooms" else 0
            bathroom = bath_var.get() if bath_var.get() != "Bathrooms" else 0
            furnished = fur_dict[fur_var.get()] if fur_var.get() != "Fur/Unfur" else 0
            price = price_dict[price_var.get()] if price_var.get() != "Price" else 0
            available = avail_var.get() if avail_var.get() != "Available" else 0


            df = get_df_from_excel()
            # print(df["Unique code"] if df["Unique code"] == "PO1" else 0)
            # new_df = df.loc(df["Key"])
            # new_df = df.loc((df["Unique code"] == df["Unique code"].str.contains(location)))
            # print(new_df)
            # print(df["Unique code"] if df["Unique code"].str.contains(location) == True else 0)
            # print(df.loc[(str(df["Unique code"])[:2] == location)])

            # print(df)
            # print(location, bedroom, bathroom, furnished, price, available)



        def create_labels(df, load=False):
            if load:
                df = get_df_from_excel()

            header = [ttk.Label(scrollable_frame, text=label) for label in df.columns[:-1]]
            unique_code = [ttk.Label(scrollable_frame, text=row["Unique code"]) for index, row in df.iterrows()]
            flat_num = [ttk.Label(scrollable_frame, text=row["Flat #"]) for index, row in df.iterrows()]
            bedroom = [ttk.Label(scrollable_frame, text=row["Bedroom"]) for index, row in df.iterrows()]
            sqft = [ttk.Label(scrollable_frame, text=row["Sq Ft"]) for index, row in df.iterrows()]
            bathroom = [ttk.Label(scrollable_frame, text=row["Bathroom"]) for index, row in df.iterrows()]
            fur_unf = [ttk.Label(scrollable_frame, text=row["Fur/Unf"]) for index, row in df.iterrows()]
            price = [ttk.Label(scrollable_frame, text=row["Price"]) for index, row in df.iterrows()]
            balcony = [ttk.Label(scrollable_frame, text=row["Balcony"]) for index, row in df.iterrows()]
            available_from = [ttk.Label(scrollable_frame, text=row["Available from"]) for index, row in df.iterrows()]

            data_labels = [unique_code , flat_num, bedroom, sqft, bathroom, fur_unf, price, balcony, available_from]

            place_labels(header, 0, True)
            [place_labels(data_labels[i], i) for i in range(len(data_labels))]

        def place_labels(labels, col, is_first_row=False):
            if is_first_row:
                for i in range(len(labels)):
                    labels[i].grid(row=0, column=i)
            else:
                for i in range(len(labels)):
                    labels[i].grid(row=i+1, column=col)


        tk.Frame.__init__(self, parent)

        """TOP FRAME"""

        top_frame = tk.Frame(self, bg='black')
        top_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        loc_var = tk.StringVar(top_frame)
        loc_var.set("Location")
        loc_option = tk.OptionMenu(top_frame, loc_var, "Canning Town", "Poplar", "Epsom", "Lewisham","Walthamstow", "Hayes", "Stepney Green")
        loc_option.place(relx=0, rely=0.1, relwidth=0.15, relheight=0.8)

        bed_var = tk.StringVar(top_frame)
        bed_var.set("Bedrooms")
        bed_option = tk.OptionMenu(top_frame, bed_var, "1", "2", "3")
        bed_option.place(relx=0.15, rely=0.1, relwidth=0.15, relheight=0.8)

        bath_var = tk.StringVar(top_frame)
        bath_var.set("Bathrooms")
        bath_option = tk.OptionMenu(top_frame, bath_var, "1", "2", "3")
        bath_option.place(relx=0.30, rely=0.1, relwidth=0.15, relheight=0.8)

        fur_var = tk.StringVar(top_frame)
        fur_var.set("Fur/Unfur")
        fur_option = tk.OptionMenu(top_frame, fur_var, "Furnished", "Unfurnished")
        fur_option.place(relx=0.45, rely=0.1, relwidth=0.15, relheight=0.8)

        price_var = tk.StringVar(top_frame)
        price_var.set("Price")
        price_option = tk.OptionMenu(top_frame, price_var, "£1000-£1499", "£1500-£1799", "£1800+")
        price_option.place(relx=0.6, rely=0.1, relwidth=0.15, relheight=0.8)

        avail_var = tk.StringVar(top_frame)
        avail_var.set("Available")
        avail_option = tk.OptionMenu(top_frame, avail_var, "January", "Febuary", "March", "April", "May", "June",
                                     "July", "August", "September", "October", "November", "December")
        avail_option.place(relx=0.75, rely=0.1, relwidth=0.15, relheight=0.8)

        search_button = tk.Button(top_frame, text="Search", command=lambda: search())
        search_button.place(relx=0.9, rely=0.1, relwidth=0.1, relheight=0.8)

        """CENTER FRAME"""

        center_frame = ttk.Frame(self)
        center_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.8)

        container = ttk.Frame(center_frame)
        canvas = tk.Canvas(container)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(side="left", fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        """BOTTOM FRAME"""
        bottom_frame = tk.Frame(self, bg='black')
        bottom_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
        load_button = tk.Button(bottom_frame, text="Load", command=lambda: create_labels(None, load=True))
        load_button.place(relx=0, rely=0.0, relwidth=0.2, relheight=0.8)








HEIGHT = 500
WIDTH = 800

app = FizzyLookup()

app.geometry('{}x{}'.format(WIDTH, HEIGHT))
# app.resizable(width=False, height=False)
app.mainloop()

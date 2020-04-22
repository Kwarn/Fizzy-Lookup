import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

"""Todo:
    speed up label creation and placement, perhaps by placing each list without first appending it to a list of lists 
    look into using timeit - perhaps isolate code in a sandbox env
"""

class FizzyLookup(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Fizzy Lookup")
        self.iconbitmap("FizzyLookupIcon.ico")
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
        frame.columnconfigure(0, weight=1)
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        def get_df_from_excel():
            df = pd.read_excel('examples.xlsx')
            return df

        def convert_df_datetime_to_str(df):
            """Makes datetime more easily searchable"""
            df['Available'] = pd.to_datetime(df["Available"], errors="coerce")
            df['Available'] = df['Available'].dt.strftime('%m - %B - %Y')
            return df

        def destroy_widgets(frame_to_clear):
            for widget in frame_to_clear.winfo_children():
                widget.destroy()

        def column_grid_config(frame, col_range):
            for i in range(0, col_range):
                frame.columnconfigure(i, weight=1)

        def set_search_options():
            """Checks OptionMenu input and converts into corresponding type/format before searching df"""

            loc_dict = {"Canning Town": "CT", "Poplar": "PO", "Epsom": "EP", "Lewisham": "LE", "Walthamstow": "WA",
                        "Hayes": "HA", "Stepney Green": "SG"}
            fur_dict = {"Furnished": "Y", "Unfurnished": "N"}
            price_dict = {"£1000-£1499": [1000, 1499], "£1500-£1799": [1500, 1799], "£1800+": [1800, 10000]}

            location = loc_dict[loc_var.get()] if loc_var.get() != "Any" else 0
            floor = int(floor_var.get()) if floor_var.get() != "Any" else 0
            bedroom = int(bed_var.get()) if bed_var.get() != "Any" else 0
            bathroom = int(bath_var.get()) if bath_var.get() != "Any" else 0
            furnished = fur_dict[fur_var.get()] if fur_var.get() != "Any" else 0
            price = price_dict[price_var.get()] if price_var.get() != "Any" else 0
            available = avail_var.get() if avail_var.get() != "Any" else 0

            if not any([location] + [floor] + [bedroom] + [bathroom] + [furnished] + [price] + [available]):
                create_labels_from_df(pd.DataFrame(), True)
            else:
                create_search_str(location, floor, bedroom, bathroom, furnished, price, available)

        def create_search_str(location, floor, bedroom, bathroom, furnished, price, available):
            """Creates string of conditions to eval(). Locates DataFrame indices matching string conditions"""

            search = []
            if location:
                search.append("(df['Location'].str.contains(location))")
            if floor:
                search.append("(df['Floor'] == floor)")
            if bedroom:
                search.append("(df['Bedroom'] == bedroom)")
            if bathroom:
                search.append("(df['Bathroom'] == bathroom)")
            if furnished:
                search.append("(df['Fur/Unf'] == furnished)")
            if price:
                search.append("((df['Price'] >= price[0]) & (df['Price'] <= price[1]))")
            if available:
                search.append("((df['Available'].str.contains(available)) & (df['Available'] != 'NaN'))")

            df = convert_df_datetime_to_str(get_df_from_excel())
            destroy_widgets(scrollable_frame)
            create_labels_from_df(df.loc[np.where(eval(" & ".join(search)))])

        def create_labels_from_df(df, load_all=False):
            if load_all:
                df = convert_df_datetime_to_str(get_df_from_excel())

            df_keys = ["Location", "Flat #", "Floor", "Bedroom", "Sq Ft", "Bathroom", "Fur/Unf", "Price", "Balcony", "Available"]
            labels = []
            for key in df_keys:
                labels.append([ttk.Label(scrollable_frame, text=row[key], borderwidth=1, relief="solid") for index, row in df.iterrows()])

            headers = [tk.Label(scrollable_frame, text=label, bg="grey", fg="white", anchor="w") for label in df.columns[:10]]
            grid_labels(headers, 0, True)
            [grid_labels(labels[i], i) for i in range(len(labels))]

        def grid_labels(labels, col, is_first_row=False):
            if is_first_row:
                for i in range(len(labels)):
                    labels[i].grid(row=0, column=i, rowspan=1, columnspan=1, sticky="nsew")
            else:
                for i in range(len(labels)):
                    labels[i].grid(row=i+1, column=col, rowspan=1, columnspan=1, sticky="nsew")

        tk.Frame.__init__(self, parent)

        """TOP FRAME"""

        top_frame = tk.Frame(self)
        column_grid_config(top_frame, 9)
        top_frame.grid(row=0, column=0, sticky="nsew")

        loc_label = ttk.Label(top_frame, text="Location", anchor="center")
        loc_label.grid(row=0, column=0, sticky="nsew")
        floor_label = ttk.Label(top_frame, text="Floor", anchor="center")
        floor_label.grid(row=0, column=1, sticky="nsew")
        bed_label = ttk.Label(top_frame, text="Bedrooms", anchor="center")
        bed_label.grid(row=0, column=2, sticky="nsew")
        bath_label = ttk.Label(top_frame, text="Bathrooms", anchor="center")
        bath_label.grid(row=0, column=3, sticky="nsew")
        fur_label = ttk.Label(top_frame, text="Furnished", anchor="center")
        fur_label.grid(row=0, column=4, sticky="nsew")
        price_label = ttk.Label(top_frame, text="Price", anchor="center")
        price_label.grid(row=0, column=5, sticky="nsew")
        avail_label = ttk.Label(top_frame, text="Available", anchor="center")
        avail_label.grid(row=0, column=6, sticky="nsew")

        loc_var = tk.StringVar(top_frame)
        loc_var.set("Any")
        loc_option = tk.OptionMenu(top_frame, loc_var, "Any", "Canning Town", "Poplar", "Epsom",
                                   "Lewisham", "Walthamstow", "Hayes", "Stepney Green")
        loc_option.grid(row=1, column=0, sticky="nsew")

        floor_var = tk.StringVar(top_frame)
        floor_var.set("Any")
        floor_options = tk.OptionMenu(top_frame, floor_var, "Any", "1", "2", "3", "4", "5")
        floor_options.grid(row=1, column=1, sticky="nsew")

        bed_var = tk.StringVar(top_frame)
        bed_var.set("Any")
        bed_option = tk.OptionMenu(top_frame, bed_var, "Any", "1", "2", "3")
        bed_option.grid(row=1, column=2, sticky="nsew")

        bath_var = tk.StringVar(top_frame)
        bath_var.set("Any")
        bath_option = tk.OptionMenu(top_frame, bath_var, "Any", "1", "2", "3")
        bath_option.grid(row=1, column=3, sticky="nsew")

        fur_var = tk.StringVar(top_frame)
        fur_var.set("Any")
        fur_option = tk.OptionMenu(top_frame, fur_var, "Any", "Furnished", "Unfurnished")
        fur_option.grid(row=1, column=4, sticky="nsew")

        price_var = tk.StringVar(top_frame)
        price_var.set("Any")
        price_option = tk.OptionMenu(top_frame, price_var, "Any", "£1000-£1499", "£1500-£1799", "£1800+")
        price_option.grid(row=1, column=5, sticky="nsew")

        avail_var = tk.StringVar(top_frame)
        avail_var.set("Any")
        avail_option = tk.OptionMenu(top_frame, avail_var, "Any", "January", "Febuary", "March", "April", "May", "June",
                                     "July", "August", "September", "October", "November", "December")
        avail_option.grid(row=1, column=6, sticky="nsew")

        search_button = tk.Button(top_frame, text="Search", command=lambda: set_search_options())
        search_button.grid(row=0, column=7, rowspan=2, columnspan=2, sticky="nsew")

        """CENTER FRAME"""

        center_frame = tk.Frame(self)
        center_frame.grid(row=1, column=0, sticky="nsew")

        container = tk.Frame(center_frame)
        canvas = tk.Canvas(container)

        scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        column_grid_config(scrollable_frame, 9)

        canvas.bind_all('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        canvas.configure(yscrollcommand=scrollbar.set)
        container.pack(fill="both", expand=True)
        canvas.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        scrollable_frame.pack(fill="both", expand=True)


HEIGHT = 500
WIDTH = 800

app = FizzyLookup()

app.geometry('{}x{}'.format(WIDTH, HEIGHT))
app.mainloop()
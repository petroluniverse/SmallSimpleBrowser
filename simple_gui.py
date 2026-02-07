    # Copyright (C) 2026 petroluniverse.com
    # petroluniverse@proton.me

    #This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import tkinter as tk
from tkinter import ttk

BASE_DIR = os.path.expanduser("~/SmallSimpleManuals")
all_pdfs_cache = []  # For live search filtering

def list_dirs(path):
    return sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])

def list_pdfs(path):
    return sorted([f for f in os.listdir(path) if f.lower().endswith(".pdf")])

def get_sel(lb):
    sel = lb.curselection()
    return lb.get(sel[0]) if sel else None

# ------------------ Toolbar Actions ------------------ #

def load_makes():
    make_list.delete(0, tk.END)
    for m in list_dirs(BASE_DIR):
        make_list.insert(tk.END, m)
    model_list.delete(0, tk.END)
    year_list.delete(0, tk.END)
    pdf_list.delete(0, tk.END)
    all_pdfs_cache.clear()

def refresh():
    load_makes()

def open_pdf(event=None):
    make = get_sel(make_list)
    model = get_sel(model_list)
    year = get_sel(year_list)
    pdf = get_sel(pdf_list)
    if not all([make, model, year, pdf]):
        return
    path = os.path.join(BASE_DIR, make, model, year, pdf)
    os.system(f'xdg-open "{path}"')

def filter_pdfs(*_):
    query = search_var.get().lower()
    pdf_list.delete(0, tk.END)
    for pdf in all_pdfs_cache:
        if query in pdf.lower():
            pdf_list.insert(tk.END, pdf)

# ------------------ List Updates ------------------ #

def on_make_select(event):
    root.after_idle(update_models)

def update_models():
    model_list.delete(0, tk.END)
    year_list.delete(0, tk.END)
    pdf_list.delete(0, tk.END)
    all_pdfs_cache.clear()
    make = get_sel(make_list)
    if not make:
        return
    for model in list_dirs(os.path.join(BASE_DIR, make)):
        model_list.insert(tk.END, model)

def on_model_select(event):
    root.after_idle(update_years)

def update_years():
    year_list.delete(0, tk.END)
    pdf_list.delete(0, tk.END)
    all_pdfs_cache.clear()
    make = get_sel(make_list)
    model = get_sel(model_list)
    if not make or not model:
        return
    for year in list_dirs(os.path.join(BASE_DIR, make, model)):
        year_list.insert(tk.END, year)

def on_year_select(event):
    root.after_idle(update_pdfs)

def update_pdfs():
    pdf_list.delete(0, tk.END)
    all_pdfs_cache.clear()
    make = get_sel(make_list)
    model = get_sel(model_list)
    year = get_sel(year_list)
    if not make or not model or not year:
        return
    path = os.path.join(BASE_DIR, make, model, year)
    all_pdfs_cache.extend(list_pdfs(path))
    for pdf in all_pdfs_cache:
        pdf_list.insert(tk.END, pdf)

# ------------------ GUI Setup ------------------ #

root = tk.Tk()
root.title("Parts catalogue")
root.geometry("1100x500")

# Toolbar
toolbar = tk.Frame(root)
toolbar.pack(fill=tk.X, padx=5, pady=5)

search_var = tk.StringVar()

# Buttons on far left
open_btn = tk.Button(toolbar, text="Open", command=open_pdf)
open_btn.pack(side=tk.LEFT, padx=(0,5))

refresh_btn = tk.Button(toolbar, text="Refresh", command=refresh)
refresh_btn.pack(side=tk.LEFT, padx=(0,15))


# Search PDF on far right
search_frame = tk.Frame(toolbar)
search_frame.pack(side=tk.RIGHT)

tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame, textvariable=search_var, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
search_var.trace_add("write", filter_pdfs)
search_entry.bind("<Return>", open_pdf)

# 4 vertical panes
paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True)

def column(title):
    frame = ttk.Frame(paned)
    ttk.Label(frame, text=title).pack(anchor="w")
    lb = tk.Listbox(frame, exportselection=False)
    lb.pack(fill=tk.BOTH, expand=True)
    paned.add(frame, weight=1)
    return lb

make_list  = column("MAKE")
model_list = column("MODEL")
year_list  = column("YEAR")
pdf_list   = column("ASSEMBLY")

# Bind selection events
make_list.bind("<<ListboxSelect>>", on_make_select)
model_list.bind("<<ListboxSelect>>", on_model_select)
year_list.bind("<<ListboxSelect>>", on_year_select)
pdf_list.bind("<Double-Button-1>", open_pdf)

# Initial load
load_makes()

root.mainloop()

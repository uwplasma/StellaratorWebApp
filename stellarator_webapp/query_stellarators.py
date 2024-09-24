import sqlite3
import tkinter as tk
from tkinter import messagebox
from qsc import Qsc
import matplotlib.pyplot as plt

def is_good_stellarator(config):
    criteria = {
        "axis_length": config[11] > 0,
        "iota": abs(config[12]) >= 0.2,
        "max_elongation": config[13] <= 10,
        "min_L_grad_B": abs(config[14]) >= 0.1,
        "min_R0": abs(config[15]) >= 0.3,
        "r_singularity": abs(config[16]) >= 0.1,
        "L_grad_grad_B": abs(config[17]) >= 0.1,
        "B20_variation": abs(config[18]) <= 5,
        "beta": config[19] >= 1e-4
    }
    
    return "good" if all(criteria.values()) else "bad"

def query_specific_configuration(config_id):
    conn = sqlite3.connect('MyStellaratorDB.db')
    cursor = conn.cursor()
    query = "SELECT * FROM Configurations WHERE ConfigID = ?;"
    cursor.execute(query, (config_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def query_configurations_by_criteria(nfp, etabar_min):
    conn = sqlite3.connect('MyStellaratorDB.db')
    cursor = conn.cursor()
    query = "SELECT * FROM Configurations WHERE nfp = ? AND etabar >= ?;"
    cursor.execute(query, (nfp, etabar_min))
    rows = cursor.fetchall()
    conn.close()
    return rows

def display_result(result):
    result_text.delete(1.0, tk.END)
    if result:
        for row in result:
            status = is_good_stellarator(row)
            result_text.insert(tk.END, f"{row} - {status}\n")
    else:
        result_text.insert(tk.END, "No results found.\n")

def query_by_id():
    config_id = entry_id.get()
    try:
        config_id_int = int(config_id)
        config = query_specific_configuration(config_id_int)
        display_result([config])
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid integer ID.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def query_by_criteria():
    nfp = entry_nfp.get()
    etabar_min = entry_etabar.get()
    try:
        nfp_int = int(nfp)
        etabar_min_float = float(etabar_min)
        configs = query_configurations_by_criteria(nfp_int, etabar_min_float)
        display_result(configs)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def plot_stellarator(config):
    try:
        print("Plotting configuration:", config)
        stel = Qsc(
            rc=[1, config[1], config[2], config[3]],
            zs=[0, config[4], config[5], config[6]],
            nfp=config[7],
            etabar=config[8],
            B2c=config[9],
            p2=config[10],
            order='r2'  # Adjust order if necessary
        )
        stel.plot_boundary(r=0.2)
        plt.show()
    except ValueError as e:
        print(f"Error plotting stellarator: {e}")
        messagebox.showerror("Plotting Error", f"Error plotting stellarator: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        messagebox.showerror("Unexpected Error", f"Unexpected error: {e}")

def plot_selected():
    config_id = entry_id.get()
    try:
        config_id_int = int(config_id)
        config = query_specific_configuration(config_id_int)
        if config:
            plot_stellarator(config)
        else:
            messagebox.showerror("Query Error", "No configuration found with the given ID.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid integer ID.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def manual_input():
    try:
        rc1 = float(entry_rc1.get())
        rc2 = float(entry_rc2.get())
        rc3 = float(entry_rc3.get())
        zs1 = float(entry_zs1.get())
        zs2 = float(entry_zs2.get())
        zs3 = float(entry_zs3.get())
        nfp = int(entry_nfp_manual.get())
        etabar = float(entry_etabar_manual.get())
        B2c = float(entry_B2c.get())
        p2 = float(entry_p2.get())

        stel = Qsc(
            rc=[1, rc1, rc2, rc3],
            zs=[0, zs1, zs2, zs3],
            nfp=nfp,
            etabar=etabar,
            B2c=B2c,
            p2=p2,
            order='r2'  # Adjust order if necessary
        )
        stel.plot_boundary(r=0.2)
        plt.show()
    except ValueError as e:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Stellarator Configuration Query")

# Frame for query by ID
frame_id = tk.Frame(app)
frame_id.pack(padx=10, pady=10)
tk.Label(frame_id, text="Query by Configuration ID").grid(row=0, column=0, columnspan=2)

tk.Label(frame_id, text="Configuration ID:").grid(row=1, column=0)
entry_id = tk.Entry(frame_id)
entry_id.grid(row=1, column=1)

tk.Button(frame_id, text="Query", command=query_by_id).grid(row=2, column=0, columnspan=2)
tk.Button(frame_id, text="Plot", command=plot_selected).grid(row=3, column=0, columnspan=2)

# Frame for query by criteria
frame_criteria = tk.Frame(app)
frame_criteria.pack(padx=10, pady=10)
tk.Label(frame_criteria, text="Query by Criteria").grid(row=0, column=0, columnspan=2)

tk.Label(frame_criteria, text="nfp:").grid(row=1, column=0)
entry_nfp = tk.Entry(frame_criteria)
entry_nfp.grid(row=1, column=1)

tk.Label(frame_criteria, text="Minimum etabar:").grid(row=2, column=0)
entry_etabar = tk.Entry(frame_criteria)
entry_etabar.grid(row=2, column=1)

tk.Button(frame_criteria, text="Query", command=query_by_criteria).grid(row=3, column=0, columnspan=2)

# Frame for manual input
frame_manual = tk.Frame(app)
frame_manual.pack(padx=10, pady=10)
tk.Label(frame_manual, text="Manual Configuration Input").grid(row=0, column=0, columnspan=2)

tk.Label(frame_manual, text="rc1:").grid(row=1, column=0)
entry_rc1 = tk.Entry(frame_manual)
entry_rc1.grid(row=1, column=1)

tk.Label(frame_manual, text="rc2:").grid(row=2, column=0)
entry_rc2 = tk.Entry(frame_manual)
entry_rc2.grid(row=2, column=1)

tk.Label(frame_manual, text="rc3:").grid(row=3, column=0)
entry_rc3 = tk.Entry(frame_manual)
entry_rc3.grid(row=3, column=1)

tk.Label(frame_manual, text="zs1:").grid(row=4, column=0)
entry_zs1 = tk.Entry(frame_manual)
entry_zs1.grid(row=4, column=1)

tk.Label(frame_manual, text="zs2:").grid(row=5, column=0)
entry_zs2 = tk.Entry(frame_manual)
entry_zs2.grid(row=5, column=1)

tk.Label(frame_manual, text="zs3:").grid(row=6, column=0)
entry_zs3 = tk.Entry(frame_manual)
entry_zs3.grid(row=6, column=1)

tk.Label(frame_manual, text="nfp:").grid(row=7, column=0)
entry_nfp_manual = tk.Entry(frame_manual)
entry_nfp_manual.grid(row=7, column=1)

tk.Label(frame_manual, text="etabar:").grid(row=8, column=0)
entry_etabar_manual = tk.Entry(frame_manual)
entry_etabar_manual.grid(row=8, column=1)

tk.Label(frame_manual, text="B2c:").grid(row=9, column=0)
entry_B2c = tk.Entry(frame_manual)
entry_B2c.grid(row=9, column=1)

tk.Label(frame_manual, text="p2:").grid(row=10, column=0)
entry_p2 = tk.Entry(frame_manual)
entry_p2.grid(row=10, column=1)

tk.Button(frame_manual, text="Plot", command=manual_input).grid(row=11, column=0, columnspan=2)

# Result display
result_text = tk.Text(app, height=15, width=100)
result_text.pack(padx=10, pady=10)

app.mainloop()













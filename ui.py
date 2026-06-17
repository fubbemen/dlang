import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
# Keeping your requested imports
from main import code_to_image
from read import read


def browse_code_file():
    # Opens a file explorer dialog to select an existing text file
    selected_path = filedialog.askopenfilename(
        title="Select Source Code File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if selected_path:
        # Clear and insert full path into the code field
        entry_code.delete(0, tk.END)
        entry_code.insert(0, selected_path)

        # Extract just the filename and suggest an output name automatically
        base_name = os.path.basename(selected_path)
        name_without_ext = os.path.splitext(base_name)[0]

        # Pre-fill the output filename if it's empty
        if not entry_filename.get().strip():
            entry_filename.insert(0, f"{name_without_ext}.png")


def browse_folder_address():
    # Opens the standard OS directory picker to choose a destination folder
    selected_dir = filedialog.askdirectory(title="Select Output Folder")
    if selected_dir:
        # Clear the entry field and insert the selected folder directory
        entry_fileadress.delete(0, tk.END)
        entry_fileadress.insert(0, selected_dir)


def run_conversion():
    # Retrieve data from the input fields
    code_path = entry_code.get().strip()
    filename_val = entry_filename.get().strip()
    fileadress_val = entry_fileadress.get().strip()

    # Validation check to ensure all parameters exist
    if not code_path or not filename_val or not fileadress_val:
        messagebox.showwarning("Missing Information", "Please fill in all fields before proceeding.")
        return

    try:
        # Status update
        label_status.config(text="Processing... Please wait.", fg="blue")
        root.update_idletasks()

        # 1. Pass the file path into your read function to get the actual code string
        actual_code_text = read(code_path)

        # 2. Executing your imported function with the read text data
        code_to_image(actual_code_text, filename_val, fileadress_val)

        # Success message
        label_status.config(text="Installation/Conversion Complete!", fg="green")
        messagebox.showinfo("Success", "The operation completed successfully!")
    except Exception as e:
        label_status.config(text="Error occurred.", fg="red")
        messagebox.showerror("Error", f"An error occurred during execution:\n{str(e)}")


# --- Main Window Setup ---
root = tk.Tk()
root.title("CodeToImage Setup Wizard")
root.geometry("540x340")
root.resizable(False, False)

# --- Top Banner (Classic Installer Style) ---
banner_frame = tk.Frame(root, bg="white", height=60)
banner_frame.pack(fill="x", side="top")
banner_frame.pack_propagate(False)

label_title = tk.Label(banner_frame, text="CodeToImage Configuration", font=("Arial", 11, "bold"), bg="white",
                       anchor="w")
label_title.pack(fill="x", padx=15, pady=(8, 2))

label_subtitle = tk.Label(banner_frame, text="Specify the parameters for the file conversion below.", font=("Arial", 9),
                          bg="white", anchor="w")
label_subtitle.pack(fill="x", padx=15)

# Separator line under banner
sep1 = ttk.Separator(root, orient="horizontal")
sep1.pack(fill="x")

# --- Main Content Frame ---
content_frame = tk.Frame(root, padx=20, pady=20)
content_frame.pack(fill="both", expand=True)

# Grid configuration for alignment
content_frame.columnconfigure(1, weight=1)

# Field 1: Code Filename (With Browse File Button)
label_code = tk.Label(content_frame, text="Filename of code (TXT):", anchor="w")
label_code.grid(row=0, column=0, sticky="w", pady=8, padx=(0, 10))

entry_code = tk.Entry(content_frame)
entry_code.grid(row=0, column=1, sticky="ew", pady=8)

btn_browse_code = tk.Button(content_frame, text="Browse...", command=browse_code_file)
btn_browse_code.grid(row=0, column=2, sticky="e", pady=8, padx=(5, 0))

# Field 2: Output Filename
label_filename = tk.Label(content_frame, text="Filename of output (PNG,JPG):", anchor="w")
label_filename.grid(row=1, column=0, sticky="w", pady=8, padx=(0, 10))
entry_filename = tk.Entry(content_frame)
entry_filename.grid(row=1, column=1, columnspan=2, sticky="ew", pady=8)

# Field 3: Folder Address (With Browse Folder Button)
label_fileadress = tk.Label(content_frame, text="Folder to save image to:", anchor="w")
label_fileadress.grid(row=2, column=0, sticky="w", pady=8, padx=(0, 10))

entry_fileadress = tk.Entry(content_frame)
entry_fileadress.grid(row=2, column=1, sticky="ew", pady=8)

btn_browse_folder = tk.Button(content_frame, text="Browse...", command=browse_folder_address)
btn_browse_folder.grid(row=2, column=2, sticky="e", pady=8, padx=(5, 0))

# --- Status Bar ---
label_status = tk.Label(content_frame, text="Ready to install.", font=("Arial", 9, "italic"), anchor="w")
label_status.grid(row=3, column=0, columnspan=3, sticky="w", pady=(15, 0))

# --- Bottom Button Bar ---
sep2 = ttk.Separator(root, orient="horizontal")
sep2.pack(fill="x")

button_frame = tk.Frame(root, padx=15, pady=10)
button_frame.pack(fill="x", side="bottom")

# Standard wizard layout buttons (Back, Next/Install, Cancel)
btn_cancel = tk.Button(button_frame, text="Cancel", width=10, command=root.quit)
btn_cancel.pack(side="right", padx=5)

btn_install = tk.Button(button_frame, text="Install >", width=10, font=("Arial", 9, "bold"), command=run_conversion)
btn_install.pack(side="right", padx=5)

btn_back = tk.Button(button_frame, text="< Back", width=10, state="disabled")
btn_back.pack(side="right", padx=5)

# Start the application loop
root.mainloop()
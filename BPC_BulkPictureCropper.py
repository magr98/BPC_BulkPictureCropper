import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import os

def crop_image(file_path, prefix, crop_mode, crop_px_top, crop_px_bottom, crop_px_left, crop_px_right):
    try:
        img = Image.open(file_path)
        w, h = img.size
        
        if crop_mode == "crop_all_edges":
            if w > crop_px_left * 2 and h > crop_px_top * 2:
                cropped = img.crop((crop_px_left, crop_px_top, w - crop_px_right, h - crop_px_bottom))
                output_name = prefix + os.path.basename(file_path)
                output_path = os.path.join(os.path.dirname(file_path), output_name)
                cropped.save(output_path)
                return f"Cropped: {output_name}"
            else:
                return f"Skipped (too small): {os.path.basename(file_path)}"
        
        elif crop_mode == "crop_left_right":
            if w > crop_px_left + crop_px_right:
                cropped = img.crop((crop_px_left, 0, w - crop_px_right, h))
                output_name = prefix + os.path.basename(file_path)
                output_path = os.path.join(os.path.dirname(file_path), output_name)
                cropped.save(output_path)
                return f"Cropped: {output_name}"
            else:
                return f"Skipped (too small): {os.path.basename(file_path)}"
        
        elif crop_mode == "crop_top_bottom":
            if h > crop_px_top + crop_px_bottom:
                cropped = img.crop((0, crop_px_top, w, h - crop_px_bottom))
                output_name = prefix + os.path.basename(file_path)
                output_path = os.path.join(os.path.dirname(file_path), output_name)
                cropped.save(output_path)
                return f"Cropped: {output_name}"
            else:
                return f"Skipped (too small): {os.path.basename(file_path)}"
        
        elif crop_mode == "crop_specific":
            if w > crop_px_left + crop_px_right and h > crop_px_top + crop_px_bottom:
                cropped = img.crop((crop_px_left, crop_px_top, w - crop_px_right, h - crop_px_bottom))
                output_name = prefix + os.path.basename(file_path)
                output_path = os.path.join(os.path.dirname(file_path), output_name)
                cropped.save(output_path)
                return f"Cropped: {output_name}"
            else:
                return f"Skipped (too small): {os.path.basename(file_path)}"
        
    except Exception as e:
        return f"Error processing {os.path.basename(file_path)}: {e}"

def on_drop(event):
    file_list = root.tk.splitlist(event.data)
    
    prefix = prefix_entry.get().strip()
    if not prefix:
        prefix = "cropped_"

    try:
        crop_px_top = int(crop_top_entry.get().strip())
        crop_px_bottom = int(crop_bottom_entry.get().strip())
        crop_px_left = int(crop_left_entry.get().strip())
        crop_px_right = int(crop_right_entry.get().strip())
    except:
        crop_px_top = crop_px_bottom = crop_px_left = crop_px_right = 200  # fallback if invalid
        status_label.config(text="? Invalid crop size input, using default: 200px")

    crop_mode = crop_mode_var.get()

    results = []
    for file_path in file_list:
        file_path = file_path.strip("{}")
        if os.path.isfile(file_path):
            result = crop_image(file_path, prefix, crop_mode, crop_px_top, crop_px_bottom, crop_px_left, crop_px_right)
            results.append(result)
    status_label.config(text="\n".join(results))

def update_crop_inputs(*args):
    # Hide all inputs first
    for widget in crop_inputs_frame.winfo_children():
        widget.grid_forget()

    # Show relevant fields based on selected crop mode
    crop_mode = crop_mode_var.get()

    if crop_mode == "crop_all_edges":
        tk.Label(crop_inputs_frame, text="Crop size (px from all edges):").grid(row=0, column=0)
        crop_all_entry.grid(row=0, column=1, padx=5)
    elif crop_mode == "crop_left_right":
        tk.Label(crop_inputs_frame, text="Left crop (px):").grid(row=0, column=0)
        crop_left_entry.grid(row=0, column=1, padx=5)
        tk.Label(crop_inputs_frame, text="Right crop (px):").grid(row=1, column=0)
        crop_right_entry.grid(row=1, column=1, padx=5)
    elif crop_mode == "crop_top_bottom":
        tk.Label(crop_inputs_frame, text="Top crop (px):").grid(row=0, column=0)
        crop_top_entry.grid(row=0, column=1, padx=5)
        tk.Label(crop_inputs_frame, text="Bottom crop (px):").grid(row=1, column=0)
        crop_bottom_entry.grid(row=1, column=1, padx=5)
    elif crop_mode == "crop_specific":
        tk.Label(crop_inputs_frame, text="Top crop (px):").grid(row=0, column=0)
        crop_top_entry.grid(row=0, column=1, padx=5)
        tk.Label(crop_inputs_frame, text="Bottom crop (px):").grid(row=1, column=0)
        crop_bottom_entry.grid(row=1, column=1, padx=5)
        tk.Label(crop_inputs_frame, text="Left crop (px):").grid(row=2, column=0)
        crop_left_entry.grid(row=2, column=1, padx=5)
        tk.Label(crop_inputs_frame, text="Right crop (px):").grid(row=3, column=0)
        crop_right_entry.grid(row=3, column=1, padx=5)

# GUI setup
root = TkinterDnD.Tk()
root.title("Multi-Image Cropper")
root.geometry("480x500")

# Prefix input
prefix_frame = tk.Frame(root)
prefix_frame.pack(pady=5)
tk.Label(prefix_frame, text="Filename prefix:").pack(side=tk.LEFT)
prefix_entry = tk.Entry(prefix_frame)
prefix_entry.insert(0, "cropped_")
prefix_entry.pack(side=tk.LEFT, padx=5)

# Crop mode dropdown
crop_mode_frame = tk.Frame(root)
crop_mode_frame.pack(pady=5)
crop_mode_var = tk.StringVar(value="crop_all_edges")
tk.Label(crop_mode_frame, text="Select crop mode:").pack(side=tk.LEFT)
crop_mode_menu = tk.OptionMenu(crop_mode_frame, crop_mode_var, 
                               "crop_all_edges", "crop_left_right", 
                               "crop_top_bottom", "crop_specific")
crop_mode_menu.pack(side=tk.LEFT)

# Frame for crop size inputs
crop_inputs_frame = tk.Frame(root)
crop_inputs_frame.pack(pady=5)

# Default input fields
crop_all_entry = tk.Entry(crop_inputs_frame, width=6)
crop_all_entry.insert(0, "200")
crop_left_entry = tk.Entry(crop_inputs_frame, width=6)
crop_left_entry.insert(0, "200")
crop_right_entry = tk.Entry(crop_inputs_frame, width=6)
crop_right_entry.insert(0, "200")
crop_top_entry = tk.Entry(crop_inputs_frame, width=6)
crop_top_entry.insert(0, "200")
crop_bottom_entry = tk.Entry(crop_inputs_frame, width=6)
crop_bottom_entry.insert(0, "200")

# Update crop input fields based on selected mode
crop_mode_var.trace("w", update_crop_inputs)
update_crop_inputs()

# Drop zone
label = tk.Label(root, text="Drop image files here\n(Multiple selection supported)", width=50, height=8, relief="groove")
label.pack(padx=10, pady=10)
label.drop_target_register(DND_FILES)
label.dnd_bind("<<Drop>>", on_drop)

# Status display
status_label = tk.Label(root, text="", justify="left")
status_label.pack(pady=5)

root.mainloop()

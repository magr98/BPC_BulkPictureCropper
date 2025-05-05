import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import os

def crop_image(file_path, prefix, crop_px):
    try:
        img = Image.open(file_path)
        w, h = img.size
        if w > crop_px * 2 and h > crop_px * 2:
            cropped = img.crop((crop_px, crop_px, w - crop_px, h - crop_px))
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
        crop_px = int(crop_entry.get().strip())
    except:
        crop_px = 200  # fallback if invalid
        status_label.config(text="? Invalid crop size input, using default: 200px")

    results = []
    for file_path in file_list:
        file_path = file_path.strip("{}")
        if os.path.isfile(file_path):
            result = crop_image(file_path, prefix, crop_px)
            results.append(result)
    status_label.config(text="\n".join(results))

# GUI setup
root = TkinterDnD.Tk()
root.title("Multi-Image Cropper")
root.geometry("480x340")

# Prefix input
prefix_frame = tk.Frame(root)
prefix_frame.pack(pady=5)
tk.Label(prefix_frame, text="Filename prefix:").pack(side=tk.LEFT)
prefix_entry = tk.Entry(prefix_frame)
prefix_entry.insert(0, "cropped_")
prefix_entry.pack(side=tk.LEFT, padx=5)

# Crop size input
crop_frame = tk.Frame(root)
crop_frame.pack(pady=5)
tk.Label(crop_frame, text="Crop size (px from each side):").pack(side=tk.LEFT)
crop_entry = tk.Entry(crop_frame, width=6)
crop_entry.insert(0, "200")
crop_entry.pack(side=tk.LEFT, padx=5)

# Drop zone
label = tk.Label(root, text="Drop image files here\n(Multiple selection supported)", width=50, height=8, relief="groove")
label.pack(padx=10, pady=10)
label.drop_target_register(DND_FILES)
label.dnd_bind("<<Drop>>", on_drop)

# Status display
status_label = tk.Label(root, text="", justify="left")
status_label.pack(pady=5)

root.mainloop()

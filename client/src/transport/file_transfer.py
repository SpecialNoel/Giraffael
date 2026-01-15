# file_transfer.py

import os
import requests
import tkinter as tk
from tkinter import filedialog

# Helper functions
def get_file_extension(filename):
    # Returns the extension of a file, including dot.
    # Example: .txt, .pdf, .png, etc..
    return os.path.splitext(filename)[1]
def get_file_dir_path(file_path):
    return os.path.dirname(file_path)

# Upload a file with given file content and room code
def upload(uri, room_code, filename):
    def ask_file_location(filename, fileExtension):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(defaultextension=fileExtension, 
                                            initialfile=filename)
        return file_path
    
    file_extension = get_file_extension(filename)
    file_path = ask_file_location(filename, file_extension)
    
    if os.path.isfile(file_path):
        print(f'✅ File [{filename}] exists on user local machine.')
    else:
        print(f'❌ File [{filename}] does not exist on user local machine.')
    
    with open(file_path, 'rb') as f:
        files = {'file': (filename, f)}
        response = requests.post(uri+'upload/'+room_code, files=files)
        print(f'Response status code: {response.status_code}')
    return 

# Download a file with given filename and room code
def download(uri, room_code, filename, chunk_size):
    def ask_file_save_location(filename, file_extension):
        # Additional arguments for filedialog.asksaveasfilename();
        #   provides default file extensions to users for selection.
        file_types = [('Text files', '*.txt'),
                     ('PDF files', '*.pdf'),
                     ('JPG files', '*.jpg'),
                     ('JPEG files', '*.jpeg'),
                     ('PNG files', '*.png'),
                     ('All files', '*.*')]
        
        root = tk.Tk()
        root.withdraw() # This hides the main window of Tk
        save_path = filedialog.asksaveasfilename(defaultextension=file_extension, 
                                               initialfile=filename,
                                               filetypes=file_types)
        return save_path
    
    # Setting 'stream' to True allows the client to download the file without loading it into memory
    response = requests.get(uri+'download/'+room_code+'/'+filename, stream=True)
    print(f'Response status code: {response.status_code}')
    
    file_extension = get_file_extension(filename)
    print('file ext:', file_extension)
    save_path = ask_file_save_location(filename, file_extension)
    try: 
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
        file_dir_path = get_file_dir_path(save_path)
        print(f'✅ File [{filename}] downloaded successfully. It is stored in [{file_dir_path}].')
    except Exception as e:
        print(f'❌ Failed to download file [{filename}].')
        print(f'Failed reason: {e}.')
    return
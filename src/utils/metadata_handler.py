import os

def add_folder_metadata(documents):
    for doc in documents:
        folder = os.path.dirname(doc.metadata['file_path'])
        doc.metadata['folder'] = folder
    return documents
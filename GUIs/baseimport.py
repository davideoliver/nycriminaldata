import pandas as pd 
import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def dload(progress_callback=None):

    print("baseimport.py loaded")
    api = KaggleApi()
    api.authenticate()
    dataset = "aniket0712/nypd-complaint-data-historic"
    file_name = "NYPD_Complaint_Data_Historic.csv"
    os.makedirs("datasets", exist_ok=True)
    file_path = os.path.join("datasets", file_name)

    if not os.path.exists(file_path):
        """
        Prompt: I'd like to add a loading bar to the load function in mainGUI.py,
        basing on the progress of the api.dataset_download_files function in baseimport.py
        """
        if progress_callback:
            progress_callback(0, "Isso pode demorar um tempo...")
        api.dataset_download_files(dataset, path="datasets", unzip=True)
        if progress_callback:
            progress_callback(100, "Download concluído!")
        # Remove extra files
        for file in os.listdir("datasets/"):
            current_file_path = os.path.join("datasets/", file)
            if os.path.isfile(current_file_path) and file != file_name:
                os.remove(current_file_path)
    else:
        if progress_callback:
            progress_callback(1000, "O arquivo já existe.")
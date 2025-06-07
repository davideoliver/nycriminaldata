import pandas as pd
import os
FILE_TO_CHECK = "NYPD_Complaint_Data_Historic.csv"
FOLDER = "datasets"

df = pd.read_csv(os.path.join(FOLDER, FILE_TO_CHECK))

reduced_df = df.sample(frac=0.25, random_state=1)
reduced_df.to_csv(os.path.join(FOLDER, FILE_TO_CHECK), index=False)
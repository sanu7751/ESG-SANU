import pandas as pd
import os

class Data:
    def paths(self, data_path):
        # Paths to data files
        esg_path = os.path.join(data_path, "ESG")
        self.file_paths = {
            "conn": os.path.join(data_path, "connections.csv"),
            "data": os.path.join(data_path, "data_as_csv.csv"),
            "embed": os.path.join(data_path, "pca_embeddings.csv"),
            "avg_esg": os.path.join(esg_path, "average_esg_scores.csv"),
            "daily_esg": os.path.join(esg_path, "overall_daily_esg_scores.csv"),
            "E_score": os.path.join(esg_path, "daily_E_score.csv"),
            "S_score": os.path.join(esg_path, "daily_S_score.csv"),
            "G_score": os.path.join(esg_path, "daily_G_score.csv")
        }

    def read(self, start_day="jan6", end_day="jan12"):
        dir_name = f"{start_day}_to_{end_day}"

        data_path = os.path.join("Data", dir_name)
        if not os.path.exists(data_path):
            raise NameError(f"There isn't data for {dir_name}")

        self.paths(data_path)
        
        data = {
            key: pd.read_csv(path, parse_dates=["date"], infer_datetime_format=True, index_col="date")
            if "score" in key else pd.read_csv(path)
            for key, path in self.file_paths.items()
        }

        # Convert DATE column to date (not timestamp) for "data"
        data["data"]["DATE"] = pd.to_datetime(data["data"]["DATE"]).dt.date

        # Multiply tones by a large number
        esg_keys = ["E_score", "S_score", "G_score", "daily_esg", "avg_esg"]
        for key in esg_keys:
            numeric_cols = data[key].select_dtypes(include=["number"]).columns
            data[key][numeric_cols] *= 10000

        return data

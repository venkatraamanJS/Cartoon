import os
import sys
from six.moves import urllib
import zipfile
import shutil
from Cartoon.logger import logging
from Cartoon.exception import CartoonException
from Cartoon.entity.config_entity import DataIngestionConfig
from Cartoon.entity.artifact_entity import DataIngestionArtifact

# Version 1 (With Type Hinting)
# class DataIngestion:
#     def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
#def:
#data_ingestion_config: DataIngestionConfig → This is type hinting, which tells Python (and other developers) 
#that data_ingestion_config should be of type DataIngestionConfig.
# DataIngestionConfig() → This creates an instance (object) of the DataIngestionConfig class and
# sets it as the default value for data_ingestion_config.

# Version 2 (Without Type Hinting)
# class DataIngestion:
#     def __init__(self, data_ingestion_config = DataIngestionConfig()):
# def:
# This works the same way, except it does not explicitly specify the expected type of data_ingestion_config.
# Python will still assign data_ingestion_config = DataIngestionConfig() by default if no argument is passed.

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = None):
        if data_ingestion_config is None:
            data_ingestion_config = DataIngestionConfig()
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
           raise CartoonException(e, sys)
        
    
    def download_data(self)-> str:
        '''
        Fetch data from the url
        '''

        try: 
            dataset_url = self.data_ingestion_config.data_download_url
            zip_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(zip_download_dir, exist_ok=True)
            data_file_name = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_file_name)
            logging.info(f"Downloading data from {dataset_url} into file {zip_file_path}")
            urllib.request.urlretrieve(dataset_url, zip_file_path)
            logging.info(f"Downloaded data from {dataset_url} into file {zip_file_path}")
            
            return zip_file_path

        except Exception as e:
            raise CartoonException(e, sys)
        

    
    def extract_zip_file(self,zip_file_path: str)-> str:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        try:
            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(feature_store_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(feature_store_path)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {feature_store_path}")

            # Check for __MACOSX folder and delete it
            macosx_folder = os.path.join(feature_store_path, "__MACOSX")
            if os.path.exists(macosx_folder):
                shutil.rmtree(macosx_folder)
                logging.info(f"Deleted __MACOSX folder from {feature_store_path}")

            return feature_store_path

        except Exception as e:
            raise CartoonException(e, sys)
        

    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try: 
            zip_file_path = self.download_data()
            feature_store_path = self.extract_zip_file(zip_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path = zip_file_path,
                feature_store_path = feature_store_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CartoonException(e, sys)

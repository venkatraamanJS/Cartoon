import os,sys
import shutil
from Cartoon.logger import logging
from Cartoon.exception import CartoonException
from Cartoon.entity.config_entity import DataValidationConfig
from Cartoon.entity.artifact_entity import (DataIngestionArtifact,
                                                 DataValidationArtifact)

class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config

        except Exception as e:
            raise CartoonException(e, sys) 

    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = None  # No assumption initially
            missing_files = []  # List to store missing files

            # Get the feature store directory
            feature_store_path = self.data_ingestion_artifact.feature_store_path

            # Find the first folder inside feature_store_path dynamically
            subdirectories = [
                d for d in os.listdir(feature_store_path)
                if os.path.isdir(os.path.join(feature_store_path, d))
            ]

            if not subdirectories:
                logging.info(f"No subdirectories found in {feature_store_path}.")
                return False  # Fail validation if no folders exist

            # Pick the first subdirectory dynamically
            target_folder = os.path.join(feature_store_path, subdirectories[0])
            logging.info(f"Checking inside folder: {target_folder}")

            # List files inside the detected folder
            all_files = os.listdir(target_folder)
            logging.info(f"Files inside {subdirectories[0]}: {all_files}")

            # Ensure validation directory exists before writing the status file
            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)

            # Check for missing required files
            for file in self.data_validation_config.required_file_list:
                if file not in all_files:
                    missing_files.append(file)  # Add missing file to list

            # Set validation status
            validation_status = not missing_files  # True if no missing files, False otherwise

            if missing_files:
                logging.info(f"Missing required files: {missing_files}")

            # Write validation status to the file
            with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise CartoonException(e, sys)



    def initiate_data_validation(self) -> DataValidationArtifact: 
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            status = self.validate_all_files_exist()
            data_validation_artifact = DataValidationArtifact(
                validation_status=status)

            logging.info("Exited initiate_data_validation method of DataValidation class")
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            if status:
                shutil.copy(self.data_ingestion_artifact.data_zip_file_path, os.getcwd())

            return data_validation_artifact

        except Exception as e:
            raise CartoonException(e, sys)
        
    # def validate_all_files_exist(self)-> bool:
    #     try:
    #         validation_status = None

    #         all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)

    #         for file in all_files:
    #             if file not in self.data_validation_config.required_file_list:
    #                 validation_status = False
    #                 os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
    #                 with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
    #                     f.write(f"Validation status: {validation_status}")
    #             else:
    #                 validation_status = True
    #                 os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
    #                 with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
    #                     f.write(f"Validation status: {validation_status}")

    #         return validation_status

    #     except Exception as e:
    #         raise CartoonException(e, sys)


    # def validate_all_files_exist(self) -> bool:
    #     try:
    #         validation_status = None  # No assumption initially
    #         missing_files = []  # List to store missing files

    #         all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)
    #         logging.info(all_files)

    #         # Ensure validation directory exists before writing the status file
    #         os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)

    #         # Check for missing required files using a for loop
    #         for file in self.data_validation_config.required_file_list:
    #             if file not in all_files:
    #                 missing_files.append(file)  # Add missing file to list

    #         # Set validation status based on missing files
    #         if missing_files:
    #             validation_status = False  # Validation failed
    #             logging.info(f"Missing required files: {missing_files}")
    #         else:
    #             validation_status = True  # Validation successful

    #         # Write validation status to the file
    #         with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
    #             f.write(f"Validation status: {validation_status}")

    #         return validation_status

    #     except Exception as e:
    #         raise CartoonException(e, sys)
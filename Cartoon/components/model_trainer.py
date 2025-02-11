import os,sys
import yaml
import shutil
from Cartoon.utils.main_utils import read_yaml_file
from Cartoon.logger import logging
from Cartoon.exception import CartoonException
from Cartoon.entity.config_entity import ModelTrainerConfig
from Cartoon.entity.artifact_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            logging.info("Unzipping data")
            os.system("unzip Cartoon_v5.zip")
            os.system("rm Cartoon_v5.zip")

            # Ensure only one extracted folder exists
            base_data_path = "Cartoon_v5"

            # Remove any unwanted folders like __MACOSX
            if os.path.exists("__MACOSX"):
                shutil.rmtree("__MACOSX")
                logging.info("Removed __MACOSX directory")

            # Ensure the correct file paths
            data_yaml_path = os.path.join(base_data_path, "data.yaml")

            # Read number of classes from data.yaml
            with open(data_yaml_path, 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = int(num_classes)

            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            # Run training command using the correct paths
            os.system(f"cd yolov5/ && python train.py --img 416 --batch {self.model_trainer_config.batch_size} "
                      f"--epochs {self.model_trainer_config.no_epochs} --data ../{data_yaml_path} "
                      f"--cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} "
                      f"--name yolov5s_results --cache")

            os.system("cp yolov5/runs/train/yolov5s_results/weights/best.pt yolov5/")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            os.system(f"cp yolov5/runs/train/yolov5s_results/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")

            # Clean up
            os.system("rm -rf yolov5/runs")
            shutil.rmtree(base_data_path)  # Delete the entire Cartoon_v5 folder
            logging.info(f"Removed extracted folder: {base_data_path}")

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise CartoonException(e, sys)




# class ModelTrainer:
#     def __init__(
#         self,
#         model_trainer_config: ModelTrainerConfig,
#     ):
#         self.model_trainer_config = model_trainer_config

#     def initiate_model_trainer(self,) -> ModelTrainerArtifact:
#         logging.info("Entered initiate_model_trainer method of ModelTrainer class")

#         try:
#             logging.info("Unzipping data")
#             os.system("unzip Cartoon_v5.zip")
#             os.system("rm Cartoon_v5.zip")

#             with open("data.yaml", 'r') as stream:
#                 num_classes = str(yaml.safe_load(stream)['nc'])

#             model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
#             print(model_config_file_name)

#             config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")

#             config['nc'] = int(num_classes)


#             with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
#                 yaml.dump(config, f)

#             os.system(f"cd yolov5/ && python train.py --img 416 --batch {self.model_trainer_config.batch_size} --epochs {self.model_trainer_config.no_epochs} --data ../data.yaml --cfg ./models/custom_yolov5s.yaml --weights {self.model_trainer_config.weight_name} --name yolov5s_results  --cache")
#             os.system("cp yolov5/runs/train/yolov5s_results/weights/best.pt yolov5/")
#             os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
#             os.system(f"cp yolov5/runs/train/yolov5s_results/weights/best.pt {self.model_trainer_config.model_trainer_dir}/")
           
#             os.system("rm -rf yolov5/runs")
#             os.system("rm -rf train")
#             os.system("rm -rf test")
#             os.system("rm -rf data.yaml")

#             model_trainer_artifact = ModelTrainerArtifact(
#                 trained_model_file_path="yolov5/best.pt",
#             )

#             logging.info("Exited initiate_model_trainer method of ModelTrainer class")
#             logging.info(f"Model trainer artifact: {model_trainer_artifact}")

#             return model_trainer_artifact


#         except Exception as e:
#             raise CartoonException(e, sys)





    
    
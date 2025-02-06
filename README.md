# Cartoon_Character_Object_Detection
Detect cartoon characters in images

## Workflows

- constants
- config_entity
- artifact_entity
- components
- pipeline
- app.py

## Project Configuration

```bash
#install aws cli from the following link

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```

```bash
#Configure aws crediential (secret key & access key)

aws configure
```


```bash
#Create a s3 bucket for model pusher. name is mentioned in the consrtant

```

## How to run:

```bash
conda create -n Cartoon python=3.8 -y
```

```bash
conda activate Cartoon
```
```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
``
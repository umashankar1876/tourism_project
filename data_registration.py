
import os
import pandas as pd
from huggingface_hub import HfApi, login, hf_hub_download
from google.colab import userdata # Keep for local testing in Colab, remove for direct CI/CD
import shutil # Added for shutil.copy

# Retrieve HF Token from environment (for GitHub Actions) or userdata (for Colab)
HF_TOKEN = os.getenv('HF_TOKEN')
if HF_TOKEN is None: # Fallback for local Colab testing if not set as env var
    HF_TOKEN = userdata.get('HF_TOKEN')

# Hardcoded for the project scope, or could be passed as environment variables
HF_USERNAME     = 'umas1990'
HF_DATASET_REPO = f'{HF_USERNAME}/tourism-dataset'

# Authenticate with Hugging Face
login(token=HF_TOKEN, add_to_git_credential=True)
print(f'Logged in to Hugging Face as {HF_USERNAME}')

api = HfApi()

# Create the dataset repository on Hugging Face (safe to rerun)
api.create_repo(repo_id=HF_DATASET_REPO, repo_type='dataset', exist_ok=True)
print(f'HF dataset repo ready: https://huggingface.co/datasets/{HF_DATASET_REPO}')

# Define the local path for the raw tourism.csv
LOCAL_TOURISM_CSV = 'tourism_project/data/tourism.csv'

# Check if the local tourism.csv exists, if not, download it (e.g., for local testing scenario)
if not os.path.exists(LOCAL_TOURISM_CSV):
    print(f"Local {LOCAL_TOURISM_CSV} not found, attempting to download from existing HF repo...")
    try:
        # Assuming a previous successful run might have pushed it
        raw_path = hf_hub_download(repo_id=HF_DATASET_REPO, filename='tourism.csv', repo_type='dataset')
        os.makedirs(os.path.dirname(LOCAL_TOURISM_CSV), exist_ok=True)
        shutil.copy(raw_path, LOCAL_TOURISM_CSV)
        print(f"Downloaded tourism.csv to {LOCAL_TOURISM_CSV}")
    except Exception as e:
        print(f"Could not download tourism.csv: {e}. Please ensure it's in tourism_project/data/")
        # Exit if the file is critical and not found
        exit(1)
else:
    print(f"Using existing local {LOCAL_TOURISM_CSV}")

# Upload tourism.csv to the HF dataset hub
api.upload_file(
    path_or_fileobj=LOCAL_TOURISM_CSV,
    path_in_repo='tourism.csv',
    repo_id=HF_DATASET_REPO,
    repo_type='dataset',
)
print(f'tourism.csv uploaded to HF: {HF_DATASET_REPO}')

# Verification after writing
if os.path.exists('/content/tourism_project/data_registration.py'):
    print('data_registration.py successfully created.')
else:
    print('Error: data_registration.py was not created.')

"""register_data.py — GitHub Actions: register-dataset job.
Creates HF dataset repo and uploads tourism.csv."""
import os
import sys
from huggingface_hub import HfApi, login

# Fetch token safely and clear out any weird trailing whitespaces/newlines
hf_token = os.environ.get('HF_TOKEN', '').strip()

if not hf_token:
    print("CRITICAL: The 'HF_TOKEN' environment variable is missing or empty!")
    sys.exit(1)

# FIXED: Explicitly disables saving credentials to the ephemeral runner's git helper
login(token=hf_token, add_to_git_credential=False)
api = HfApi()

HF_USER = os.getenv('HF_USER', 'umas1990') 
DATASET_REPO = f'{HF_USER}/tourism-dataset'

api.create_repo(repo_id=DATASET_REPO, repo_type='dataset', exist_ok=True)
print(f'Dataset repo: https://huggingface.co/datasets/{DATASET_REPO}')

# FIXED PATH: Targets the repository root path context correctly
api.upload_file(
    path_or_fileobj='data/tourism.csv',  
    path_in_repo='tourism.csv',
    repo_id=DATASET_REPO,
    repo_type='dataset',
)
print('tourism.csv registered on Hugging Face Hub.')

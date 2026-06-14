"""register_data.py — GitHub Actions: register-dataset job.
Creates HF dataset repo and uploads tourism.csv."""
import os
from huggingface_hub import HfApi, login

# HF_TOKEN is now expected to be an environment variable set in GitHub Actions
login(token=os.environ['HF_TOKEN'])
api = HfApi()

# HF_USER is also expected to be an environment variable or directly hardcoded if constant
# For consistency with other scripts, let's assume HF_USER is passed via environment
# or use a default if not found, but for CI/CD, it's usually explicitly set.
HF_USER = os.getenv('HF_USER', 'umas1990') # Use default if not set as env var
DATASET_REPO = f'{HF_USER}/tourism-dataset'

api.create_repo(repo_id=DATASET_REPO, repo_type='dataset', exist_ok=True)
print(f'Dataset repo: https://huggingface.co/datasets/{DATASET_REPO}')

api.upload_file(
    path_or_fileobj='tourism_project/data/tourism.csv',
    path_in_repo='tourism.csv',
    repo_id=DATASET_REPO,
    repo_type='dataset',
)
print('tourism.csv registered on Hugging Face Hub.')

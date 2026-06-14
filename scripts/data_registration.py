"""data_registration.py — GitHub Actions: register-dataset job.
Combines explicit client token isolation with targeted folder uploads."""
import os
import sys
from huggingface_hub import HfApi
from huggingface_hub.utils import RepositoryNotFoundError

# 1. Fetch token directly from the environment matrix
hf_token = os.environ.get('HF_TOKEN', '').strip()

if not hf_token:
    print("CRITICAL: The 'HF_TOKEN' environment variable is missing or empty in the runner!")
    sys.exit(1)

# 2. Initialize the API client by injecting the token string directly (Bypasses global login bugs!)
api = HfApi(token=hf_token)

# 3. Configure destination parameters
HF_USER = os.getenv('HF_USER', 'umas1990') 
DATASET_REPO = f'{HF_USER}/tourism-dataset'
REPO_TYPE = "dataset"

# 4. Safe lookup and registration layer
try:
    api.repo_info(repo_id=DATASET_REPO, repo_type=REPO_TYPE)
    print(f"Dataset Repository '{DATASET_REPO}' already exists. Proceeding to sync...")
except RepositoryNotFoundError:
    print(f"Dataset Repository '{DATASET_REPO}' not found. Initializing new repository asset...")
    api.create_repo(repo_id=DATASET_REPO, repo_type=REPO_TYPE, private=False)
    print(f"Dataset Repository '{DATASET_REPO}' successfully created.")

# 5. Sync the entire data folder relative to the GitHub Action root path context
try:
    api.upload_folder(
        folder_path="tourism_project/data", # Points to root data directory unpacked by actions/checkout
        repo_id=DATASET_REPO,
        repo_type=REPO_TYPE,
    )
    print('✅ Complete dataset folder assets successfully registered on Hugging Face Hub.')
except Exception as e:
    print(f"❌ Upload failed dynamically: {str(e)}")
    sys.exit(1)

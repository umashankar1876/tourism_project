from huggingface_hub.utils import RepositoryNotFoundError
from huggingface_hub import HfApi
import os

repo_id = "umas1990/tourism-dataset"
repo_type = "dataset"

# Initialize API client
api = HfApi(token=os.getenv("HF_TOKEN"))

# Step 1: Check if the repository exists
try:
    api.repo_info(repo_id=repo_id, repo_type=repo_type)
    print(f"Repository '{repo_id}' already exists. Using it.")
except RepositoryNotFoundError:
    print(f"Repository '{repo_id}' not found. Creating new repository...")
    api.create_repo(repo_id=repo_id, repo_type=repo_type, private=False)
    print(f"Repository '{repo_id}' created.")

# Step 2: Sync the data directory asset folder
api.upload_folder(
    folder_path="data",
    repo_id=repo_id,
    repo_type=repo_type,
)
print("✅ Complete dataset folder assets successfully registered on Hugging Face Hub.")

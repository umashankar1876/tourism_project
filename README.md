# ✈️ Tourism Package Predictor & MLOps Pipeline

[![Tourism Project Pipeline](https://github.com/umashankar1876/tourism_project/actions/workflows/main.yml/badge.svg)](https://github.com/umashankar1876/tourism_project/actions)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/umas1990/tourism-app)

An end-to-end Machine Learning Operations (MLOps) pipeline that builds, tracks, evaluates, and dynamically deploys a predictive model focused on predicting specialized tourism packages. 

The web application frontend is built using **Streamlit**, containerized using **Docker**, and dynamically synchronized directly with **Hugging Face Spaces** via GitHub Actions CI/CD workflows.

---

## 🏗️ System Architecture & Directory Structure

```text
tourism_project/
├── .github/
│   └── workflows/
│       └── main.yml           # Automated MLOps GitHub Actions Pipeline
├── data/                      # Raw and prepared datasets
├── deployment/
│   ├── app.py                 # Streamlit Web Application Interface
│   ├── Dockerfile             # Hardened security container layer configuration
│   └── requirements.txt       # Environment dependencies with explicit pinning
└── model_building/            # Python orchestration scripts & notebooks for model execution

# GitHub Actions Workflow: Deploy to Google Cloud Run

## Overview

This document offers a high-level breakdown of the GitHub Actions workflow defined in the `.github/workflows/deploy_GCR.yaml` file.
The primary purpose of this workflow is to streamline the process of deploying a Docker containerized application to
Google Cloud Run upon code pushes to the `main` branch.

### Workflow Triggers

- Triggered upon every `push` event to the `main` branch. Ensure you adjust for your production branch if it's different from `main`.

## Step-by-Step Workflow Breakdown

1. **📥 Checkout**
    - Retrieves the current repository's code so the subsequent workflow steps can access it.

2. **📧 Extract `client_email` Field**
    - The `client_email` field from the Google Cloud Service Account JSON key is extracted. This email is essential for authenticating with Google Cloud in the subsequent steps.

3. **☁️ Setup Google Cloud CLI**
    - Initiates the Google Cloud Command Line Interface to facilitate interactions with Google Cloud services.

4. **🔐 Authenticate to Google Cloud with Workload Identity Provider**
    - Uses the previously extracted `client_email` and the Service Account JSON key to authenticate with Google Cloud, ensuring secure interactions for the following steps.

5. **🐳 Build Docker Image**
    - Constructs a Docker image from the checked-out code. This image is tagged suitably to be pushed to Google's Container Registry (GCR) in the next step.

6. **📤 Push Docker Image to Google Container Registry (GCR)**
    - Before pushing, Docker's authentication is configured to interact with GCR. The Docker image built in the previous step is then pushed to GCR.

7. **🚢 Deploy to Google Cloud Run**
    - The Docker image stored in GCR is deployed to Google Cloud Run, ensuring the application is live and accessible.
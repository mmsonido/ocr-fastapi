"""
deploy.py
Automates Docker image build and deployment to Google Cloud Run for the OCR FastAPI project.
"""
import subprocess
import sys
import os
import logging
from dotenv import load_dotenv
load_dotenv()

DOCKER_IMAGE = os.getenv("DOCKER_IMAGE")
SERVICE_NAME = os.getenv("SERVICE_NAME")
REGION = os.getenv("REGION")
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def check_env_vars():
    missing = [var for var in ["DOCKER_IMAGE", "SERVICE_NAME", "REGION"] if not os.getenv(var)]
    if missing:
        logging.error(f"Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

def run_command(cmd: str) -> None:
    """
    Runs a shell command and streams output. Raises RuntimeError on failure.
    """
    logging.info(f"[Running] {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {cmd}\nError: {e}")
        raise

def ensure_buildx() -> None:
    """
    Ensures Docker buildx is enabled and in use.
    """
    result = subprocess.run(["docker", "buildx", "ls"], capture_output=True, text=True)
    if "*" not in result.stdout:
        run_command("docker buildx create --use")
    else:
        logging.info("Docker buildx already enabled.")

def build_and_push_image() -> None:
    """
    Builds and pushes the Docker image for linux/amd64 platform.
    """
    cmd = (
        f"docker buildx build "
        f"--platform linux/amd64 "
        f"-t {DOCKER_IMAGE} "
        f"--push ."
    )
    run_command(cmd)

def deploy_to_cloud_run() -> None:
    """
    Deploys the Docker image to Google Cloud Run.
    """
    cmd = (
        f"gcloud run deploy {SERVICE_NAME} "
        f"--image {DOCKER_IMAGE} "
        f"--platform managed "
        f"--region {REGION} "
        f"--allow-unauthenticated "
        f"--timeout=600s "
        f"--memory=4Gi "
        f"--cpu=4"
    )
    run_command(cmd)

def main() -> None:
    """
    Main deployment workflow. Checks environment, builds, and deploys.
    """
    try:
        check_env_vars()
        ensure_buildx()
        build_and_push_image()
        deploy_to_cloud_run()
        logging.info("[Success] Deployment complete.")
    except Exception as e:
        logging.error(f"Deployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

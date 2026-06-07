FROM astrocrpublic.azurecr.io/runtime:3.2-4

USER root

# Install uv for efficient package management
RUN pip install uv

# Create the workspace
RUN mkdir -p /opt/airflow/projects

# COPY only the project configuration/source
# We use COPY here so the image is self-contained for production
COPY projects/ /opt/airflow/projects/
COPY requirements.txt /opt/airflow/

# Install global requirements first
RUN uv pip install --system -r /opt/airflow/requirements.txt

# Install the projects so they are 'baked into' the image
RUN find /opt/airflow/projects/ -name "pyproject.toml" -execdir uv pip install --system -e . \;

USER astro
# syntax=docker/dockerfile:1
# Start with Ubuntu 20.04
FROM ubuntu:20.04

# Set the working directory
WORKDIR /usr/src/app

# Install curl and dependencies for the ODBC driver
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    g++ \
    unixodbc-dev \
    libpq-dev

# Update package index and upgrade packages
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y wget bzip2 ca-certificates curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add SSL certs (remove this if not an ARUP user)
# ---------------------------------------------------------
COPY ./build/*.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
# ---------------------------------------------------------

# Install Miniconda
RUN curl -s https://api.github.com/repos/conda-forge/miniforge/releases/latest | grep "browser_download_url.*Linux-x86_64.sh" | cut -d : -f 2,3 | tr -d \" | wget -O ~/miniforge.sh -qi - && \
    bash ~/miniforge.sh -b -p /opt/conda && \
    rm ~/miniforge.sh && \
    /opt/conda/bin/conda clean -t -i -p -y
ENV PATH="/opt/conda/bin:${PATH}"

# Set SSL for Conda (remove this if not an ARUP user)
# ---------------------------------------------------------
RUN conda config --set ssl_verify "/usr/local/share/ca-certificates/curl-ca-bundle.crt"
# ---------------------------------------------------------

# Copy individual files
COPY environment.yml ./

# Create the Conda environment
RUN conda env create -f environment.yml

# Activate the environment and ensure it's active in future RUN directives
SHELL ["conda", "run", "-n", "geoenv", "/bin/bash", "-c"]

# Verify the Python version to ensure Python is installed
RUN conda run -n geoenv python --version

# Set the default shell to use the conda environment
SHELL ["conda", "run", "-n", "geoenv", "/bin/bash", "-c"]

# Make RUN commands use the new environment
RUN echo "conda activate geoenv" >> ~/.bashrc

# Start a shell when the container launches to keep it open for development
CMD ["bash"]
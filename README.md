# geospatial_demo

## Purpose of This Repository

This repository is designed as a demonstration for Arup employees and working environment for geospatial data analysis using Python. It includes examples and tools for working with geospatial data, visualizing data using Folium, and setting up a reproducible Python environment.

## Set Up

To set up the development environment for this project, you'll need to have the following tools and software installed:

1. **bash**: A Unix shell and command language.
2. **miniforge**: A minimal installer for conda specific to conda-forge.
3. **vscode (Visual Studio Code)**: A powerful, open-source code edito

Additionally, you will need the following VSCode extensions:

- **Python**: Provides rich support for the Python language.
- **Python Environment Manager**: Helps manage your Python environments.
- **Jupyter**: Supports Jupyter notebooks in VSCode.

### Step-by-Step Instructions

#### Create and Activate Virtual Environment

A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus several additional packages.

1. Open your terminal (bash).
2. Navigate to your project directory.
3. Create the virtual environment using the provided `environment.yml` file:

    ```bash
    conda env create -f environment.yml
    ```

4. (Optional) If you add new packages, run this to update:

    ```bash
    conda env update -f environment.yml --prune
    ```

#### Install Additional Packages

If you need to install additional packages after setting up your environment, you can do so using `conda` or `pip`. Remember to update the `environment.yml` file afterward.

#### Updating environment.yml

If you add new packages to your environment, you should update the `environment.yml` file to capture these changes. Run the following command to export the current state of your environment:

    ```bash
    conda env export --no-builds > environment.yml
    ```

### Example environment.yml

The `environment.yml` file is used to specify the dependencies and configuration of your Conda environment. Here is an example structure of an `environment.yml` file:

```yaml
name: geoenv
channels:
  - conda-forge
dependencies:
  - python=3.10
  - numpy
  - pandas
  - folium
  - geopandas
  - pip
  - pip:
    - some-pip-package
```

## Trouble Shooting

## Miniforge Installation Issues

If you are having issues installing or using Miniforge please refer to the Arup guides below. 

[Arup Install Guide](https://arup.sharepoint.com/sites/network-software-development/SitePages/Installing-Python.aspx)
[Arup Problems with Miniforge Installation Guide](https://arup.sharepoint.com/sites/network-software-development/SitePages/Problems-with-Miniforge-Installation.aspx)

## SSL Issues

If you are having issues installing packages you may need to follow the below guide.

[Arup SSL issue guide](https://arup.sharepoint.com/sites/network-software-development/SitePages/SSL-Certificates.aspx?xsdata=MDV8MDF8fDkzNjI3OGU5Yjc0YjQzODViNGEwMDhkYjE5N2VhZmRhfDRhZTQ4YjQxMDEzNzQ1OTk4NjYxZmM2NDFmZTc3YmVhfDB8MHw2MzgxMzE4MDQxMDk5NzY3MzZ8VW5rbm93bnxWR1ZoYlhOVFpXTjFjbWwwZVZObGNuWnBZMlY4ZXlKV0lqb2lNQzR3TGpBd01EQWlMQ0pRSWpvaVYybHVNeklpTENKQlRpSTZJazkwYUdWeUlpd2lWMVFpT2pFeGZRPT18MXxNVFkzTnpVNE16WXdPVFl3TVRzeE5qYzNOVGd6TmpBNU5qQXhPekU1T2pZek5EbGpPREUxTFRKbU1UUXROR0ZsTkMxaU9USmlMVEZqTmpjeVpEQm1NbVF5TVY4NE5EbGpNMkk0WWkwM05HVmxMVFJtT0RVdE9EazRaQzB4TlRkbVlUSTVOMlV5T1RoQWRXNXhMbWRpYkM1emNHRmpaWE09fDhiMzZlNzJmMjVmNzRkYWU1MjViMDhkYjE5N2VhZmQ4fGYzNTU4ZjY3ZTQ4ZjRmMzI5Nzg4ODUzMTcyYTI1ZDEx&sdata=ckI2Rzlwc1NOMStNVEs3MjlkTTZubkhUcXdRd3IrUkhRQVVwWldaTzNobz0%3D&ovuser=4ae48b41-0137-4599-8661-fc641fe77bea%2CChris.Wynne%40arup.com&OR=Teams-HL&CT=1677583612092&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yMzAyMDUwMTQwMyIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D)

## Running Conda in Bash

If you are encountering issues using conda in Bash you may need to follow these steps. To set up a Conda environment using Miniforge in Git Bash, follow these steps:

#### Step-by-Step Instructions

1. **Locate the Conda Executable**:
   Ensure Miniforge is installed on your system. By default, Miniforge installs Conda executables in the `AppData\Local\miniforge3` directory.

2. **Open Git Bash**:
   Open Git Bash and navigate to the directory where Miniforge is installed. For example:
   ```sh
   cd /c/Users/your-username/AppData/Local/miniforge3
   ```

3. **Edit the .bashrc File**:
    Open the .bashrc file in a text editor to add the Miniforge path:
    ```sh
    nano ~/.bashrc
    ```

4. **Add Miniforge to PATH and Create an Alias**:
   Add the following lines to the end of the .bashrc file. Make sure to replace your-username with your actual username.
   ```sh
    export PATH="$PATH:/c/Users/your-username/AppData/Local/miniforge3"
    alias conda='/c/Users/your-username/AppData/Local/miniforge3/_conda.exe'
    ```

5. **Save and Exit Nano**:
    - Press Ctrl + O to write the changes.
    - Press Enter to confirm the file name.
    - Press Ctrl + X to exit Nano.

6. **Apply the Changes**:
   ```sh
   source ~/.bashrc
   ```

7. **Verify Conda installation**:
    ```sh
    conda --version
    ```

By following these steps, you will ensure that the Conda executable is correctly recognized in your Git Bash terminal, allowing you to manage your Conda environments effectively.
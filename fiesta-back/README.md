# web-fiesta
Fiesta, on the web.

## HTTP REST server
The REST backend server is served via Flask in Python.
### Setup the conda environment
Python dependencies are managed via a conda environment.  
The description of the `fiesta` environment is contained within the `environment.yml` file.  

In order to replicate locally the environment, type:  
`conda env create -f environment.yml`  
Check that the `fiesta` environment is now listed:   
`conda env list`  
The conda env. is now setup.
### Launch server script
Activate the `fiesta` conda env.  
`conda activate fiesta`  
Launch the api server.   
`python server/api.py`  
# JETSON NANO AND AWS SERVER CONNECTION

This repo includes 2 scripts:
  * scripts_jetsonnano_to_database : send check-in data from jetson nano to server (database and S3 storage).
  * scripts_database_to_jetsonnano : get student's data which wasn't trained from server to jetsonnano, change trained status field.
  
 ## Note:
  This repo is missing `config.ini` file. Please contact me to get it!
  Don't upload file `config.ini` to the internet!
  
  ## Installation
  
  To run scripts, you need to clone this repo and initialize the enviroment:
```
git clone https://github.com/tronghuuphan/python-database-s3.git
pip install pipenv
pipenv install
pipenv shell
```
 

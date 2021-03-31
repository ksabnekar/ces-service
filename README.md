""" Steps for setting up repo development """

1.	Create a virtual environment:
    > 	Python -m venv virtualEnv
     -   “virtualEnv” is the name set for your virtual environment.

2.	Now run your virtual environment by running the activation script. First navigate to the virtualEnv\Scripts directory:
    >	cd virtualEnv\Scripts
    Then enter 'activate'

3.	Your virtual environment pip might need to be upgraded:
    >	python.exe -m pip install --upgrade pip
    
4.	Now pip install the "requirements.txt" file. Use the command:
    >	pip install requirements.txt

If you get an error that states: 
    "ERROR: Could not find a version that satisfies the requirement requirements.txt (from versions: none)
    ERROR: No matching distribution found for requirements.txt"
Try the following command instead:
   >	pip install -r requirements.txt

5. In order to run the server, we first must migrate the files (Make sure you are in the ces-service directory to run the below commands)
   >    python manage.py makemigrations
    - makemigrations: which is responsible for creating new migrations based on the changes you have made to your models.
   
   >    python manage.py migrate
    - migrate: which is responsible for applying and unapplying migrations

6. We can start the web server by running:
   >    python manage.py runserver
    - This should be running on your local host under the port 8080.
    - Example: http://127.0.0.1:8080/
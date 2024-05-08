# ♕ Chess Arena Manager ♔

This script facilitates the organization and management of chess tournaments, including player registration, round tracking, match scheduling, and result recording.

## How it works

### - Player Management
Players' information is stored in JSON files, allowing for offline access and management. Each player's data includes their last name, first name, and date of birth.

### - Tournament Management
Tournament data is persisted in JSON files, located in the data/tournaments directory. Each tournament includes details such as its name, location, start and end dates, number of rounds, current round number, and a list of registered players.

### - Tournament Rounds and Matches
Tournaments consist of multiple rounds, each containing a list of matches.
Each match consists of a pair of players, with results determining points awarded.

### - Reporting
The application provides various reports, including lists of players, tournaments, tournament details, player lists per tournament, and round and match lists per tournament. Reports can be exported for future use.

### - Data Saving and Loading
Program state is saved and loaded between user actions.

### - Code Structure and Maintenance
The code follows the Model-View-Controller (MVC) design pattern, with three main packages: models, views, and controllers.
Code cleanliness and maintainability are ensured through adherence to PEP 8 guidelines, with the use of flake8 for code formatting and linting.

## Requirements

- Python 3.6 or later

## How to run

Once the code has been downloaded, go to the project directory and enter the following commands in terminal :

  `python -m venv env` *install a new vitual environement*
    
  `env/Scripts/activate` *activate the environement*
    
  `pip install -r requirements.txt` *install all the depedencies*
    
  `python main.py` *run the code*

  `deactivate` *when over, deactivate the environement*

## How to use Flake8

Once you are in the directory containing your Python files.

Run Flake8 by executing the following command:
  
  `flake8 --format=html --htmldir=flake-report .`
  
> [!NOTE]
> The commands above are for Windows use. Go to the official [Python documentation](https://docs.python.org/3/tutorial/venv.html) for MacOS or Unix usage.

## Contact
Feel free to [mail me](mailto:mas.ste@gmail.com) for any questions, comments, or suggestions.


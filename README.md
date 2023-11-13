# URL, IP Parser

A simple program for searching URL and IP addresses in text based on keywords and storing each record in a database with a reference to the source. Supported formats include CSV and text files.

## Installation

1. **Install Python:**
   - Download: [python.org/downloads](https://www.python.org/downloads/)
   - Check the version using the command: `python --version`

2. **Install PostgreSQL and pgAdmin:**
   - Download pgAdmin: [pgadmin.org/download](https://www.pgadmin.org/download/)
   - Create your database in pgAdmin.


3. **Download the program:**
   - Open your IDE and navigate to the project folder.
   - Open the config.ini file and update the information according to your created database in pgAdmin.

4. **Install Dependencies:**
   - Open the terminal in the project folder.
   - Run the command: `pip install -r requirements.txt`
   - Check installed packages: `pip freeze`

## Running

1. **Prepare the configuration file:**
   - Edit the `config.json` file and add the URL sources you want to analyze.

2. **Run the program:**
   - Open the terminal in the project folder.
   - Execute the command: `python main.py`

3. **Check logs:**
   - Logs can be toggled on or off in the `main.py` file.

You can check the records in pgAdmin or through the command line.

## Authors

- [@TomasBalbinder](https://github.com/TomasBalbinder)
## License

[MIT](https://choosealicense.com/licenses/mit/)


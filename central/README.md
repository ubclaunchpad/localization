# Setup
1. Install Python 3.12
2. Setup a virtual environment. To do this, run `python3 -m venv env`
3. Activate the virtual environment. 
a. On mac, run `source env/bin/activate`
b. On windows, run `venv\Scripts\activate` or `activate`
4. Now, run `pip install -r requirements.txt` to install all project dependencies

# Run the app
1. Run `python3 run.py`
2. Click on the link in the terminal, `http://127.0.0.1:8000`
3. You should see a JSON message pop up:
```
{
  "message": "hey"
}
```

### How the app is structured
Premature optimization is the root of all evil. Same goes with excessive structuring
`central api` will follow a very simple directory structure that can later on be refactored

The `src` folder contains everything the app needs to run
`routes` contains business logic
&nbsp; &nbsp; &nbsp; &nbsp; `__init__.py` sets up our flask app
&nbsp; &nbsp; &nbsp; &nbsp; `server.py` is what we will write our application code in

***Central will be a REST API***


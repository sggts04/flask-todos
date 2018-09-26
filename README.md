# Todos WebApp
This is the code for Todos WebApp built in Flask, with a user system built through json files.
The site is live on http://sggts04.pythonanywhere.com/ however it is expected to be on a more updated state than this repo.

## Installation
For testing, editing or playing around with the code, you can download the app to your local machine:
```
git clone https://github.com/sggts04/flask_todos
cd flask_todos
pip install -r requirements.txt
```
Now, edit app.py and set ```app.config['SECRET_KEY'] = "secret_key_here"``` to your own secret key instead of ```secret_key_here```.
Then run
```
python app.py
```
or ```python3 app.py``` or ```python3.7 app.py``` depending on how python is set up on your machine, please note that this is built in Python 3.7
Then the app will be available on http://127.0.0.1:5000/ then. However, the live site is [here](http://sggts04.pythonanywhere.com/) which you can't edit :)    
## Video
A video demonstrating(an older version) this app: https://www.youtube.com/watch?v=Ecf2_Wc0SxI    

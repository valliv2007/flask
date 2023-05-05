from flask import Flask, render_template

from utils.decorators import responce

app = Flask(__name__)

def get_films():
    return  [{
        'id':1,
        'name': 'HP',
        'date': '18 January 2023'
    },
    {
        'id':2,
        'name': 'HP2',
        'date': '18 January 2024'
    }]

@app.route('/')
@app.route('/hello')
@responce(template_file='hello.html')
def index():
    films = get_films()
    return {'films': films}

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/<string:name>')
def greeting(name:str):
    return f'Hello, {name.capitalize()}'

if __name__ =='__main__':
    app.run()

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from scraping_list import MyScraperList
from scrapping_grid import MyScraperGrid
import os
import pandas as pd
app = Flask(__name__)
app.secret_key= "hakuna matata"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=['GET', 'POST'])
def form_view():
    return render_template('form.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
       flash('Data collection will start now...')
       query = request.form['query']
       searchtype = request.form['page']
       if searchtype == 'list':
            scraper = MyScraperList(query)
            scraper.collect_all()
            path = os.path.join('static', 'mined', f'{"_".join(query.split())}.csv')
            scraper.save(path)
            return jsonify({
                'query': query,
                'searchtype': searchtype,
                'status': 'success',
                'path': path
                })
       else:
            scraper = MyScraperGrid(query)
            scraper.collect_all()
            path = os.path.join('static', 'mined', f'{"_".join(query.split())}.csv')
            scraper.save(path)
            return jsonify({
                'query': query,
                'searchtype': searchtype,
                'status': 'success',
                'path': path
                })
    return jsonify({
        'status': 'error',
    })

@app.route('/collection', methods=['GET', 'POST'])
def list_collected_data():
    files = os.listdir(os.path.join('static', 'mined'))
    return render_template('collection.html', files=files)

@app.route('/view/<filename>')
def view_file(filename):
    path = os.path.join('static', 'mined', filename)
    df = pd.read_csv(path)
    return render_template('view_data.html', df=df.to_html(), filename=filename.split('.')[0])

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000, debug=True)
 
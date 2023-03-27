from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'AIzaSyAXbaFH6SNfc41hx6w2Xuv_oDvqNoWPumY'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    location = request.form['location']
    radius = request.form['radius']
    keyword = request.form['keyword']
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': keyword,
        'location': location,
        'radius': radius,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    results = response.json()['results']
    businesses = []
    for result in results:
        name = result['name']
        address = result['formatted_address']
        rating = result.get('rating', None)
        business = {
            'name': name,
            'address': address,
            'rating': rating
        }
        businesses.append(business)
    sorted_businesses = sorted(businesses, key=lambda x: x['rating'] or 0, reverse=True)
    return render_template('results.html', businesses=sorted_businesses)

if __name__ == '__main__':
    app.run(debug=True)

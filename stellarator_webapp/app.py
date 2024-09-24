from flask import Flask, render_template, request
import query_stellarators as qs

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        config_id = request.form.get('config_id')
        if config_id:
            result = qs.query_specific_configuration(config_id)
    return render_template('index.html', result=result)

@app.route('/plot/<int:config_id>')
def plot(config_id):
    try:
        image_url = qs.plot_stellarator(config_id)
        return render_template('plot.html', image_url=image_url)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)














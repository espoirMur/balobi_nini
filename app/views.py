from app import app
from flask import  render_template
from visualisation.terms_count import get_term_count


@app.route('/', methods=['GET', 'POST'])
def index():
    terms_counts = get_term_count()
    return render_template('word_cloud.html', terms_counts=terms_counts)

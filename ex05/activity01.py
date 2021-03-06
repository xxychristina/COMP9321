import pandas as pd
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

@api.route('/books/<int:id>')
class Books(Resource):
    def get(self, id):
        if id not in df.index:
            api.abort(404, "Book {} are not found".format(id))
        
        book = dict(df.loc[id])
        return book


if __name__=='__main__':
    #read the csv file to dataset
    df = pd.read_csv("Books.csv")

    # drop unnecessary columns
    columns_to_drop = ['Edition Statement',
                       'Corporate Author',
                       'Corporate Contributors',
                       'Former owner',
                       'Engraver',
                       'Contributors',
                       'Issuance type',
                       'Shelfmarks'
                       ]
    df.drop(columns_to_drop, inplace=True, axis=1)

    # clean the date of publication & convert it to numeric data
    new_date = df['Date of Publication'].str.extract(r'^(\d{4})', expand=False)
    new_date = pd.to_numeric(new_date)
    new_date = new_date.fillna(0)
    df['Date of Publication'] = new_date

    # set the index column; this will help us to find books with their ids
    df.set_index('Identifier', inplace=True)

    # replace spaces in the name of columns
    df.columns = [c.replace(' ', '_') for c in df.columns]

    # run the application
    app.run(debug=True)
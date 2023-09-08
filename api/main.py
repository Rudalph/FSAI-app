import firebase_admin
from firebase_admin import credentials, firestore
import csv
from flask import Flask, render_template, request, Response


app = Flask(__name__)

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate('firebase-admin-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/export_csv', methods=['POST'])
def export_csv():
    # Replace 'your_collection_name' with the name of the Firestore collection you want to export
    collection_ref = db.collection('mandals')

    # Retrieve documents from Firestore
    documents = collection_ref.stream()

    # Initialize a list to store rows (each document is a row)
    rows = []

    # Extract unique field names from all documents
    field_set = set()
    for doc in documents:
        document_data = doc.to_dict()
        field_set.update(document_data.keys())

    # Sort the field names alphabetically
    fieldnames = sorted(list(field_set))

    # Add the fieldnames as the first row in the CSV
    rows.append(fieldnames)

    # Retrieve documents again for data extraction
    documents = collection_ref.stream()

    # Iterate through documents and add their data to rows
    for doc in documents:
        document_data = doc.to_dict()
        row = [document_data.get(field, '') for field in fieldnames]
        rows.append(row)

    # Specify the name of the output CSV file
    csv_filename = 'output.csv'

    # Write the data to a CSV file
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

    def generate():
        with open(csv_filename, 'rb') as csvfile:
            data = csvfile.read()
            yield data

    # Send the CSV file as a downloadable attachment
    response = Response(generate(), content_type='text/csv')
    response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"
    return response

if __name__ == '__main__':
    app.run(debug=True)

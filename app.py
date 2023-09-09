# import firebase_admin
# from firebase_admin import credentials, firestore
# import csv
# from flask import Flask, render_template, request, Response


# app = Flask(__name__)

# # Initialize Firebase Admin SDK with your credentials
# cred = credentials.Certificate('firebase-admin-key.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/export_csv', methods=['POST'])
# def export_csv():
#     # Replace 'your_collection_name' with the name of the Firestore collection you want to export
#     collection_ref = db.collection('mandals')

#     # Retrieve documents from Firestore
#     documents = collection_ref.stream()

#     # Initialize a list to store rows (each document is a row)
#     rows = []

#     # Extract unique field names from all documents
#     field_set = set()
#     for doc in documents:
#         document_data = doc.to_dict()
#         field_set.update(document_data.keys())

#     # Sort the field names alphabetically
#     fieldnames = sorted(list(field_set))

#     # Add the fieldnames as the first row in the CSV
#     rows.append(fieldnames)

#     # Retrieve documents again for data extraction
#     documents = collection_ref.stream()

#     # Iterate through documents and add their data to rows
#     for doc in documents:
#         document_data = doc.to_dict()
#         row = [document_data.get(field, '') for field in fieldnames]
#         rows.append(row)

#     # Specify the name of the output CSV file
#     csv_filename = 'output.csv'

#     # Write the data to a CSV file
#     with open(csv_filename, mode='w', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerows(rows)

#     def generate():
#         with open(csv_filename, 'rb') as csvfile:
#             data = csvfile.read()
#             yield data

#     # Send the CSV file as a downloadable attachment
#     response = Response(generate(), content_type='text/csv')
#     response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"
#     return response

# if __name__ == '__main__':
#     app.run(debug=False)


import firebase_admin
from firebase_admin import credentials, firestore
import csv
from flask import Flask, render_template, request, Response, send_file

app = Flask(__name__)

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate('firebase-admin-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html', response1=False, response2=False, response3=False)

@app.route('/export_csv', methods=['POST'])
def export_csv():
    if request.method == 'POST':
        export_type = request.form.get('export_type')

        if export_type == 'collection1':
            collection_ref = db.collection('mandals')
            csv_filename = 'output1.csv'
        elif export_type == 'collection2':
            collection_ref = db.collection('mandalsSelectedForNext')
            csv_filename = 'output2.csv'
        else:
            # Handle invalid export_type here, e.g., return an error page
            return render_template('error.html', message='Invalid export type')

        # Retrieve documents from Firestore for the selected collection
        documents = collection_ref.stream()

        # Initialize a list to store rows (each document is a row)
        rows = []

        # Extract unique field names
        field_set = set()
        for doc in documents:
            document_data = doc.to_dict()
            field_set.update(document_data.keys())

        # Sort the field names alphabetically
        fieldnames = sorted(list(field_set))
        rows.append(fieldnames)

        # Retrieve documents again for data extraction
        documents = collection_ref.stream()

        # Iterate through documents and add their data to rows
        for doc in documents:
            document_data = doc.to_dict()
            row = [document_data.get(field, '') for field in fieldnames]
            rows.append(row)

        # Write the data to the CSV file
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

        def generate_csv():
            with open(csv_filename, 'rb') as csvfile:
                data = csvfile.read()
                yield data

        # Send the CSV file as a downloadable attachment
        response = Response(generate_csv(), content_type='text/csv')
        response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"
        return response

@app.route('/export_top_scores_csv', methods=['POST'])
def export_top_scores_csv():
    if request.method == 'POST':
        collection_ref = db.collection('mandalsSelectedForNext')
        csv_filename = 'output2_top_scores.csv'

        # Retrieve top 20 documents based on 'totalScore' attribute in descending order
        documents = collection_ref.order_by('totalScore', direction=firestore.Query.DESCENDING).limit(20).stream()

        # Initialize a list to store rows (each document is a row)
        rows = []

        # Extract unique field names
        field_set = set()
        for doc in documents:
            document_data = doc.to_dict()
            field_set.update(document_data.keys())

        # Sort the field names alphabetically
        fieldnames = sorted(list(field_set))
        rows.append(fieldnames)

        # Retrieve documents again for data extraction
        documents = collection_ref.order_by('totalScore', direction=firestore.Query.DESCENDING).limit(20).stream()

        # Iterate through documents and add their data to rows
        for doc in documents:
            document_data = doc.to_dict()
            row = [document_data.get(field, '') for field in fieldnames]
            rows.append(row)

        # Write the data to the CSV file
        with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

        def generate_csv():
            with open(csv_filename, 'rb') as csvfile:
                data = csvfile.read()
                yield data

        # Send the CSV file as a downloadable attachment
        response = Response(generate_csv(), content_type='text/csv')
        response.headers["Content-Disposition"] = f"attachment; filename={csv_filename}"
        return response

@app.route('/download_csv/<filename>')
def download_csv(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)

import data_manager
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentor-names')
def mentor_names():
    # We get back dictionaries here (for details check 'database_common.py')
    mentor_names = data_manager.get_mentor_names()

    return render_template('mentor_names.html', mentor_names=mentor_names)


@app.route('/mentor-nicknames')
def mentor_nicknames():
    mentor_nicknames = data_manager.get_mentor_nicknames('Miskolc')

    return render_template('mentor_names.html', mentor_names=mentor_nicknames, mentor_nicknames=True)


@app.route('/applicant-info/<application_code>')
def applicant_info(application_code):
    applicant_info = data_manager.get_applicant_info(application_code, search_by_code=True)
    return render_template('applicant_info.html', applicant_info=applicant_info, display_all=True)


@app.route('/find-applicant-by-first-name', methods=['GET', 'POST'])
def find_applicant_by_first_name():
    if request.method == 'GET':
        return render_template('search.html', first_name=True)
    else:
        user_input = request.form.to_dict()
        applicant_first_name = (user_input.get('first_name')).capitalize()
        applicant_info = data_manager.get_applicant_info(applicant_first_name)
        return render_template('applicant_info.html', applicant_info=applicant_info)


@app.route('/find-applicant-by-email', methods=['GET', 'POST'])
def find_applicant_by_email():
    if request.method == 'GET':
        return render_template('search.html', email=True)
    else:
        user_input = request.form.to_dict()
        applicant_email = user_input.get('email')
        applicant_info = data_manager.get_applicant_info_by_email(applicant_email)
        return render_template('applicant_info.html', applicant_info=applicant_info)


@app.route('/find_applicant_by_application_code', methods=['GET', 'POST'])
def find_applicant_by_application_code():
    if request.method == 'GET':
        return render_template('search.html', appl_code=True)
    else:
        user_input = request.form.to_dict()
        return redirect(url_for('applicant_info', application_code=user_input['application_code']))


@app.route('/add-new-applicant', methods=['GET', 'POST'])
def add_new_applicant():
    if request.method == 'GET':
        return render_template('add_applicant.html')
    else:
        user_input = request.form.to_dict()
        data_manager.append_to_database('applicants', user_input)
        return redirect(url_for('applicant_info', application_code=user_input['application_code']))


@app.route('/update-record/<table>', methods=['GET', 'POST'])
def update_record(table):
    if request.method == 'GET':
        names = data_manager.get_all_names_from_table(table)
        return render_template('update.html')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

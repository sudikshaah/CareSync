import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Patient, Doctor, Appointment, MedicalRecord, Bill

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caresync.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_secret_caresync'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    from datetime import date
    total_patients = Patient.query.count()
    active_doctors = Doctor.query.count()
    todays_appointments = Appointment.query.filter_by(date=date.today()).count()
    total_revenue = db.session.query(db.func.sum(Bill.total)).scalar() or 0.0
    recent_appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).limit(5).all()
    return render_template('dashboard.html', 
                           total_patients=total_patients, 
                           active_doctors=active_doctors, 
                           todays_appointments=todays_appointments, 
                           total_revenue=total_revenue,
                           recent_appointments=recent_appointments)

# --- PATIENTS ---
@app.route('/patients', methods=['GET', 'POST'])
def patients():
    search = request.args.get('search')
    if search:
        patients_list = Patient.query.filter(
            (Patient.name.contains(search)) | (Patient.contact.contains(search))
        ).all()
    else:
        patients_list = Patient.query.all()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']
        new_patient = Patient(name=name, age=age, gender=gender, contact=contact)
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient added successfully!')
        return redirect(url_for('patients'))

    return render_template('patients.html', patients=patients_list, search=search)

@app.route('/patients/<int:id>/edit', methods=['POST'])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)
    patient.name = request.form['name']
    patient.age = request.form['age']
    patient.gender = request.form['gender']
    patient.contact = request.form['contact']
    db.session.commit()
    flash('Patient updated successfully!')
    return redirect(url_for('patients'))

@app.route('/patients/<int:id>/delete', methods=['POST'])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!')
    return redirect(url_for('patients'))

# --- DOCTORS ---
@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    doctors_list = Doctor.query.all()
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']
        new_doctor = Doctor(name=name, specialization=specialization, contact=contact)
        db.session.add(new_doctor)
        db.session.commit()
        flash('Doctor added successfully!')
        return redirect(url_for('doctors'))
    return render_template('doctors.html', doctors=doctors_list)

@app.route('/doctors/<int:id>/edit', methods=['POST'])
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    doctor.name = request.form['name']
    doctor.specialization = request.form['specialization']
    doctor.contact = request.form['contact']
    db.session.commit()
    flash('Doctor updated successfully!')
    return redirect(url_for('doctors'))

@app.route('/doctors/<int:id>/delete', methods=['POST'])
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted successfully!')
    return redirect(url_for('doctors'))

# --- APPOINTMENTS ---
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    patients_list = Patient.query.all()
    doctors_list = Doctor.query.all()
    appointments_list = Appointment.query.all()

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        from datetime import datetime
        date_str = request.form['date']
        time_str = request.form['time']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        
        new_app = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date_obj, time=time_obj)
        db.session.add(new_app)
        db.session.commit()
        flash('Appointment booked successfully!')
        return redirect(url_for('appointments'))

    return render_template('appointments.html', appointments=appointments_list, patients=patients_list, doctors=doctors_list)

@app.route('/appointments/<int:id>/status', methods=['POST'])
def update_appointment_status(id):
    app_obj = Appointment.query.get_or_404(id)
    app_obj.status = request.form['status']
    db.session.commit()
    flash('Appointment status updated!')
    return redirect(url_for('appointments'))

# --- RECORDS ---
@app.route('/records', methods=['GET', 'POST'])
def records():
    patients_list = Patient.query.all()
    records_list = MedicalRecord.query.all()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        diagnosis = request.form['diagnosis']
        notes = request.form['notes']
        from datetime import date
        new_record = MedicalRecord(patient_id=patient_id, diagnosis=diagnosis, notes=notes, date=date.today())
        db.session.add(new_record)
        db.session.commit()
        flash('Medical record added successfully!')
        return redirect(url_for('records'))
    return render_template('records.html', records=records_list, patients=patients_list)

# --- BILLING ---
@app.route('/billing/<int:appointment_id>', methods=['GET', 'POST'])
def billing(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    bill = Bill.query.filter_by(appointment_id=appointment.id).first()
    
    if request.method == 'POST':
        consultation_fee = float(request.form.get('consultation_fee', 0))
        medicine_cost = float(request.form.get('medicine_cost', 0))
        test_cost = float(request.form.get('test_cost', 0))
        total = consultation_fee + medicine_cost + test_cost
        
        from datetime import date
        if bill:
            bill.consultation_fee = consultation_fee
            bill.medicine_cost = medicine_cost
            bill.test_cost = test_cost
            bill.total = total
        else:
            bill = Bill(patient_id=appointment.patient_id, appointment_id=appointment.id, 
                        consultation_fee=consultation_fee, medicine_cost=medicine_cost, 
                        test_cost=test_cost, total=total, date=date.today())
            db.session.add(bill)
        
        db.session.commit()
        flash('Bill generated/updated successfully!')
        return redirect(url_for('print_bill', bill_id=bill.id))

    return render_template('billing.html', appointment=appointment, bill=bill)

@app.route('/billing/print/<int:bill_id>')
def print_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    return render_template('print_bill.html', bill=bill)

@app.route('/bills')
def bills_list():
    bills_data = Bill.query.order_by(Bill.date.desc()).all()
    return render_template('bills_list.html', bills_data=bills_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

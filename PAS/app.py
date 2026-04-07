from flask import Flask, request, jsonify, render_template
import sqlite3
import requests

app = Flask(__name__)
DB = "appointment.db"
DOCTOR_API = "http://127.0.0.1:5000"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        doctor_id INTEGER,
        doctor_name TEXT,
        date TEXT,
        time_slot TEXT
    )
    """)
    conn.commit()
    conn.close()


init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/doctors')
def get_doctors():
    return jsonify(requests.get(f"{DOCTOR_API}/doctors/full").json())


@app.route('/doctor/<int:id>')
def get_doctor(id):
    return jsonify(requests.get(f"{DOCTOR_API}/doctor/{id}/full").json())


@app.route('/appointment', methods=['POST'])
def book_appointment():
    data = request.json

    res = requests.post(f"{DOCTOR_API}/book-slot", json={
        "doctor_id": data['doctor_id'],
        "date": data['date'],
        "time_slot": data['time_slot']
    })

    if res.status_code != 200:
        return jsonify({"error": "Slot not available"}), 400

    conn = get_conn()
    conn.execute("""
    INSERT INTO appointments (patient_name, doctor_id, doctor_name, date, time_slot)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data['patient_name'],
        data['doctor_id'],
        data['doctor_name'],
        data['date'],
        data['time_slot']
    ))
    conn.commit()
    conn.close()

    return jsonify({"message": "Appointment booked"})


@app.route('/appointments')
def get_appointments():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM appointments").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/appointment/<int:id>', methods=['DELETE'])
def cancel_appointment(id):
    conn = get_conn()
    appt = conn.execute("SELECT * FROM appointments WHERE id=?", (id,)).fetchone()

    if not appt:
        conn.close()
        return jsonify({"error": "Not found"}), 404

    requests.post(f"{DOCTOR_API}/release-slot", json={
        "doctor_id": appt['doctor_id'],
        "date": appt['date'],
        "time_slot": appt['time_slot']
    })

    conn.execute("DELETE FROM appointments WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Appointment cancelled"})


if __name__ == '__main__':
    app.run(port=5001, debug=True)

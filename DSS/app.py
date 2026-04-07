from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB = "doctor.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doctor_id INTEGER,
        date TEXT,
        time_slot TEXT,
        is_booked INTEGER DEFAULT 0,
        UNIQUE(doctor_id, date, time_slot),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/doctor', methods=['POST'])
def add_doctor():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO doctors (name) VALUES (?)", (data['name'],))
    conn.commit()

    return jsonify({"message": "Doctor added"})


@app.route('/doctors')
def get_doctors():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM doctors").fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])


@app.route('/availability', methods=['POST'])
def add_availability():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO availability (doctor_id, date, time_slot)
        VALUES (?, ?, ?)
        """, (data['doctor_id'], data['date'], data['time_slot']))
        conn.commit()
        return jsonify({"message": "Availability added"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Duplicate schedule"}), 400
    finally:
        conn.close()


@app.route('/doctors/full')
def get_doctors_full():
    conn = get_conn()
    rows = conn.execute("""
    SELECT d.id, d.name, a.date, a.time_slot, a.is_booked
    FROM doctors d
    LEFT JOIN availability a ON d.id = a.doctor_id
    ORDER BY d.id
    """).fetchall()
    conn.close()

    doctors = {}

    for r in rows:
        doc_id = r['id']
        if doc_id not in doctors:
            doctors[doc_id] = {
                "id": r['id'],
                "name": r['name'],
                "availability": []
            }

        if r['date']:
            doctors[doc_id]['availability'].append({
                "date": r['date'],
                "time_slot": r['time_slot'],
                "is_booked": bool(r['is_booked'])
            })

    return jsonify(list(doctors.values()))


@app.route('/doctor/<int:id>/full')
def get_single_doctor(id):
    conn = get_conn()
    rows = conn.execute("""
    SELECT d.id, d.name, a.date, a.time_slot, a.is_booked
    FROM doctors d
    LEFT JOIN availability a ON d.id = a.doctor_id
    WHERE d.id=?
    """, (id,)).fetchall()
    conn.close()

    if not rows:
        return jsonify({"error": "Doctor not found"}), 404

    doctor = {
        "id": rows[0]['id'],
        "name": rows[0]['name'],
        "availability": []
    }

    for r in rows:
        if r['date']:
            doctor['availability'].append({
                "date": r['date'],
                "time_slot": r['time_slot'],
                "is_booked": bool(r['is_booked'])
            })

    return jsonify(doctor)


@app.route('/book-slot', methods=['POST'])
def book_slot():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()

    slot = cursor.execute("""
    SELECT id FROM availability
    WHERE doctor_id=? AND date=? AND time_slot=? AND is_booked=0
    """, (data['doctor_id'], data['date'], data['time_slot'])).fetchone()

    if not slot:
        conn.close()
        return jsonify({"error": "Slot not available"}), 400

    cursor.execute("UPDATE availability SET is_booked=1 WHERE id=?", (slot['id'],))
    conn.commit()
    conn.close()

    return jsonify({"message": "Slot booked"})
@app.route('/doctor/<int:id>', methods=['PUT'])
def edit_doctor(id):
    data = request.json
    conn = get_conn()
    conn.execute("UPDATE doctors SET name=? WHERE id=?", (data['name'], id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Doctor updated"})


@app.route('/doctor/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    conn = get_conn()

    conn.execute("DELETE FROM availability WHERE doctor_id=?", (id,))
    conn.execute("DELETE FROM doctors WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Doctor deleted"})


@app.route('/delete-slot', methods=['POST'])
def delete_slot():
    data = request.json
    conn = get_conn()

    conn.execute("""
    DELETE FROM availability
    WHERE doctor_id=? AND date=? AND time_slot=?
    """, (data['doctor_id'], data['date'], data['time_slot']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Slot deleted"})

@app.route('/edit-schedule', methods=['PUT'])
def edit_schedule():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()

    try:
        # update doctor name
        cursor.execute(
            "UPDATE doctors SET name=? WHERE id=?",
            (data['name'], data['doctor_id'])
        )

        # update schedule
        cursor.execute("""
            UPDATE availability
            SET date=?, time_slot=?
            WHERE doctor_id=? AND date=? AND time_slot=?
        """, (
            data['new_date'],
            data['new_time'],
            data['doctor_id'],
            data['old_date'],
            data['old_time']
        ))

        conn.commit()
        return jsonify({"message": "Schedule updated successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Duplicate schedule exists"}), 400
    finally:
        conn.close()

@app.route('/release-slot', methods=['POST'])
def release_slot():
    data = request.json
    conn = get_conn()

    conn.execute("""
    UPDATE availability
    SET is_booked=0
    WHERE doctor_id=? AND date=? AND time_slot=?
    """, (data['doctor_id'], data['date'], data['time_slot']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Slot released"})


if __name__ == '__main__':
    app.run(port=5000, debug=True)

import pickle
import mysql.connector
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, send_from_directory, url_for
print("APP STARTED")

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

with open("../MODELS/complaint_classifier.pkl", "rb") as file:
    model = pickle.load(file)

with open("../MODELS/vectorizer.pkl", "rb") as file:
    vectorizer = pickle.load(file)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pratik@123",
    database="smart_city_ai"
)

cursor = db.cursor()


@app.route("/", methods=["GET", "POST"])
def home():
    complaint = ""
    prediction = ""
    priority = ""
    complaint_id = None

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        area = request.form["area"]
        complaint = request.form["complaint"]
        evidence = request.files["evidence"]
        evidence_filename = ""

        if evidence and evidence.filename != "":
           evidence_filename = secure_filename(evidence.filename)
           evidence.save(os.path.join(app.config["UPLOAD_FOLDER"], evidence_filename))
        
        complaint_vector = vectorizer.transform([complaint])
        prediction = model.predict(complaint_vector)
        prediction = prediction[0]
        
        department_map = {
           "Water Issue": "Water Supply Department",
           "Road Issue": "Road Maintenance Department",
           "Garbage": "Sanitation Department",
           "Traffic": "Traffic Management Department",
           "Street Light": "Electricity Department",
           "Drainage": "Drainage Department",
           "Electricity": "Electricity Department",
           "Public Safety": "Public Safety Department",
           "Noise Complaint": "Public Nuisance Department",
           "Illegal Parking": "Traffic Management Department"
        }

        assigned_department = department_map.get(prediction, "General Civic Department")

        officer_map = {
    "Water Supply Department": "Rahul Sharma",
    "Road Maintenance Department": "Amit Patel",
    "Sanitation Department": "Priya Singh",
    "Traffic Management Department": "Vikram Rao",
    "Electricity Department": "Neha Patil",
    "Drainage Department": "Suresh Yadav",
    "Public Safety Department": "Anjali Mehta",
    "Public Nuisance Department": "Karan Shah",
    "General Civic Department": "Admin Officer"
}

        assigned_officer = officer_map.get(assigned_department, "Admin Officer")       

        complaint_lower = complaint.lower()

        high_keywords = [
            "fire", "accident", "danger", "injury", "electric shock",
            "sewage overflow", "flood", "road blocked", "major leakage",
            "no water supply", "medical", "emergency"
        ]

        low_keywords = [
            "suggestion", "minor", "small", "request", "cleaning"
        ]

        priority = "Medium"

        for word in high_keywords:
            if word in complaint_lower:
                priority = "High"

        for word in low_keywords:
            if word in complaint_lower:
                priority = "Low"

        sql = """
    INSERT INTO complaints
(name, phone, email, area, complaint_text, category, priority_level, status, evidence_file, assigned_department,assigned_officer, admin_remark,resolution_date)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
        """

        values = (
    name,
    phone,
    email,
    area,
    complaint,
    prediction,
    priority,
    "Pending",
    evidence_filename,
    assigned_department,
    assigned_officer,
    "",
    None
)

        cursor.execute(sql, values)
        db.commit()
        complaint_id = cursor.lastrowid

        print("Complaint:", complaint)
        print("Prediction:", prediction)
        print("Priority:", priority)

    return render_template(
    "index.html",
       complaint=complaint,
       prediction=prediction,
       priority=priority,
       complaint_id=complaint_id
)

@app.route("/dashboard")
def dashboard():
    search = request.args.get("search", "")
    status_filter = request.args.get("status", "")
    category_filter = request.args.get("category", "")

    query = """
SELECT id, name, phone, email, area, complaint_text, category, priority_level, status, created_at, evidence_file,assigned_department,assigned_officer,admin_remark,resolution_date
FROM complaints
WHERE 1=1
"""

    values = []

    if search:
        query += " AND (name LIKE %s OR area LIKE %s OR complaint_text LIKE %s)"
        values.extend([f"%{search}%", f"%{search}%", f"%{search}%"])

    if status_filter:
        query += " AND status = %s"
        values.append(status_filter)

    if category_filter:
        query += " AND category = %s"
        values.append(category_filter)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, values)
    complaints = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending' OR status='pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='In Progress'")
    in_progress = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE priority_level='High'")
    high_priority = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,
        high_priority=high_priority,
        search=search,
        status_filter=status_filter,
        category_filter=category_filter
    )


@app.route("/update_status", methods=["POST"])
def update_status():
    complaint_id = request.form["complaint_id"]
    new_status = request.form["status"]

    if new_status == "Resolved":
        cursor.execute(
            "UPDATE complaints SET status = %s, resolution_date = NOW() WHERE id = %s",
            (new_status, complaint_id)
        )
    else:
        cursor.execute(
            "UPDATE complaints SET status = %s, resolution_date = NULL WHERE id = %s",
            (new_status, complaint_id)
        )

    db.commit()

    return redirect(f"/dashboard#complaint-{complaint_id}")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/analytics")
def analytics():
    cursor.execute("SELECT category, COUNT(*) FROM complaints GROUP BY category")
    category_data = cursor.fetchall()

    cursor.execute("SELECT status, COUNT(*) FROM complaints GROUP BY status")
    status_data = cursor.fetchall()

    cursor.execute("SELECT priority_level, COUNT(*) FROM complaints GROUP BY priority_level")
    priority_data = cursor.fetchall()

    cursor.execute("""
    SELECT area, COUNT(*)
    FROM complaints
    GROUP BY area
    ORDER BY COUNT(*) DESC
    LIMIT 5
    """)
    area_data = cursor.fetchall()

    cursor.execute("""
    SELECT assigned_department, COUNT(*)
    FROM complaints
    WHERE assigned_department IS NOT NULL AND assigned_department != ''
    GROUP BY assigned_department
    """)
    department_data = cursor.fetchall()

    cursor.execute("""
    SELECT assigned_officer, COUNT(*)
    FROM complaints
    WHERE assigned_officer IS NOT NULL AND assigned_officer != ''
    GROUP BY assigned_officer
    """)
    officer_data = cursor.fetchall()

    category_labels = [row[0] for row in category_data]
    category_counts = [row[1] for row in category_data]

    status_labels = [row[0] for row in status_data]
    status_counts = [row[1] for row in status_data]

    priority_labels = [row[0] for row in priority_data]
    priority_counts = [row[1] for row in priority_data]

    area_labels = [row[0] for row in area_data]
    area_counts = [row[1] for row in area_data]

    department_labels = [row[0] for row in department_data]
    department_counts = [row[1] for row in department_data]

    officer_labels = [row[0] for row in officer_data]
    officer_counts = [row[1] for row in officer_data]

    return render_template(
        "analytics.html",
        category_labels=category_labels,
        category_counts=category_counts,
        status_labels=status_labels,
        status_counts=status_counts,
        priority_labels=priority_labels,
        priority_counts=priority_counts,
        area_labels=area_labels,
        area_counts=area_counts,
        department_labels=department_labels,
        department_counts=department_counts,
        officer_labels=officer_labels,
        officer_counts=officer_counts
    )

@app.route("/complaint/<int:complaint_id>")
def complaint_detail(complaint_id):
    cursor.execute(
        "SELECT id, name, phone, email, area, complaint_text,category, priority_level, status, created_at, evidence_file FROM complaints WHERE id = %s",
        (complaint_id,)
    )

    complaint = cursor.fetchone()

    return render_template(
        "complaint_detail.html",
        complaint=complaint
    )

@app.route("/delete_complaint/<int:complaint_id>")
def delete_complaint(complaint_id):
    cursor.execute(
        "DELETE FROM complaints WHERE id = %s",
        (complaint_id,)
    )
    db.commit()

    return redirect("/dashboard")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/update_remark", methods=["POST"])
def update_remark():
    complaint_id = request.form["complaint_id"]
    admin_remark = request.form["admin_remark"]

    cursor.execute(
        "UPDATE complaints SET admin_remark = %s WHERE id = %s",
        (admin_remark, complaint_id)
    )

    db.commit()

    return redirect(f"/dashboard#complaint-{complaint_id}")

@app.route("/track", methods=["GET", "POST"])
def track():
    complaint = None
    not_found = False

    complaint_id = request.args.get("id")

    if request.method == "POST":
        complaint_id = request.form["complaint_id"]

    if complaint_id:
        cursor.execute(
           """
           SELECT id, name, area, complaint_text, category, priority_level,
        status, assigned_department, assigned_officer,
        admin_remark, created_at, resolution_date, evidence_file
        FROM complaints
        WHERE id = %s
         """,
            (complaint_id,)
        )

        complaint = cursor.fetchone()

        if complaint is None:
            not_found = True

    return render_template(
        "track.html",
        complaint=complaint,
        not_found=not_found
    )

if __name__ == "__main__":
    app.run()
    
 
from flask import Blueprint, render_template, redirect, url_for,jsonify, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import db, User, Shift
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime,time
import re  # Για έλεγχο email
from flask_migrate import Migrate

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return redirect(url_for("main.login"))

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash("Λάθος διαπιστευτήρια", "error")
            return redirect(url_for("main.login"))
        
        # Έλεγχος email format
        if not re.match(r'^[\w\.-]+@gmail\.com$', user.email):
            flash("Μόνο Gmail emails επιτρέπονται", "error")
            return redirect(url_for("main.login"))
        
        login_user(user)
        return redirect(url_for("main.dashboard"))
    
    return render_template("index.html")
from sqlalchemy.exc import IntegrityError  # Προσθήκη στο επάνω μέρος του αρχείου

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "employee")

        # Validation
        if not all([email, username, password]):
            flash("Συμπληρώστε όλα τα πεδία", "error")
            return redirect(url_for("main.register"))

        if not re.match(r'^[\w\.-]+@gmail\.com$', email):
            flash("Μόνο Gmail emails επιτρέπονται", "error")
            return redirect(url_for("main.register"))

        if User.query.filter_by(username=username).first():
            flash("Το όνομα χρήστη χρησιμοποιείται ήδη", "error")
            return redirect(url_for("main.register"))
            
        if User.query.filter_by(email=email).first():
            flash("Το email χρησιμοποιείται ήδη", "error")
            return redirect(url_for("main.register"))

        try:
            new_user = User(
                username=username,
                email=email,
                password=generate_password_hash(password),
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            flash("Εγγραφή επιτυχής! Μπορείτε τώρα να συνδεθείτε.", "success")
            return redirect(url_for("main.login"))
        except IntegrityError:
            db.session.rollback()
            flash("Σφάλμα βάσης δεδομένων", "error")

    return render_template("register.html")


@main.route('/check_username', methods=['POST'])
def check_username():
    username = request.json.get('username')
    user = User.query.filter_by(username=username).first()
    return jsonify({'exists': user is not None})

@main.route('/check_email', methods=['POST'])
def check_email():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    return jsonify({'exists': user is not None})



@main.route("/dashboard")
@login_required
def dashboard():
    shifts = Shift.query.filter_by(user_id=current_user.id).all()
    total_wage = round(sum(shift.daily_wage for shift in shifts if shift.daily_wage), 2)
    return render_template("dashboard.html", shifts=shifts, total_wage=total_wage)


@main.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():
    if current_user.role != "admin":
        return render_template("unauthorized.html"), 403

    if request.method == "POST":
        try:
            # Υπολογισμός ωρών και λεπτών
            start_time = request.form["start"]
            end_time = request.form["end"]
            
            # Μετατροπή σε datetime objects
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")
            
            # Υπολογισμός διαφοράς (χειριζόμενοι και νυχτερινές βάρδιες)
            if end_dt < start_dt:
                # Αν η ώρα λήξης είναι την επόμενη μέρα
                end_dt = datetime.strptime("23:59", "%H:%M")
                duration_part1 = (end_dt - start_dt).seconds / 3600
                duration_part2 = datetime.strptime(end_time, "%H:%M").hour
                total_hours = duration_part1 + duration_part2
            else:
                total_hours = (end_dt - start_dt).seconds / 3600
                
            total_minutes = (total_hours * 60) % 60
            hours = int(total_hours)

            # Υπολογισμός ημερομισθίου
            hourly_rate = 5.2
            wage = (hours * hourly_rate) + (total_minutes * (hourly_rate / 60))
            wage = round(wage, 2)

            # Bonus 75% για Κυριακή
            shift_date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
            if shift_date.weekday() == 6:  # Κυριακή
                wage *= 1.75
                wage = round(wage, 2)

            # Αποθήκευση στη βάση
            new_shift = Shift(
                user_id=request.form["user_id"],
                date=request.form["date"],
                start_time=request.form["start"],
                end_time=request.form["end"],
                daily_wage=wage,
                position=request.form.get("position", "waiter")
            )
            db.session.add(new_shift)
            db.session.commit()
            flash("Η βάρδια προστέθηκε επιτυχώς!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Σφάλμα: {str(e)}", "error")

    return render_template("schedule.html", users=User.query.all(), shifts=Shift.query.all())


@main.route("/shift/<int:shift_id>", methods=["POST", "DELETE"])
@login_required
def delete_shift(shift_id):
    if current_user.role != "admin":
        return render_template("unauthorized.html"), 403
        
    shift = Shift.query.get_or_404(shift_id)
    db.session.delete(shift)
    db.session.commit()
    flash("Η βάρδια διαγράφηκε επιτυχώς", "success")
    return redirect(url_for("main.schedule"))


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

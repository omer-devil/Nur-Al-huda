# =========================================================================== #
# Author: Omer Kemal                                                          #
# Social Media:                                                               #
#   - Facebook: https://web.facebook.com/omer.kemal.7                         #
#   - GitHub: https://github.com/omer-devil                                   #
# =========================================================================== #

from flask import request, render_template, Blueprint, url_for, redirect, session
from sqlalchemy.orm import sessionmaker

from utility._templates_filters import getlist
from utility.data_processor import read_from_json
from database.modle import Student, Teacher, CreatAssessment, Assessment, Sections, thought, Parent
from database.manage_db import var, engine


Admin = Blueprint(
    var.ADMIN, __name__,
    static_folder=var.STATIC_FOLDE,
    static_url_path=var.STATIC_FOLDE_PATH,
    template_folder=var.TEMPLATE_FOLDER
)
Session = sessionmaker(bind=engine)
_session = Session()

Admin.add_app_template_filter(getlist, 'getList')

# student info (done!!!!)
@Admin.route('/admin/panal', methods=['GET'])
def admin():
    if "username" in session:
        if session["role"] == "admin":
            return render_template('admin_panal.html')
        else:
            return redirect(url_for('event.unautrized'))
    else:
        return redirect(url_for('Login.login'))


# add student(done!!!)
@Admin.route('/admin/panal/add_students', methods=['GET', 'POST'])
def add_students():
    try:
        if 'username' in session:
            data, _data = read_from_json()
            gender = data.Permanent.Gender
            grades = data.Permanent.grade
            sections = data.Permanent.section
            if session['role'] == 'admin':
                if request.method == 'POST':
                    fname = request.form['fname']
                    mname = request.form['mname']
                    lname = request.form['lname']
                    Grade = request.form['grade']
                    _gender = request.form["gender"]
                    _Section = request.form['section']
                    ID = var.ID()
                    exist = _session.query(Sections).filter(
                        Sections.section == _Section.upper(),
                        Sections.grade == Grade
                    ).first()

                    reg = Student(
                        ID, fname, mname, lname, _gender,
                        ID+fname, _Section.upper(), Grade
                    )
                    print(reg)
                    try:
                        if not exist:
                            section = Sections(var.ID(), _Section.upper(), Grade)
                            _session.add(section)
                            _session.commit()
                            print('section was added')

                        _session.add(reg)
                        _session.commit()
                        print('student was added')
                        message = 'meassage'
                        return redirect(url_for('event.successful'))
                    except Exception as e:
                        _session.rollback()
                        var.log(f"Error occurred: {e}")
                        return redirect(url_for('event.internal_server_error'))
                else:
                    return render_template(
                        'add_students.html',
                        sections=sections, gender=gender,grades=grades
                    )
            else:
                return redirect(url_for('event.unautrized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


# add student()
@Admin.route('/admin/panal/add_student/<grade>/<section>', methods=['GET', 'POST'])
def add_student(grade=None, section=None):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                data, _data = read_from_json()
                gender = data.Permanent.Gender
                if request.method == 'POST':
                    if grade and section:
                        fname = request.form['fname']
                        mname = request.form['mname']
                        lname = request.form['lname']
                        _gender = request.form["gender"]
                        ID = var.ID()
                        data, _data = read_from_json()
                        gender = data.Permanent.Gender
                        reg = Student(
                            ID,  fname, mname,
                            lname, _gender,ID+fname, section.upper(), grade
                        )
                        print(reg)
                        try:
                            _session.add(reg)
                            _session.commit()
                            print('student was added')
                            _session.close()
                            return redirect(url_for('event.successful'))
                        except Exception as e:
                            var.log(f"Error occurred: {e}")
                            return redirect(url_for('event.internal_server_error'))
                    else:
                        return redirect(url_for('event.error'))
                else:
                    data, _data = read_from_json()
                    gender = data.Permanent.Gender
                    return render_template('add_student.html', gender=gender, grade=grade, section=section)
            else:
                return redirect(url_for('event.unautrized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


@Admin.route('/admin/panal/section_info')
def info():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                sections = _session.query(Sections).all()
                print(sections)
                return render_template('info_section.html', sections=sections)
            else:
                return redirect(url_for('event.unautrized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


@Admin.route('/admin/panal/get_students/<grade>/<section>')
def get_students(grade=False, section=None):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if grade and section:
                    students = _session.query(Student).filter_by(grade=grade, section=section).all()
                    return render_template(
                        'get_students.html', students=students, grade=grade, section=section
                        )
                else:
                    return 'No grade provided'
            else:
                return redirect(url_for('event.unauthorized'))
        else:
            return redirect(url_for('Login.login', message=var.NONE_LOGIN_MESSAGE))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()

# update basic info(name and gender)
@Admin.route('/admin/panal/update_student_Basic/<ID>', methods=['GET', 'POST'])
def update_student_Basic(ID):
    try:
        if 'username' in session:
            _student = _session.query(Student).filter_by(ID=ID).all()
            student = getlist(_student)
            data, _data = read_from_json()
            sections = data.Permanent.section
            grades = data.Permanent.grade
            gender = data.Permanent.Gender
            if session['role'] == 'admin':
                if request.method == 'GET':
                    return render_template('basic_update.html', student=student,gender=gender,grades=grades,sections=sections)
                elif request.method == 'POST':
                    student_fname = request.form['fname']
                    student_mname = request.form['mname']
                    student_lname = request.form['lname']
                    student_gender = request.form["gender"]

                    _session.query(Student).filter_by(ID=ID).update({
                        'fname': student_fname,
                        'mname': student_mname,
                        'lname': student_lname,
                        'gender': student_gender
                    })
                    _session.commit()
                    _session.close()
                    print(student)
                    return redirect(url_for('event.successful'))
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


# reset password
@Admin.route('/admin/panal/reset_password/<role>/<ID>')
def reset_password(role,ID):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if role == 'teacher':
                    endpoint = "info"
                    teacher = getlist(_session.query(Teacher).filter_by(ID=ID).all())
                    new_password = teacher[0][0] + teacher[0][1]
                    _session.query(Teacher).filter_by(ID=ID).update({
                        'password': new_password
                    })
                elif role == "student":
                    endpoint = "options"
                    student = getlist(_session.query(Student).filter_by(ID=ID).all())
                    new_password = student[0][0] + student[0][1]
                    _session.query(Student).filter_by(ID=ID).update({
                        'password': new_password
                    })
                elif role == 'parent':
                    parent = getlist(_session.query(Parent).filter_by(ID=ID).all())
                    new_password = parent[0][0] + parent[0][1]
                    _session.query(Parent).filter_by(ID=ID).update({
                        'password': new_password
                    })
                
                _session.commit()
                return redirect(url_for(f"admin.update_{endpoint}",ID=ID))
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error at reset occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()
# update advance(section , grade and change password)
@Admin.route('/admin/panal/update_options/<ID>')
def update_options(ID):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                _student = _session.query(Student).filter_by(ID=ID).all()
                student = getlist(_student)
            
                return render_template('update_options.html', student=student)
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


# teacher
@Admin.route('/admin/panal/add_teacher',methods=['POST', 'GET'])
def add_teacher():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if request.method == 'POST':
                    fname = request.form["fname"]
                    mname = request.form["mname"]
                    lname = request.form["lname"]
                    gender = request.form["gender"]
                    try:
                        teacher = Teacher(
                            var.ID(), fname, mname,
                            lname,gender,var.ID() + fname
                        )
                        _session.add(teacher)
                        _session.commit()
                        return redirect(url_for('event.successful'))
                    except Exception as e:
                        print(e)
                        _session.rollback()
                        return redirect(url_for('event.internal_server_error'))
                elif request.method == "GET":
                    data, _data = read_from_json()
                    gender = data.Permanent.Gender
                    return render_template(
                        'add_techer.html',gender=gender
                    )
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()

@Admin.route("/admin/panal/get_teachers")
def get_teacher():
    try:
        if "username" in session:
            if session["role"] == "admin":
                teachers = _session.query(Teacher).all()
                return render_template("get_teacher.html", teachers=teachers)
            else:
                return redirect(url_for('event.unauthorized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()


@Admin.route("/admin/panal/update/<ID>")
def update_info(ID):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                teacher = _session.query(Teacher).filter_by(ID=ID).all()
                teacher = getlist(teacher)
            
                return render_template('update_info.html', teacher=teacher)
            else:
                return redirect('event.unauthorized')
        else:
            return redirect(url_for('login.Login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))
    finally:
        _session.close()

@Admin.route('/admin/panal/add_subject_to_teacher/<ID>',methods=['POST','GET'])
def add_subject_to_teacher(ID=None):
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                if request.method == 'POST':
                    if ID:
                        subject = request.form['subject']
                        grade = request.form['grade']
                        sections = request.form.getlist('sections')
                        for section in sections:
                            try:
                                _thought = thought(
                                    var.ID(),subject,ID,grade, section, var.ACCSESS[1]
                                )
                                _session.add(_thought)
                            except Exception as e:
                                _session.rollback()
                                var.log(f"Error occurred at routte(/admin/panal/add_subject_to_teacher/): {e}")
                        _session.commit()
                        return redirect(url_for('event.successful'))
                    else:
                        return redirect(url_for('event.error'))
                else:
                    data = read_from_json()[0]
                    teacher = _session.query(Teacher).filter_by(ID=ID).all()
                    subjects = data.Permanent.subjects
                    grades = data.Permanent.grade
                    sections = data.Permanent.section
                    return render_template(
                        'add_subject_to_teacher.html', teacher=getlist(teacher),
                        sections=sections,grades=grades,subjects=subjects
                    )
            else:
                return redirect(url_for('event.unauthorized'))
        else:
            return redirect(url_for('Login.login'))
    except Exception as e:
        var.log(f"Error occurred: {e}")
        return redirect(url_for('event.internal_server_error'))


@Admin.route('/admin/panal/edit_teacher_info/<ID>',methods=['POST','GET'])
def edit_teacher_basic_info(ID=None):
    if 'username' in session:
        if session['role'] == 'admin':
            teacher = getlist(_session.query(Teacher).filter_by(ID=ID).all())
            data, _data = read_from_json()
            gender = data.Permanent.Gender
            if request.method == "GET":
                return render_template('edit_teacher_info.html', gender=gender,teacher=teacher)
            elif request.method == "POST":
                teacher_fname = request.form['fname']
                teacher_mname = request.form['mname']
                teacher_lname = request.form['lname']
                teacher_gender = request.form['gender']
                try:
                    _session.query(Teacher).filter_by(ID=ID).update({
                        'fname': teacher_fname,
                        'mname': teacher_mname,
                        'lname': teacher_lname,
                        'gender': teacher_gender
                    })
                    _session.commit()
                    return render_template('edit_teacher_info.html', gender=gender,teacher=teacher)
                except Exception as e:
                    _session.rollback()
                    print(e)
                    return 'error'

        else:
            return redirect(url_for('event.unauthorized'))
    else:
        return redirect(url_for('Login.login'))


# Delete

@Admin.route('/admin/panal/delete_student', methods=['POST'])
def delete_student():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                data = request.get_json()
                student = _session.query(Student).filter_by(ID=data['id']).first()

                if student is None:
                    return {'message': 'Student not found'}, 404  # Return error if student doesn't exist

                _session.delete(student)
                _session.commit()

                return {'message': 'Student deleted successfully'}, 200  # Return success message as JSON

            else:
                return {'message': 'Unauthorized access'}, 403  # Return unauthorized status if user is not admin
        else:
            return {'message': 'Not logged in'}, 401  # Return not authorized status if session doesn't exist

    except Exception as e:
        _session.rollback()  # Rollback if any error occurs
        var.log(f"Error occurred: {e}")
        return {'message': 'An error occurred while deleting student'}, 500  # Return general error response

    finally:
        _session.close()  # Ensure session is closed


@Admin.route('/admin/panal/delete_teacher', methods=['POST'])
def delete_teacher():
    try:
        if 'username' in session:
            if session['role'] == 'admin':
                data = request.get_json()
                student = _session.query(Teacher).filter_by(ID=data['id']).first()

                if student is None:
                    return {'message': 'Teacher not found'}, 404  # Return error if Teacher doesn't exist

                _session.delete(student)
                _session.commit()

                return {'message': 'Teacher deleted successfully'}, 200  # Return success message as JSON

            else:
                return {'message': 'Unauthorized access'}, 403  # Return unauthorized status if user is not admin
        else:
            return {'message': 'Not logged in'}, 401  # Return not authorized status if session doesn't exist

    except Exception as e:
        _session.rollback()  # Rollback if any error occurs
        var.log(f"Error occurred: {e}")
        return {'message': 'An error occurred while deleting Teacher'}, 500  # Return general error response

    finally:
        _session.close()  # Ensure session is closed


# server/main.py
# from fastapi import FastAPI, Depends, Header, HTTPException, Form
# from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import hashlib
from flask import Flask, request, session, jsonify
from flask_cors import CORS
import re
import logging
from db_init import db
app = Flask(__name__)
app.secret_key = 'your-secret-key'  # 必须设置！

# only allow port 4000 to access the backend
CORS(app, origins=["http://localhost:5137"], supports_credentials=True)

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_REGEX = r'^1[3-9]\d{9}$'

def validate_email(email):
    if not email:
        return False, "邮箱不能为空"
    if not re.match(EMAIL_REGEX, email):
        return False, "邮箱格式不正确"
    return True, ""

def validate_phone(phone_number):
    if not phone_number:
        return False, "手机号不能为空"
    if not re.match(PHONE_REGEX, phone_number):
        return False, "手机号必须是11位，且以1开头（如13800138000）"
    return True, ""

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# app.logger.setLevel(logging.INFO)

# @app.before_request
# def log_request():
#     logger.info(f"📥 {request.method} {request.path} from {request.remote_addr}")
#     logger.info(f"Headers: {dict(request.headers)}")
#     try:
#         data = request.form.to_dict()
#         logger.info(f"Body: {data}")
#     except:
#         logger.info("Body: (无法解析 form)")

# Front-back interaction functions
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Dormitory Management System API"})

# studnet register
@app.route("/api/student/register", methods=["POST"])
def student_register():
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    name = request.form.get('name')
    gender = request.form.get('gender')
    major = request.form.get('major')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    print(student_id, password, name, gender, major, email, phone_number)
    is_valid_email, email_msg = validate_email(email)
    if not is_valid_email:
        return jsonify({"success": False, "message": email_msg})

    is_valid_phone, phone_msg = validate_phone(phone_number)
    if not is_valid_phone:
        return jsonify({"success": False, "message": phone_msg})
    
    # hash the password to avoid storing plain text
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO student_info (student_id, password, name, gender, major, email, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)", (student_id, hashed_password, name, gender, major, email, phone_number))
        conn.commit()
        return jsonify({
            "success": True,
            "message": "学生注册成功！"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"注册失败：{str(e)}"
        })
    
# student log in
@app.route("/api/student/login", methods=["POST"])
def student_login():
    # print("Login request received")
    student_id = request.form.get('student_id')
    password = request.form.get('password')
    print(student_id, password)
    # hash the password to avoid direct comparsion
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name \
                    FROM student_info WHERE student_id = ? \
                    AND password = ?", (student_id, hashed_password))
        user = cursor.fetchone() # get one record
        
        if user:
            session['student_id'] = user[0]  
            session['student_logged_in'] = True
            
            return jsonify({
                "success": True,
                # "student_id": user[0],
                # "name": user[1],
                "user": {
                    "student_id": user[0],
                    "name": user[1]
                },
                "role": "student",
                "message": "学生登录成功！"
            })
        else:
            return jsonify({
                "success": False,
                "message": "学号或密码错误"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"没有用户{user[0]} Error：{str(e)}"
        })
@app.route("/api/student/info", methods=["GET"])
def get_student_info():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"}), 401
    student_id = session.get('student_id')
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT student_id, name, gender, major, dormitory_no, email, phone_number
            FROM student_info
            WHERE student_id = ?
        ''', (student_id,))
        user = cursor.fetchone()
        if user:
            return jsonify({
                "success": True,
                "data": {
                    "student_id": user[0],
                    "name": user[1],
                    "gender": user[2],
                    "major": user[3],
                    "dormitory_no": user[4],
                    "email": user[5],
                    "phone_number": user[6]
                }
            })
        else:
            return jsonify({
                "success": False,
                "message": "未找到学生信息"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取学生信息失败：{str(e)}"
        })

# student modify personal info
@app.route("/api/student/modify", methods=["POST"])
def student_modify_info():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"}), 401
    student_id = session.get('student_id')
    
    # for security, we get student_id from the session insttead of in the request
    
    name = request.form.get('name')
    gender = request.form.get('gender')
    major = request.form.get('major')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    print(student_id, name, gender, major, email, phone_number)
    # # Only update the modified part:
    # data = request.json
    # allowed_fields = ['name', 'gender', 'major', 'email', 'phone_number']
    # update_parts = []
    # update_values = []
    
    # for field in allowed_fields:
    #     # if not updated, the data of the field is None 
    #     if field in data and data[field] is not None:
    #         update_parts.append(f"{field} = ?")
    #         update_values.append(data[field])
    # if not update_parts:
    #     return jsonify({"success": False, "message": "没有提供要修改的字段"}), 400
    
    # update_parts.append("updated_at = CURRENT_TIMESTAMP")
    # update_values.append(student_id)
    fields_to_update = {
        'name': name,
        'gender': gender, 
        'major': major,
        'email': email,
        'phone_number': phone_number
    }
    update_data = {field: value for field, value in fields_to_update.items() if value is not None}
    if not update_data:
        return jsonify({"success": False, "message": "没有提供要修改的字段"}), 400
    
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    try:
        update_parts = [f"{field} = ?" for field in update_data.keys()]
        update_values = list(update_data.values())
        
        update_parts.append("updated_at = CURRENT_TIMESTAMP")
        update_values.append(student_id)
        
        sql = f"UPDATE student_info SET {', '.join(update_parts)} WHERE student_id = ?"
        cursor.execute(sql, tuple(update_values))
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": f"个人信息修改成功！更新的字段有{list(update_data.keys())}",
            "data":{
                "student_id": student_id,
                "name": name,
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"个人信息修改失败：{str(e)}"
        })

# student: see the domitory info including himself and all his roomamates
@app.route("/api/student/dormitory", methods=["GET"])
def get_student_dormitory():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    try:
        # fetch the dormitory information of the logged-in student
        cursor.execute('''
            SELECT d.building_no, d.floor_no, d.dormitory_door_no, s.name
            FROM student_info s
            JOIN dormitory_info d ON s.dormitory_no = d.dormitory_no
            WHERE s.student_id = ?
        ''', (student_id,))
        own_info = cursor.fetchone()
        # fetch all the room mate information
        cursor.execute('''
            SELECT d.building_no, d.floor_no, d.dormitory_door_no, s.name as roommate_name
            FROM student_info s
            JOIN dormitory_info d ON s.dormitory_no = d.dormitory_no
            WHERE s.dormitory_no = (SELECT dormitory_no FROM student_info WHERE student_id = ?)
            AND s.student_id != ?
        ''', (student_id, student_id))
        roommates = cursor.fetchall()
        # return own info and the roomamate info seperately
        return jsonify({
            "success": True,
            "data":{
                "own_info": {
                    "building_no": own_info[0],
                    "floor_no": own_info[1],
                    "dormitory_door_no": own_info[2],
                    "student_name": own_info[3]
                },
                "roommates": [{
                    "building_no": row[0], 
                    "floor_no": row[1], 
                    "dormitory_door_no": row[2], 
                    "roommate_name": row[3]
                } for row in roommates]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取宿舍信息失败：{str(e)}"
        })

# student request dormitory changes
@app.route("/api/student/dormitory/change_request", methods=["POST"])
def dormitory_change_request():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    
    new_dormitory_no = request.form.get('new_dormitory_no')
    reason = request.form.get('reason')
    print(student_id, new_dormitory_no, reason)
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    if not new_dormitory_no:
        return jsonify({
            "success": False,
            "message": "请选择目标宿舍"
        })
    
    if not reason:
        return jsonify({
            "success": False,
            "message": "请填写申请理由"
        })

    try:
        cursor.execute("SELECT dormitory_no FROM student_info WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            return jsonify({
                "success": False,
                "message": "学生信息不存在"
            })
            
        old_dormitory_no = result[0]
        
        # check if the new dorm exits
        cursor.execute("SELECT dormitory_no FROM dormitory_info WHERE dormitory_no = ?", (new_dormitory_no,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "目标宿舍不存在,尚未分配宿舍请等待"})
        
        # check if the new dorm is the same as the old one
        if old_dormitory_no == new_dormitory_no:
            return jsonify({"success": False, "message": "不能申请调到当前宿舍"})
        
        # check if there is an exixiting pending request
        cursor.execute("SELECT id FROM dorm_adjustment_requests WHERE student_id = ? AND status = '待审批'", (student_id,))
        if cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "您已有未处理的宿舍调整申请，请勿重复提交"
            })
        
        cursor.execute("INSERT INTO dorm_adjustment_requests (student_id, old_dormitory_no, new_dormitory_no, reason) VALUES (?, ?, ?, ?)", (student_id, old_dormitory_no, new_dormitory_no, reason.strip()))
        conn.commit()
        
        return jsonify({
            "success": True,
            "message": "宿舍调整申请提交成功！"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"申请提交失败：{str(e)}"
        })

# student: view dormitory fee overview
@app.route("/api/student/dormitory/fees", methods=["GET"])
def get_dormitory_fees():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT df.academic_year, df.semester, df.dormitory_no, df.fee_amount, df.paid_amount, df.payment_status, df.due_date, df.payment_date
            FROM dormitory_fees df 
            JOIN student_info s ON s.dormitory_no = df.dormitory_no
            WHERE s.student_id = ?
            ORDER BY df.academic_year DESC, df.semester DESC
        ''', (student_id,))
        fees = cursor.fetchall()
        return jsonify({
            "success": True,
            "data":{
                "fees": [
                    {
                        "academic_year": row[0],
                        "semester": row[1],
                        "dormitory_no": row[2],
                        "fee_amount": row[3],
                        "paid_amount": row[4],
                        "remaining_amount": float(row[3] or 0) - float(row[4] or 0),
                        "payment_status": row[5],
                        "due_date": row[6],
                        "payment_date": row[7]
                    } for row in fees
                ]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取宿舍费用信息失败：{str(e)}"
        })

# submit: dormitory maintainance request
@app.route("/api/student/maintenance/request", methods=["POST"])
def submit_maintenance_request():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    issue = request.form.get('issue')
    priority = request.form.get('priority')
    print(student_id, issue, priority)
    # check the input format
    if not issue or not issue.strip():
        return jsonify({
            "success": False,
            "message": "请填写报修问题描述"
        })
    
    if not priority or priority not in ['低', '中', '高']:
        return jsonify({
            "success": False,
            "message": "请选择正确的优先级"
        })
        
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT dormitory_no FROM student_info WHERE student_id = ?", (student_id,))
        result = cursor.fetchone()
        if not result or not result[0]:
            return jsonify({
                "success": False,
                "message": "未找到宿舍信息，你的宿舍未分配"
            })
        
        dormitory_no = result[0]
        
        cursor.execute("INSERT INTO maintenance_requests (student_id, dormitory_no, issue, priority) VALUES (?, ?, ?, ?)", (student_id, dormitory_no, issue.strip(), priority))
        conn.commit()
        return jsonify({
            "success": True,
            "message": "报修请求提交成功！"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"报修请求提交失败：{str(e)}"
        })

# student: students must be able to view all their maintenance requests
@app.route("/api/student/maintenance/all_requests", methods=["GET"])
def get_all_maintenance_requests():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, dormitory_no, issue, priority, status, created_at, resolved_at, student_id
            FROM maintenance_requests
            WHERE student_id = ?
            ORDER BY 
                CASE priority 
                    WHEN '高' THEN 1 
                    WHEN '中' THEN 2 
                    WHEN '低' THEN 3 
                END,
                created_at DESC
        ''', (student_id,))
        requests = cursor.fetchall()
        return {
            "success": True,
            "data": {
                "maintenance_requests": [
                {
                    "request_id": row[0],
                    "dormitory_no": row[1],
                    "issue": row[2],
                    "priority": row[3],
                    "status": row[4],
                    "created_at": row[5],
                    "resolved_at": row[6]
                } for row in requests]
                }
        }
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取所有报修请求失败：{str(e)}"
        }), 500
        
# student: modify maintenance request: be able to select a specific requests then modify so the request id is needed
# And only the request has not been processed can be modified
@app.route("/api/student/maintenance/modify_request", methods=["POST"])
def modify_maintenance_request():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    request_id = request.form.get('request_id')
    issue = request.form.get('issue')
    priority = request.form.get('priority')
    print(student_id, request_id, issue, priority)
    if not request_id:
        return jsonify({
            "success": False,
            "message": "请求ID不能为空"
        })
    
    if not issue or not issue.strip():
        return jsonify({
            "success": False,
            "message": "请填写报修问题描述"
        })
    
    if not priority or priority not in ['低', '中', '高']:
        return jsonify({
            "success": False,
            "message": "请选择正确的优先级"
        })
    
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        # make sure the request belongs to the current student
        # and the request has not been processed yet
        cursor.execute('''
            SELECT status FROM maintenance_requests 
            WHERE id = ? AND student_id = ?
        ''', (request_id, student_id))
        
        result = cursor.fetchone()
        if not result:
            return jsonify({
                "success": False,
                "message": "报修请求不存在或无权修改"
            })
        if result[0] != '待处理':
            return jsonify({
                "success": False,
                "message": f"当前状态为'{result[0]}'，无法修改"
            })
        
        cursor.execute("UPDATE maintenance_requests SET issue = ?, priority = ?, status = '待处理' WHERE id = ? AND student_id = ? AND status = '待处理'", (issue, priority, request_id, student_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({
                "success": False,
                "message": "修改失败，请检查请求状态"
            })
        
        return jsonify({
            "success": True,
            "message": "报修请求修改成功！"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"报修请求修改失败：{str(e)}"
        })
        
# student: view all dormitory change requests
@app.route("/api/student/dormitory/all_change_requests", methods=["GET"])
def get_all_dormitory_change_requests():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, old_dormitory_no, new_dormitory_no, reason, status, created_at, approved_at
            FROM dorm_adjustment_requests
            WHERE student_id = ?
            ORDER BY created_at DESC
        ''', (student_id,))
        requests = cursor.fetchall()
        return jsonify({
            "success": True,
            "data":{
                "dormitory_change_requests": [
                    {
                        "request_id": row[0],
                        "old_dormitory_no": row[1],
                        "new_dormitory_no": row[2],
                        "reason": row[3],
                        "status": row[4],
                        "created_at": row[5],
                        "approved_at": row[6]
                    } for row in requests
                ]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取所有宿舍调整请求失败：{str(e)}"
        })
# student: modify dormitory change
@app.route("/api/student/dormitory/modify_change_request", methods=["POST"])
def modify_dormitory_change_request():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"})
    student_id = session.get('student_id')
    request_id = request.form.get('request_id')
    new_dormitory_no = request.form.get('new_dormitory_no')
    reason = request.form.get('reason')
    print(student_id, request_id, new_dormitory_no, reason)
    if not request_id:
        return jsonify({
            "success": False,
            "message": "请求ID不能为空"
        }), 400
    
    if not new_dormitory_no:
        return jsonify({
            "success": False,
            "message": "新宿舍号不能为空"
        })
    
    if not reason or not reason.strip():
        return jsonify({
            "success": False,
            "message": "申请理由不能为空"
        })
    
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status, old_dormitory_no 
            FROM dorm_adjustment_requests 
            WHERE id = ? AND student_id = ?
        ''', (request_id, student_id))
        
        result = cursor.fetchone()
        if not result:
            return jsonify({
                "success": False,
                "message": "宿舍调整申请不存在或无权修改"
            })
        
        current_status = result[0]
        old_dormitory_no = result[1]
        if current_status != '待审批':
            return jsonify({
                "success": False,
                "message": f"当前状态为'{current_status}'，无法修改"
            })
        
        if int(old_dormitory_no) == int(new_dormitory_no):
            return jsonify({
                "success": False,
                "message": "不能申请调到当前宿舍"
            })
            
        cursor.execute("SELECT dormitory_no FROM dormitory_info WHERE dormitory_no = ?", (new_dormitory_no,))
        if not cursor.fetchone():
            return jsonify({
                "success": False,
                "message": "目标宿舍不存在"
            })
            
        cursor.execute("UPDATE dorm_adjustment_requests SET new_dormitory_no = ?, reason = ? WHERE id = ? AND student_id = ? AND status = '待审批'", (new_dormitory_no, reason, request_id, student_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({
                "success": False,
                "message": "修改失败，请检查申请状态"
            })
        
        return jsonify({
            "success": True,
            "message": "宿舍调整申请修改成功！"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"宿舍调整申请修改失败：{str(e)}"
        })
# student log out
@app.route("/api/student/logout", methods=["POST"])
def student_logout():
    if not session.get('student_logged_in'):
        return jsonify({"success": False, "message": "请先登录学生账号"}), 401
    try:
        session.pop('student_id', None)
        session.pop('student_logged_in', None)
        return jsonify({
            "success": True,
            "message": "学生注销成功！"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"退出登录失败：{str(e)}"
        })

# admin log in
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    admin_id = request.form.get('admin_id')
    password = request.form.get('password')
    print(admin_id, password)
    if not admin_id or not password:
        return jsonify({
            "success": False,
            "message": "管理员ID和密码不能为空"
        })
    
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        # 哈希密码
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("SELECT admin_id, name FROM admin_info WHERE admin_id = ? AND password = ?", (admin_id, hashed_password))
        user = cursor.fetchone()
        
        if user:
            session['admin_id'] = user[0]
            session['admin_logged_in'] = True
            return jsonify({
                "success": True,
                "admin_id": user[0],
                "name": user[1],
                "role": "administrator",
                "message": "管理员登录成功！"
            })
        else:
            return jsonify({
                "success": False,
                "message": "管理员ID或密码错误"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"登录失败：{str(e)}"
        })
    
# admin: view all students accounts
@app.route("/api/admin/students/all_accounts", methods=["GET"])
def get_all_student_accounts():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        }), 403
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT student_id, name, gender, major,  dormitory_no, email, phone_number, created_at, updated_at
            FROM student_info 
            ORDER BY created_at DESC
        ''')
        students = cursor.fetchall()
        return jsonify({
            "success": True,
            "data":{
                "students": [
                    {
                        "student_id": row[0],
                        "name": row[1],
                        "gender": row[2],
                        "major": row[3],
                        "dormitory_no": row[4],
                        "email": row[5],
                        "phone_number": row[6],
                        "created_at": row[7],
                        "updated_at": row[8]
                    } for row in students]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取所有学生账号失败：{str(e)}"
        })
# admin get own admin info
@app.route("/api/admin/admin_info", methods=["GET"])
def get_admin_info():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        })
    admin_id = session.get('admin_id')
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT admin_id, name, email, phone_number, created_at, updated_at
            FROM admin_info 
            WHERE admin_id = ?
        ''', (admin_id,))
        admin = cursor.fetchone()
        if admin:
            return jsonify({
                "success": True,
                "data":{
                    "admin_id": admin[0],
                    "name": admin[1],
                    "email": admin[2],
                    "phone_number": admin[3],
                    "created_at": admin[4],
                    "updated_at": admin[5]
                }
            })
        else:
            return jsonify({
                "success": False,
                "message": "未找到管理员信息"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取管理员信息失败：{str(e)}"
        }) 
# admin modify own personla info
@app.route("/api/admin/modify_account", methods=["POST"])
def admin_modify_own_account():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        })
    admin_id = session.get('admin_id')
    name = request.form.get('name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    print(admin_id, name, email, phone_number)
    is_valid_email, email_msg = validate_email(email)
    if not is_valid_email:
        return jsonify({"success": False, "message": email_msg})

    is_valid_phone, phone_msg = validate_phone(phone_number)
    if not is_valid_phone:
        return jsonify({"success": False, "message": phone_msg})
    
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE admin_info SET name = ?, email = ?, phone_number = ?, updated_at = CURRENT_TIMESTAMP WHERE admin_id = ?", (name, email, phone_number, admin_id))
        conn.commit() 
        return {
            "success": True,
            "message": f"管理员 {name}信息修改成功！"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"信息修改失败：{str(e)}"
        }

# admin modify student account
@app.route("/api/admin/student/modify_account", methods=["POST"])
def admin_modify_student_account():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        })
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    major = request.form.get('major')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    print(student_id, name, gender, major, email, phone_number)
    if not student_id:
        return jsonify({
            "success": False,
            "message": "学生ID不能为空"
        })
    if not all([name, gender, major, email]):
        return jsonify({
            "success": False,
            "message": "必填字段不能为空"
        })
    if gender not in ['男', '女', '其他']:
        return jsonify({
            "success": False,
            "message": "性别输入不合法"
        })
    is_valid_email, email_msg = validate_email(email)
    if not is_valid_email:
        return jsonify({"success": False, "message": email_msg})

    is_valid_phone, phone_msg = validate_phone(phone_number)
    if not is_valid_phone:
        return jsonify({"success": False, "message": phone_msg})
    
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM student_info WHERE student_id = ?", (student_id,))
        existing_student = cursor.fetchone()
        
        if not existing_student:
            return jsonify({
                "success": False,
                "message": "学生不存在"
            })
        
        cursor.execute("UPDATE student_info SET name = ?, gender = ?, major = ?, email = ?, phone_number = ? WHERE student_id = ?", (name, gender, major, email, phone_number,student_id))
        conn.commit() 
        return {
            "success": True,
            "message": f"学生 {name}信息修改成功！"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"信息修改失败：{str(e)}"
        }
# admin: view all dormitory adjustment requests
@app.route("/api/admin/all_change_requests", methods=["GET"])
def get_all_dormitory_change_requests_admin():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        })
    # student_id = request.form.get('student_id')
    # if not student_id:
    #     return jsonify({
    #         "success": False,
    #         "message": "学生ID不能为空"
    #     })
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM dorm_adjustment_requests")
        result = cursor.fetchone()
        if not result:
            return jsonify({
                "success": False,
                "message": "无宿舍调整申请"
            })
        cursor.execute('''
            SELECT id, student_id, old_dormitory_no, new_dormitory_no, reason, status, created_at, approved_at
            FROM dorm_adjustment_requests
            ORDER BY 
            CASE status 
                WHEN '待审批' THEN 1
                WHEN '已通过' THEN 2
                WHEN '已拒绝' THEN 3
            END,
            created_at DESC
        ''')
        requests = cursor.fetchall()
        cursor.execute("SELECT dormitory_no,(total_beds - occupied_beds) AS available_beds FROM dormitory_info WHERE total_beds > occupied_beds ORDER BY available_beds DESC")
        avaliable_dormitories = cursor.fetchall()
        return jsonify({
            "success": True,
            "data":{
                "dormitory_change_requests": [
                    {
                        "request_id": row[0],
                        "student_id": row[1],
                        "old_dormitory_no": row[2],
                        "new_dormitory_no": row[3],
                        "reason": row[4],
                        "status": row[5],
                        "created_at": row[6],
                        "approved_at": row[7]
                    } for row in requests
                ],
                "avaliable_dormitories": [
                    {
                        "dormitory_no": row[0],
                        "available_beds": row[1]
                    } for row in avaliable_dormitories
                ]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取所有学生宿舍调整请求失败：{str(e)}"
        })

# admin: Approve or reject student dormitory adjustment requests
@app.route("/api/admin/student/approve_change_requests", methods=["POST"])
def approve_dormitory_change_requests():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        }), 403
    student_id = request.form.get('student_id')
    request_id = request.form.get('request_id')
    action = request.form.get('action')  # 'approve' or 'reject'
    print(student_id, request_id, action)
    validation_errors = []
    
    if not student_id:
        validation_errors.append("学生ID不能为空")
    
    if not request_id:
        validation_errors.append("请求ID不能为空")
    elif not request_id.isdigit():
        validation_errors.append("请求ID必须是数字")
    
    if action not in ['approve', 'reject']:
        validation_errors.append("操作类型必须是 'approve' 或 'reject'")
    
    if validation_errors:
        return jsonify({
            "success": False,
            "message": "，".join(validation_errors)
        })
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status, new_dormitory_no 
            FROM dorm_adjustment_requests 
            WHERE id = ? AND student_id = ?
        ''', (request_id, student_id))
        
        result = cursor.fetchone()
        if not result:
            return jsonify({
                "success": False,
                "message": "宿舍调整申请不存在"
            })
        
        current_status = result[0]
        new_dormitory_no = result[1]
        if current_status != '待审批':
            return jsonify({
                "success": False,
                "message": f"当前状态为'{current_status}'，无法操作"
            })
        
        if action == 'approve':
            # chekc if the new dormitory has available beds
            cursor.execute("SELECT total_beds, occupied_beds FROM dormitory_info WHERE dormitory_no = ?", (new_dormitory_no,))
            dorm_result = cursor.fetchone()
            # the request will be rejected automatically
            if not dorm_result:
                cursor.execute("UPDATE dorm_adjustment_requests SET status = '已拒绝', approved_at = CURRENT_TIMESTAMP WHERE id = ? AND student_id = ?", (request_id, student_id))
                return jsonify({
                    "success": False,
                    "message": "目标宿舍不存在，无法批准该申请"
                })
            total_beds, occupied_beds = dorm_result
            if occupied_beds >= total_beds:
                cursor.execute("UPDATE dorm_adjustment_requests SET status = '已拒绝', approved_at = CURRENT_TIMESTAMP WHERE id = ? AND student_id = ?", (request_id, student_id))
                return jsonify({
                    "success": False,
                    "message": "目标宿舍床位已满，无法批准该申请"
                })
            try: 
                # 1. approve it to update the status in dorm_adjustment_requests
                cursor.execute("UPDATE dorm_adjustment_requests SET status = '已通过', approved_at = CURRENT_TIMESTAMP WHERE id = ? AND student_id = ?", (request_id, student_id))
                # 2. update the student_info to change the dormitory_no
                cursor.execute("UPDATE student_info SET dormitory_no = ? WHERE student_id = ?", (new_dormitory_no, student_id))
                # 3. update the dormitory_info to increase occupied_beds by 1 for the new dormitory
                cursor.execute("UPDATE dormitory_info SET occupied_beds = occupied_beds + 1 WHERE dormitory_no = ?", (new_dormitory_no,))
                # 4. update the dormitory_info to decrease occupied_beds by 1 for the old dormitory
                cursor.execute("UPDATE dormitory_info SET occupied_beds = occupied_beds - 1 WHERE dormitory_no = (SELECT old_dormitory_no FROM dorm_adjustment_requests WHERE id = ? AND student_id = ?)", (request_id, student_id))
            except Exception as e:
                conn.rollback()
                return jsonify({
                    "success": False,
                    "message": f"批准操作失败：{str(e)}"
                })
            
        else:  # reject
            cursor.execute("UPDATE dorm_adjustment_requests SET status = '已拒绝', approved_at = CURRENT_TIMESTAMP WHERE id = ? AND student_id = ?", (request_id, student_id))
        
        conn.commit()
        return jsonify({
            "success": True,
            "message": f"宿舍调整申请已{'批准' if action == 'approve' else '拒绝'}！"
        })
    
    except Exception as e:
        try:
            conn.rollback()
        except:
            pass
        return jsonify({
            "success": False,
            "message": f"操作失败：{str(e)}"
        })
# admin: view all dormitory status
@app.route("/api/admin/dormitory/all_status", methods=["GET"])
def get_all_dormitory_status():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        })
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT dormitory_no, building_no, floor_no, dormitory_door_no, total_beds, occupied_beds
            FROM dormitory_info
            ORDER BY building_no, floor_no, dormitory_door_no
        ''')
        dormitories = cursor.fetchall()
        dormitory_status_list = []
        for dormitory in dormitories:
            dormitory_no = dormitory[0]
            cursor.execute("SELECT payment_status FROM dormitory_fees WHERE dormitory_no = ? ORDER BY due_date DESC LIMIT 1", (dormitory_no,))
            latest_payment_status = cursor.fetchone()
            dormitory_status_list.append({
                "dormitory_no": dormitory[0],
                "building_no": dormitory[1],
                "floor_no": dormitory[2],
                "dormitory_door_no": dormitory[3],
                "total_beds": dormitory[4],
                "occupied_beds": dormitory[5],
                "available_beds": dormitory[4] - dormitory[5],
                "room_availability": "未满" if dormitory[4] - dormitory[5] > 0 else "已满",
                "latest_payment_status": latest_payment_status[0] if latest_payment_status else "无缴费记录"
            })
        return jsonify({
            "success": True,
            "data":{
                "dormitories": dormitory_status_list
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取所有宿舍状态失败：{str(e)}"
        })
# # admin: View dormitory status (e.g., room availability, occupancy status, payment status)
# @app.route("/api/admin/dormitory/status", methods=["GET"])
# def get_dormitory_status():
#     if not session.get('admin_logged_in'):
#         return jsonify({
#             "success": False,
#             "message": "需要管理员权限"
#         })
#     dormintory_no = request.form.get('dormitory_no')
#     if not dormintory_no:
#         return jsonify({
#             "success": False,
#             "message": "宿舍号不能为空"
#         })
#     try:
#         conn = sqlite3.connect('dormitory.db')
#         cursor = conn.cursor()
#         cursor.execute('''
#             SELECT dormitory_no, building_no, floor_no, dormitory_door_no, total_beds, occupied_beds
#             FROM dormitory_info
#             WHERE dormitory_no = ?
#         ''', (dormintory_no,))
#         dormitory = cursor.fetchone()
#         if not dormitory:
#             return jsonify({
#                 "success": False,
#                 "message": "宿舍不存在"
#             })
#         cursor.execute("SELECT payment_status FROM dormitory_fees WHERE dormitory_no = ? ORDER BY due_date DESC LIMIT 1", (dormintory_no,))
#         latest_payment_status = cursor.fetchone()
#         return jsonify({
#             "success": True,
#             "data":{
#                 "dormitory_no": dormitory[0],
#                 "building_no": dormitory[1],
#                 "floor_no": dormitory[2],
#                 "dormitory_door_no": dormitory[3],
#                 "total_beds": dormitory[4],
#                 "occupied_beds": dormitory[5],
#                 "available_beds": dormitory[4] - dormitory[5],
#                 "room_availability": "未满" if dormitory[4] - dormitory[5] > 0 else "已满",
#                 "latest_payment_status": latest_payment_status[0] if latest_payment_status else "无缴费记录"
#             }
#         })
#     except Exception as e:
#         return jsonify({
#             "success": False,
#             "message": f"获取宿舍状态失败：{str(e)}"
#         })
# admin: view all maintenance requests
@app.route("/api/admin/maintenance/all_requests", methods=["GET"])
def get_all_maintenance_requests_admin():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        })
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, student_id, dormitory_no, issue, priority, status, created_at, resolved_at
            FROM maintenance_requests
            ORDER BY 
                CASE status
                    WHEN '待处理' THEN 1
                    WHEN '处理中' THEN 2
                    WHEN '已完成' THEN 3
                END,
                CASE priority 
                    WHEN '高' THEN 1 
                    WHEN '中' THEN 2 
                    WHEN '低' THEN 3 
                END,
                created_at DESC
        ''')
        requests = cursor.fetchall()
        return jsonify({
            "success": True,
            "data":{
                "maintenance_requests": [
                    {
                        "request_id": row[0],
                        "student_id": row[1],
                        "dormitory_no": row[2],
                        "issue": row[3],
                        "priority": row[4],
                        "status": row[5],
                        "created_at": row[6],
                        "resolved_at": row[7]
                    } for row in requests
                ]
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取所有报修请求失败：{str(e)}"
        })
# admin: Process dormitory maintenance requests and update status
@app.route("/api/admin/maintenance/process_request", methods=["POST"])
def process_maintenance_request():
    if not session.get('admin_logged_in'):
        return jsonify({
            "success": False,
            "message": "需要管理员权限"
        }), 403
    request_id = request.form.get('request_id')
    action = request.form.get('action')  # '处理中'or '已完成'
    print(request_id, action)
    if not request_id:
        return jsonify({
            "success": False,
            "message": "请求ID不能为空"
        })
    
    if action not in ['处理中', '已完成']:
        return jsonify({
            "success": False,
            "message": "操作类型必须是 '处理中' or '已完成'"
        })
    
    try:
        conn = sqlite3.connect('dormitory.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT status 
            FROM maintenance_requests 
            WHERE id = ?
        ''', (request_id,))
        
        result = cursor.fetchone()
        if not result:
            return jsonify({
                "success": False,
                "message": "报修请求不存在"
            })
        
        current_status = result[0]
        if current_status == '已完成':
            return jsonify({
                "success": False,
                "message": f"当前状态为'{current_status}'，无法操作"
            })
        
        cursor.execute("UPDATE maintenance_requests SET status = ?, resolved_at = CURRENT_TIMESTAMP WHERE id = ?", (action, request_id))
        conn.commit()
        return jsonify({
            "success": True,
            "message": f"报修请求状态已更改，当前状态为{action}"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"操作失败：{str(e)}"
        })
# admin log out
@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    if not session.get('admin_logged_in'):
        return jsonify({"success": False, "message": "请先登录管理员账号"}), 401
    try:
        session.pop('admin_id', None)
        session.pop('admin_logged_in', None)
        return jsonify({
            "success": True,
            "message": "管理员注销成功！"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"退出登录失败：{str(e)}"
        })
    
if __name__ == '__main__':
    db()
    app.run(debug=True, host='0.0.0.0', port=4000)
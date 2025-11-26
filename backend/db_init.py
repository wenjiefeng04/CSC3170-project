import sqlite3
import hashlib
import os

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def db_init():
    # create a SQLite3 connection with the database
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()

    # create the initial tables if not exist: Dormitory_Information, Student_Information, 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dormitory_info (
            dormitory_no INTEGER PRIMARY KEY AUTOINCREMENT,
            building_no TEXT NOT NULL,      -- 楼号，如 "A栋"
            floor_no TEXT NOT NULL,         -- 楼层，如 "3F"
            dormitory_door_no TEXT NOT NULL,-- 宿舍门牌号，如 "301"
            total_beds INTEGER NOT NULL CHECK (total_beds > 0),     -- 总床位数
            occupied_beds INTEGER NOT NULL DEFAULT 0 CHECK (occupied_beds >= 0), -- 空床位数（可自动计算，此处为冗余缓存
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)
        '''
        )
    cursor.execute('''
        -- 2. Student_Information
        CREATE TABLE IF NOT EXISTS student_info (
            student_id TEXT PRIMARY KEY,    -- 学号（唯一标识）
            password TEXT NOT NULL,         -- 密码（建议存储哈希值）
            name TEXT NOT NULL,             -- 姓名
            gender TEXT CHECK(gender IN ('男', '女', '其他')), -- 性别
            major TEXT NOT NULL,                     -- 专业
            dormitory_no INTEGER DEFAULT NULL,           -- 所在宿舍ID（外键）default to be NULL
            email TEXT NOT NULL DEFAULT '122090112@link.cuhk.edu.cn',  -- 邮箱
            phone_number TEXT NOT NULL,      -- 联系电话
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (dormitory_no) REFERENCES dormitory_info(dormitory_no) ON DELETE SET NULL ON UPDATE CASCADE              --Allow NULL if dormitory is deleted so that student records are preserved
        )
        ''' )
    cursor.execute('''
        -- 3. admin info table
        CREATE TABLE IF NOT EXISTS admin_info (
            admin_id TEXT PRIMARY KEY,    -- 管理员ID（唯一标识）
            password TEXT NOT NULL,       -- 密码（建议存储哈希值）
            name TEXT NOT NULL,           -- 姓名
            email TEXT NOT NULL DEFAULT '122090112@link.cuhk.edu.cn',  -- 邮箱
            phone_number TEXT NOT NULL,      -- 联系电话
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    cursor.execute('''
        -- 3. Dormitory Adjustment Request
        CREATE TABLE IF NOT EXISTS dorm_adjustment_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,       -- 申请人学号
            old_dormitory_no INTEGER,       -- 原宿舍ID
            new_dormitory_no INTEGER,       -- 目标宿舍ID
            reason TEXT,                    -- 申请原因
            status TEXT CHECK(status IN ('待审批', '已通过', '已拒绝')) DEFAULT '待审批',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            approved_at DATETIME DEFAULT NULL,
            FOREIGN KEY (student_id) REFERENCES student_info(student_id) ON DELETE CASCADE,
            FOREIGN KEY (old_dormitory_no) REFERENCES dormitory_info(dormitory_no) ON DELETE SET NULL,
            FOREIGN KEY (new_dormitory_no) REFERENCES dormitory_info(dormitory_no) ON DELETE SET NULL
        )
        ''')
    
    cursor.execute('''
        -- 4. Maintenance Request
        CREATE TABLE IF NOT EXISTS maintenance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,       -- 报修人学号
            dormitory_no INTEGER NOT NULL,  -- 报修宿舍ID
            issue TEXT NOT NULL,            -- 故障描述
            priority TEXT CHECK(priority IN ('低', '中', '高')) DEFAULT '中',
            status TEXT CHECK(status IN ('待处理', '处理中', '已完成')) DEFAULT '待处理',
            assigned_to TEXT,               -- 负责人（可选）
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolved_at DATETIME DEFAULT NULL,
            FOREIGN KEY (student_id) REFERENCES student_info(student_id) ON DELETE CASCADE,
            FOREIGN KEY (dormitory_no) REFERENCES dormitory_info(dormitory_no) ON DELETE CASCADE
        )
        ''')
    cursor.execute('''
        -- dormitory fee overview table
        CREATE TABLE IF NOT EXISTS dormitory_fees (
            paymenet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dormitory_no INTEGER NOT NULL,
            academic_year TEXT NOT NULL, -- 学年，如：'2023-2024'
            semester TEXT CHECK(semester IN ('春季','夏季','秋季')), 
            fee_amount DECIMAL(10,2) NOT NULL, -- 应缴金额
            paid_amount DECIMAL(10,2) DEFAULT 0.00, -- 实缴金额
            payment_status TEXT CHECK(payment_status IN ('未缴费', '部分缴费', '已缴费')) DEFAULT '未缴费',
            payment_date DATE NOT NULL, -- 缴费日期
            due_date DATE NOT NULL, -- 缴费截止日期
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMP DEFAULT NULL ,
            FOREIGN KEY (dormitory_no) REFERENCES dormitory_info(dormitory_no) ON DELETE CASCADE
        )
        ''')
    # create indexes for faster queries
    cursor.executescript('''    
        CREATE INDEX idx_student_dormitory ON student_info(dormitory_no);
        CREATE INDEX idx_adjustment_student ON dorm_adjustment_requests(student_id);
        CREATE INDEX idx_maintenance_dormitory ON maintenance_requests(dormitory_no);
        CREATE INDEX idx_maintenance_status ON maintenance_requests(status);

        --  Enable foreign key constraints, default set to off in SQLite
        PRAGMA foreign_keys = ON;
    ''')
    conn.commit()
    
def db_insert_dormitory():
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO dormitory_info (building_no, floor_no, dormitory_door_no, total_beds, occupied_beds)
        VALUES 
        ('A栋', '1F', 'A101', 4, 0),
        ('A栋', '1F', 'A102', 4, 0),
        ('A栋', '2F', 'A201', 4, 0),
        ('B栋', '1F', 'B101', 6, 0),
        ('B栋', '1F', 'B102', 6, 0),
        ('C栋', '3F', 'C301', 4, 0),
        ('C栋', '3F', 'C302', 4, 0),
        ('D栋', '2F', 'D201', 4, 0),
        ('D栋', '2F', 'D202', 4, 0),
        ('E栋', '1F', 'E101', 6, 0);
        ''') # the primary key dormitory_no will be auto-incremented
    conn.commit()
    
def db_insert_student():
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    with open('student_info_test.txt', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:  # 跳过空行
                continue
            try:
                # 按逗号分割，注意：字段中不应包含逗号
                parts = line.split(',')
                if len(parts) != 8:
                    print(f"第 {line_num} 行格式错误（应为8个字段）：{line}")
                    continue

                # 去除前后空格
                student_id = parts[0].strip()
                password = parts[1].strip()
                name = parts[2].strip()
                gender = parts[3].strip()
                major = parts[4].strip()
                dormitory_no = int(parts[5].strip())  # 转换为整数
                email = parts[6].strip()
                phone_number = parts[7].strip()
                
                hashed_password = hash_password(password)
                # 插入数据
                cursor.execute('''
                    INSERT INTO student_info (
                        student_id, password, name, gender, major, dormitory_no, email, phone_number
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (student_id, hashed_password, name, gender, major, dormitory_no, email, phone_number))
                
                # for every insertion, must add 1 to the occupied beds of the corresponding dormitory
                cursor.execute('''UPDATE dormitory_info
                                  SET occupied_beds = occupied_beds + 1
                                    WHERE dormitory_no = ?''', (dormitory_no,))

                print(f"第 {line_num} 行插入成功: {name} ({student_id})")

            except ValueError as e:
                print(f"第 {line_num} 行数据类型错误: {e}")
            except sqlite3.IntegrityError as e:
                print(f"第 {line_num} 行插入失败（主键冲突或约束违反）: {e}")
            except Exception as e:
                print(f"第 {line_num} 行未知错误: {e}")
    conn.commit()
    conn.close()
    print("所有学生数据导入完成！")

def db_insert_admin():
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    admin_data = [
    ('A001', 'adminPass1', '张管理员', 'admin1@example.com', '13800138000'),
    ('A002', 'root1234', '李主管', 'admin2@example.com', '13900139000'),
    ('A003', 'superuser', '王主任', 'admin3@example.com', '13700137000'),
    ('A004', 'password123', '赵经理', 'admin4@example.com', '13600136000'),
    ('A005', 'secureAdmin', '钱总监', 'admin5@example.com', '13500135000') ]
    for admin in admin_data:
        admin_id, password, name, email, phone = admin
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO admin_info (admin_id, password, name, email, phone_number) VALUES (?, ?, ?, ?, ?)",
                    (admin_id, hashed_password, name, email, phone))

    conn.commit()

def db_insert_change_request():
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    
    data = [
        ('S001', 5, 3, '宿舍噪音大，影响学习', '待审批'),
        ('S001', 5, 4, '我喜欢', '已拒绝'),
        ('S002', 1, 7, '室友作息不一致，申请调换', '已通过'),
        ('S003', 10, 2, '健康原因需靠近医务室', '已拒绝'),
        ('S004', 3, 9, '希望与同专业同学同住', '待审批'),
        ('S005', 7, 1, '原宿舍漏水，维修中', '已通过')
    ]
    
    cursor.executemany('''
        INSERT INTO dorm_adjustment_requests (student_id, old_dormitory_no, new_dormitory_no, reason, status)
        VALUES (?, ?, ?, ?, ?)
    ''', data) 
    conn.commit()
    conn.close()

def db_insert_maintenance_request():
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    
    data = [
        ('S001', 5, '空调不制冷，需要维修', '高', '待处理', None),
        ('S001', 5, '断电', '高', '处理中', None),
        ('S006', 2, '宿舍201门锁损坏，无法上锁', '高', '待处理', None),
        ('S007', 9, '503宿舍热水器不出热水', '中', '处理中', '维修员赵六'),
        ('S008', 4, '阳台排水管破裂，下雨漏水', '高', '已完成', '维修员钱七'),
        ('S009', 6, '书桌抽屉滑轨脱落，无法使用', '低', '待处理', None),
        ('S010', 8, '公共区域电灯频繁闪烁，存在安全隐患', '中', '处理中', '维修员孙八')
    ]
    
    cursor.executemany('''
        INSERT INTO maintenance_requests (student_id, dormitory_no, issue, priority, status, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    conn.close()

def db_insert_dormitory_fee():
    conn = sqlite3.connect('dormitory.db')
    cursor = conn.cursor()
    
    data = [
        (1, '2023-2024', '秋季', 1200.00, 1200.00, '已缴费', '2023-09-15', '2023-09-30'),
        (2, '2023-2024', '秋季', 1200.00, 600.00, '部分缴费', '2023-09-20', '2023-09-30'),
        (3, '2023-2024', '秋季', 1200.00, 0.00, '未缴费', '2023-10-01', '2023-10-15'),
        (4, '2023-2024', '春季', 1200.00, 1200.00, '已缴费', '2023-03-10', '2023-03-25'),
        (5, '2023-2024', '春季', 1200.00, 800.00, '部分缴费', '2023-03-15', '2023-03-31'),
        (6, '2023-2024', '春季', 1200.00, 0.00, '未缴费', '2023-04-01', '2023-04-15'),
        (7, '2023-2024', '夏季', 600.00, 600.00, '已缴费', '2023-06-10', '2023-06-20'),
        (8, '2023-2024', '夏季', 600.00, 300.00, '部分缴费', '2023-06-15', '2023-06-30'),
        (9, '2023-2024', '夏季', 600.00, 0.00, '未缴费', '2023-07-01', '2023-07-15'),
        (10, '2023-2024', '秋季', 1200.00, 1200.00, '已缴费', '2023-09-10', '2023-09-25')
    ]
    
    cursor.executemany('''
        INSERT INTO dormitory_fees (dormitory_no, academic_year, semester, fee_amount, paid_amount, payment_status, payment_date, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    conn.close()
def db_clean():
    if os.path.exists('dormitory.db'):
        os.remove('dormitory.db')
        print("Existing database removed.")
    else:
        print("No existing database found.")
        
def db():
    db_clean()
    db_init()
    db_insert_dormitory()
    db_insert_student()
    db_insert_admin()
    db_insert_change_request()
    db_insert_maintenance_request()
    db_insert_dormitory_fee()
    print("Database initialized and sample data inserted.")
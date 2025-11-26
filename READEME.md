# How to run this project

1. Make sure you are under the root directory of this project
2. Dependency install: (after activate a conda enviornment)
conda create --name <env> --file requirements.txt
conda activate <env>
3. Start the backend: start the server. Clean the dirty database and initialize a clean database
(Open the terminal)
cd ./backend
python app.python
4. Start frontend: start the Web UI
(Open another terminal)
cd ./frontend
npm run dev

# To show the fontend-backend interaction

Demonstrate function: *Student account register and personal information modification*
The SQL to show the table `student_info`:

```python
import sqlite3
conn = sqlite3.connect('dormitory.db')
cursor = conn.cursor()
sql = 'SELECT student_id, name, gender, major, dormitory_no, email, phone_number FROM student_info ORDER BY created_at DESC'
cursor.execute(sql)
result = cursor.fetchall()
for record in result:
    print(record)
```

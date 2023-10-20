from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database='service_db',
                        user = 'postgres',
                        password = '5591',
                        host = 'localhost',
                        port = '5432')
cursor = conn.cursor()
cursor1 = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    message = ''
    username = request.form.get('username') 
    password = request.form.get('password')
    if request.method == 'POST':
        if request.form.get("login"):
            if username != '' and password != '':
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username),str(password)))
                records = list(cursor.fetchall())
                print(records)
                cursor1.execute("SELECT * FROM service.users")
                records1 = list(cursor1.fetchall())
                all_login = []
                all_password = []
                for i in range(len(records1)):
                    all_login.append(records1[i][2])
                    all_password.append(records1[i][3])
                    if records != []:
                        return render_template('account.html', full_name=records[0][1],username=username,password=password)
                    elif records == [] and username not in all_login:
                        message = 'There is no such person in database'
                    elif records == [] and username in all_login and password != records1[i][3]:
                        message = 'Correct username, but wrong password'
            else:
                message = 'Please, fill the gaps'
        elif request.form.get('registration'):
            return redirect('/registration/')
        message = message
    return render_template('login.html', message=message)
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        message = ''
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        cursor1.execute("SELECT * FROM service.users")
        records1 = list(cursor1.fetchall())
        all_login = []
        for i in range(len(records1)):
            all_login.append(records1[i][2])
        if name == '' or password == '' or login == '':
            message = 'Please, fill the gaps'
            return render_template('registration.html',message=message)
        elif login in all_login:
            message = 'This login has already been used, try another'
            return render_template('registration.html',message=message) 
        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',(str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
    return render_template('registration.html')



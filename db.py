import pymysql

#takes input as emp_id, password, name, age and return true if successful or false if failed
def signup(emp_id,pas,name,age):
    con=pymysql.connect('localhost','root','','test')
    sql="INSERT INTO employee(emp_id,emp_password, emp_name, emp_age) VALUES ('"+emp_id+"','"+pas+"', '"+name+"',"+ age+")"
    try:
        con.cursor().execute(sql)
        con.commit()
        return True
    except:
        con.rollback()
        return False
    finally:
        con.close()
#takes input as emp_id, password and return data if successful or false if failed
def login(emp_id,pas):
    con = pymysql.connect(host="localhost", user="root", passwd="", database="test")
    cursor = con.cursor()

    retrive = "Select * from employee where emp_id="+emp_id+" AND emp_password="+"'"+pas+"'"
    try:
        cursor.execute(retrive)
        rows = cursor.fetchall()
        return rows
    except:
        return False
    finally:
        con.close()

#takes input as emp_id and return details  if successful or false if failed
def query(emp_id):
    con = pymysql.connect(host="localhost", user="root", passwd="", database="test")
    cursor = con.cursor()

    retrive = "Select * from employee where emp_id="+emp_id
    try:
        cursor.execute(retrive)
        rows = cursor.fetchall()
        con.commit()

        return rows
    except:
        return False

    finally:
        con.close()

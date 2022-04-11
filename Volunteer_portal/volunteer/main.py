import psycopg2
from flask import Flask, render_template, g, request, redirect, url_for
from flask import Blueprint
from datetime import datetime
from . import db

bp=Blueprint("volunteer", "volunteer", url_prefix="/volunteer")

@bp.route("/reg", methods=["GET", "POST"])
def register():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    if request.method=="GET":
        return render_template("register.html")
    elif request.method=="POST":
        userid =request.form.get("u_id")
        uname=request.form.get("name")
        udob=request.form.get("dob")
        uemail=request.form.get("email")
        umobileno=request.form.get("mobileno")
        uusertype=request.form.get("usertype")
        uyearofstudy=request.form.get("yearofstudy")
        udept=request.form.get("dept")
        upassword=request.form.get("password")
        upsw_repeat=request.form.get("psw_repeat")
        if (upassword == upsw_repeat):
            cursor.execute("insert into users (u_id,name,dob,email,mobileno,usertype,yearofstudy,dept,password) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(userid,uname,udob,uemail,umobileno,uusertype,uyearofstudy,udept,upassword))
            if (uusertype == 'Student'):
                cursor.execute("insert into student(stu_id,yearofstudy) values (%s,%s)",(userid,uyearofstudy))
            if (uusertype == 'Admin'):
                cursor.execute("insert into administrator(adm_id,dept) values (%s,%s)",(userid,udept))         
    dbconn.commit()
    return redirect(url_for("volunteer.login"),302)
@bp.route("/login",methods=["GET", "POST"])
def login():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    if request.method=="POST":
        userid=request.form.get("u_id")
        p_word=request.form.get("password")
        cursor.execute("select * from users where u_id=(%s) and password=(%s)",(userid,p_word,))
        retrieved=cursor.fetchall()
        strlen=len(retrieved)
        if (strlen==1):
            cursor.execute("select usertype from users where u_id=(%s) and password=(%s)",(userid,p_word,))
            utype=cursor.fetchone()[0]
            if(utype=='Student'):
                 return render_template("studenthome.html",userid=userid)
            else:
                 return render_template("AdminHome.html",userid=userid)
        else:
            return render_template("error.html")
    elif request.method=="GET":
            return render_template("login.html")
    dbconn.commit()
@bp.route("/add", methods=["GET", "POST"])
def add_activity():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    if request.method=="GET":
        return render_template("addactivity.html")
    elif request.method=="POST":
        userid=request.form.get("userid")
        title=request.form.get("title")
        skills=request.form.get("skills")
        description=request.form.get("description")
        startdate=request.form.get("startdate")
        enddate=request.form.get("enddate")
        cursor.execute("insert into activities (adm_id,title,skills,description,startdate,enddate) values (%s,%s,%s,%s,%s,%s)",(userid,title,skills,description,startdate,enddate,))
        dbconn.commit()
        return render_template("AdminHome.html",userid=userid)
@bp.route("/view/<admid>")
def view_activities(admid):
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select * from activities order by enddate asc")
    tasks=cursor.fetchall()
    return render_template("viewlist_admin.html", tasks=tasks,admid=admid)
@bp.route("/<value>/<admid>")
def delete_activities(value,admid):
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select adm_id from activities where act_id=(%s)",(value,))
    t=cursor.fetchone()[0]
    if(t==admid):
        cursor.execute("delete from activities where act_id=(%s)",(value,))
        dbconn.commit()
        return render_template("AdminHome.html",userid=admid)
    return render_template("AdminHome.html",userid=admid)
@bp.route("/view_student/<userid>")
def view_activities_stu(userid):
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select * from activities order by enddate asc")
    tasks=cursor.fetchall()
    return render_template("viewlist_student.html", tasks=tasks,userid=userid)
@bp.route("/<actid>/<admid>/<userid>")
def apply_activity(actid,admid,userid):
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select * from activities order by enddate asc")
    tasks=cursor.fetchall()
    applicationdate=datetime.now()
    cursor.execute("insert into applications (stu_id,adm_id,act_id,applicationdate) values (%s,%s,%s,%s)",(userid,admid,actid,applicationdate,))
    dbconn.commit()
    return render_template("viewlist_student.html", tasks=tasks,userid=userid)
@bp.route("/view_aps/<userid>")
def view_applied_activities_stu(userid):
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select a.act_id,a.title,a.skills,b.status,b.applicationdate from activities a,applications b where a.act_id=b.act_id and b.stu_id=(%s)",(userid,))
    k=cursor.fetchall()
    return render_template("app_act_stu.html",tasks=k)
@bp.route("/view_app/")
def view_applications():
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select a.app_id,a.stu_id,b.title,a.status,a.applicationdate from applications a,activities b where a.act_id=b.act_id and a.adm_id=b.adm_id")
    k=cursor.fetchall()
    return render_template("app_view_admin.html",tasks=k)
@bp.route("/edit/<appid>")
def edit_app(appid):
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("update applications set status='selected' where app_id=(%s)",(appid,))
    dbconn.commit()
    cursor.execute("select a.app_id,a.stu_id,b.title,a.status,a.applicationdate from applications a,activities b where a.act_id=b.act_id")
    k=cursor.fetchall()
    return render_template("app_view_admin.html",tasks=k)
@bp.route("/selected/<userid>")
def selected_activities(userid):
    dbconn=db.get_db()
    cursor=dbconn.cursor()
    cursor.execute("select a.act_id,a.title,b.applicationdate from activities a,applications b where a.act_id=b.act_id and b.stu_id=(%s) and b.status='selected'",(userid,))
    k=cursor.fetchall()
    return render_template("selected.html",tasks=k)
@bp.route("/forgot")
def forgot():
    return render_template("forgot.html")
  
if __name__=="__main__":
    app.run()

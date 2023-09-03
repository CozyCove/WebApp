import sqlite3 
from flask import Flask, render_template, request, redirect, url_for, jsonify

app=Flask(__name__)
db = sqlite3.connect("enrollees.db",check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

SECTIONS=[
    "THEIA",
    "SELENE",
    "HELIOS",
    "GAIA",
]
STRANDS=[
    "STEM",     
    "HUMSS",
    "ABM",
    "ICT",  
]
PHRASES=[
"I'm not lazy; I'm just in an energy-saving state.",
"Chemistry: because solutions can't be found in your comfort zone.",
"Stay positive; it's a noble gas.",
"If you're not part of the solution, you're part of the precipitate.",
"Chemistry is like cooking, just don't lick the spoon.",
"Keep calm and titrate on.",
"When in doubt, add more acid.",
"Chemistry: it's like math, but with more explosions.",
"Chemistry: where alcohol gets you into trouble, and water gets you out of it.",
"Don't trust an atom; they make up everything!",
"Chemistry is the only place where you can get a reaction without even trying.",
"Keep your friends close and your reagents closer.",
"Chemistry: where solutions turn into problems.",
"The periodic table is my roadmap to success.",
"In chemistry, it's not a mistake; it's a learning experience.",
"I've got my ion you because you're positively electrifying!",
"Chemistry: because studying atoms is a blast!",
"Keep your lab coat white and your experiments bold.",
"Chemistry: making the world a better place one reaction at a time.",
"Chemists do it on the table, periodically.",
"Why do chemists like nitrates so much? Because they're cheaper than day rates!",
"Don't be a boron; be an element of surprise.",
"Chemistry: where you can mix things up and not get in trouble.",
"Keep calm and bond on.",
"If you're feeling negative, try being positive for a change.",
"Chemistry: because it's okay to have strong reactions.",
"Chemists are great at solving problems, except for their own love lives.",
"Chemistry: where every solution is just a dilution.",
"Chemistry: turning caffeine into knowledge since forever.",
"Remember, in chemistry, it's all about the mole-ment.",
"Chemists: we have all the solutions, even if they're dilute.",
"Mole Day: because it's always 6.02 x 10²³ somewhere!",
"Chemistry is like a puzzle, but with more explosions.",
"Keep your head high and your test tube higher.",
"When life gives you lemons, make a battery.",
"Chemists never die; they just stop reacting.",
"Lab safety is no accident.",
]

@app.route('/')
def endix():
    return render_template("endix.html")

@app.route("/Form")
def Form():
    return render_template("Form.html", strands=STRANDS, sections=SECTIONS)

@app.route("/History")
def history():
    return render_template('History.html')

@app.route("/Campus_Map")
def Map():
    return render_template('Campus_Map.html')

@app.route("/leaderboards", methods = ["POST"])
def Enroll():   
    username = request.form.get("name")
    score = request.form.get("score")
    time = request.form.get("total_time_spent")
    print(username,score,time)
    if not username:
       return render_template('fail.html')
    
    db.execute("INSERT INTO userscores (name, score, time) VALUES (?, ?,?)", (username, score,time))
    db.commit()         
    return redirect('/Enrollees')   
                
@app.route("/Enrollees")
def Enrollees():
    userscores=db.execute("SELECT * FROM userscores")
    return render_template('Enrollees.html', userscores=userscores)  

@app.route("/EnrolleesJSON")
def EnrolleesJSON():
    userscores = db.execute("SELECT * FROM userscores ORDER BY score DESC, time ASC").fetchall()
    userscores_list = [{"id": row["id"], "name": row["name"], "score": row["score"], "time": row["time"]} for row in userscores]
    return jsonify(userscores_list)



@app.route("/Deregister", methods =["post"])
def deregister():
    id=request.form.get("id")
    if id:
        db.execute("DELETE FROM enrollees WHERE id=?", [id] )
        db.commit()
    return redirect("/Enrollees")   

@app.route("/Chemistry")
def Chemistry():
    conn = sqlite3.connect('flashcards.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Retrieve flashcards from the database
    cursor.execute('SELECT * FROM flashcards')
    elements = cursor.fetchall()
    cursor.execute('SELECT * FROM compounds')
    compounds = cursor.fetchall()
    
    compounds_list = [dict(row) for row in compounds]
    elements_list = [dict(row) for row in elements]
    conn.close()
    return render_template('Chemistry.html', elements=elements_list, compounds = compounds_list, phrases=PHRASES )
#if __name__ == "__main__":
#Specify the host and port here
#    app.run(host="192.168.1.2", port=5100)

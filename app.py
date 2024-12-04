from flask import Flask, render_template
app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/service')
def service():
    return render_template("service.html")

@app.route('/FAQ')
def FAQ():
    return render_template("FAQ.html")

if __name__=='__main__':
    app.run(debug=True)
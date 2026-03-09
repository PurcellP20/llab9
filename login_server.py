from flask import Flask, request, render_template_string, send_from_directory
import random
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")

LOGIN_PAGE = """
<h2>Login</h2>
<form method="POST">
Username:<br>
<input type="text" name="username"><br><br>
Password:<br>
<input type="password" name="password"><br><br>
<input type="submit" value="Login">
</form>
<p>{{msg}}</p>
"""

IMAGE_PAGE = """
<h2>Login Successful</h2>
<img src="/image/{{img}}" width="600">
"""

@app.route("/image/<filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@app.route("/", methods=["GET","POST"])
def login():

    msg=""

    if request.method=="POST":

        username=request.form.get("username")
        password=request.form.get("password")

        if username=="user" and password=="bluetiger456!":

            try:

                images=[f for f in os.listdir(IMAGE_DIR)
                        if f.lower().startswith("img")]

                if not images:
                    return "No images found in images/ directory"

                img=random.choice(images)

                return render_template_string(IMAGE_PAGE,img=img)

            except Exception as e:
                return f"Server error: {e}"

        else:
            msg="Invalid credentials"

    return render_template_string(LOGIN_PAGE,msg=msg)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5550)

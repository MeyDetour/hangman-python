from app import app
from flask import render_template, request, flash, redirect
import pendu

app.secret_key = "super secret key"
# difficult => 1,2,3
penduInstance = pendu.Pendu(2)


@app.route('/', methods=['get', 'post'])
@app.route('/index', methods=['get', 'post'])
def index():
    word_to_render, letter_said, death_count, done = penduInstance.get_stats()

    done = False
    message = ""
    data = request.form.get('givenLetter')

    if request.method == 'POST' and not done:
        if not data:
            flash("Please enter letter")
        else:
            data = data.upper()
            data = data.strip()
            if  len(data) != 1 :
                #set() avoid duplicated letter
                done, message = penduInstance.run_pendu(list(set(list(data))))

            elif  not data.isalpha() or  data == "" or data in letter_said:
                flash("Entre alphabetic letter")
            else:
                done, message = penduInstance.run_pendu(data)

    word_to_render, letter_said, death_count, done = penduInstance.get_stats()

    word_to_render_with_html = ""
    for letter in word_to_render:
        if letter.islower():
            word_to_render_with_html += f"<div class='letterNotDiscover'><span>{letter.upper()}</span></div>"
        elif letter == "_":
            word_to_render_with_html += "<div class='letterUndiscover'> </div>"
        elif letter == " ":
            word_to_render_with_html += "<div class='letterSpace'> </div>"
        else:
            word_to_render_with_html += f"<div class='letterDiscover'><span>{letter}</span></div>"

    print("death here is ", death_count)
    return render_template("index.html",
                           done=done,
                           message=message,
                           word=word_to_render_with_html,
                           death_count_str=str(death_count),
                           death_count=death_count,
                           letter_said=", ".join(letter_said),
                           )


@app.route('/reset')
def reset():
    penduInstance.reset()
    return redirect("/index")

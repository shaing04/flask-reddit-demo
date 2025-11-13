from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

dog_links = [
    {
        "title": "30 Fun and Fascinating Dog Facts",
        "url": "https://www.akc.org/expert-advice/lifestyle/dog-facts/",
        "score": 10,
    },
    {
        "title": "Why Do Dogs Tilt Their Heads?",
        "url": "https://www.sciencefocus.com/nature/why-do-dogs-tilt-their-head-when-you-speak-to-them",
        "score": 5,
    },
    {
        "title": "r/dogs — top posts",
        "url": "https://www.reddit.com/r/dogs/",
        "score": 3,
    },
    {
        "title": "Basic Dog Training Guide",
        "url": "https://www.animalhumanesociety.org/resource/how-get-most-out-training-your-dog",
        "score": 2,
    },
    {
        "title": "The Dogist (photo stories)",
        "url": "https://thedogist.com/",
        "score": 1,
    },
]


@app.get("/")
def homepage():
    return render_template("index.html", links=dog_links)


@app.route("/upvote/<int:post_id>")
def upvote(post_id):
    # update upvote score
    dog_links[post_id]["score"] += 1

    # sort to be descending greated num votes to lowest
    dog_links.sort(key=lambda d: d["score"], reverse=True)

    # redirects user back to homepage after voting
    return redirect(url_for("homepage"))


@app.route("/downvote/<int:post_id>")
def downvote(post_id):
    # update downvote score
    dog_links[post_id]["score"] -= 1

    # sort posts
    dog_links.sort(key=lambda d: d["score"], reverse=True)

    return redirect(url_for("homepage"))


# create method in html = POST
# add to the route a new object
@app.route("/add", methods=["POST"])
def new_post():
    # get title and url from form
    title = request.form["title"]
    url = request.form["url"]

    # minimal validation
    if not title:
        error = "Please enter a valid title"

        return render_template("index.html", links=dog_links, error=error)

    if not url.startswith("http"):
        error = "Please enter a valid URL (must start with http)"

        return render_template("index.html", links=dog_links, error=error)

    # append the data to the dog_links data struct
    dog_links.append({"title": title, "url": url, "score": 1})

    # sort descending
    dog_links.sort(key=lambda d: d["score"], reverse=True)

    # redirect back to homepage after updating
    return redirect(url_for("homepage"))


@app.route("/hide/<int:post_id>")
def hide(post_id):
    dog_links[post_id]["hidden"] = True
    return redirect(url_for("homepage"))


@app.route("/unhide/<int:post_id>")
def unhide(post_id):
    dog_links[post_id]["hidden"] = False
    return redirect(url_for("homepage"))

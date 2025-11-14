from flask import Flask, render_template, redirect, url_for, request
import sqlite3


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


def get_db_connection():
    conn = sqlite3.connect("dog_posts.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 1,
            hidden INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()

    # Seed initial posts if table is empty
    count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    if count == 0:
        for link in dog_links:  # use your existing dog_links list
            conn.execute(
                "INSERT INTO posts (title, url, score, hidden) VALUES (?, ?, ?, ?)",
                (link["title"], link["url"], link["score"], 0),
            )
        conn.commit()
    conn.close()


init_db()

if __name__ == "__main__":
    init_db()  # ensure table exists
    app.run(debug=True)


@app.get("/")
def homepage():
    connection = get_db_connection()

    # unhidden posts (hidden = 0)
    visible_posts = connection.execute(
        "SELECT * FROM posts WHERE hidden = 0 ORDER BY score DESC"
    ).fetchall()

    # hidden posts (hidden = 1)
    hidden_posts = connection.execute(
        "SELECT * FROM posts WHERE hidden = 1 ORDER BY score DESC"
    ).fetchall()

    connection.close()

    # Pass both lists to the template
    return render_template(
        "index.html", visible_posts=visible_posts, hidden_posts=hidden_posts
    )


@app.route("/upvote/<int:post_id>")
def upvote(post_id):
    # update upvote score
    connection = get_db_connection()
    connection.execute("UPDATE posts SET score = score + 1 WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("homepage"))


@app.route("/downvote/<int:post_id>")
def downvote(post_id):
    # update downvote score
    connection = get_db_connection()
    connection.execute("UPDATE posts SET score = score - 1 WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()

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
        return render_template(
            "index.html", visible_posts=[], hidden_posts=[], error=error
        )

    if not url.startswith("http"):
        error = "Please enter a valid URL (must start with http)"
        return render_template(
            "index.html", visible_posts=[], hidden_posts=[], error=error
        )

    connection = get_db_connection()

    # creates new post with submitted title, url, starting score of 1
    connection.execute(
        "INSERT INTO posts (title, url, score, hidden) VALUES (?, ?, ?, ?)",
        (title, url, 1, 0),
    )
    connection.commit()
    connection.close()

    # redirect back to homepage after updating
    return redirect(url_for("homepage"))


@app.route("/hide/<int:post_id>")
def hide(post_id):
    connection = get_db_connection()

    # updates state of hiddent tag to 1 (true)
    connection.execute("UPDATE posts SET hidden = 1 WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("homepage"))


@app.route("/unhide/<int:post_id>")
def unhide(post_id):
    connection = get_db_connection()

    # updates state of hidden tag to 0 (false)
    connection.execute("UPDATE posts SET hidden = 0 WHERE id = ?", (post_id,))
    connection.commit()
    connection.close()

    return redirect(url_for("homepage"))

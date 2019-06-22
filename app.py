from flask import Flask
app = Flask(__name__)

@app.route("/")
def load_index():
    webPage = open("index.html", 'r')
    htmlString = webPage.read()
    webPage.close()

    return htmlString

if __name__ == "__main__":
    app.run()

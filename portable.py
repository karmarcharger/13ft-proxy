import flask
import requests
import os
from flask import request

app = flask.Flask(__name__)
#os.environ["PROXY"] = "" #for debugging when not in docker
#os.environ["HOSTNAME"] = "localhost:8084" #for debugging when not in docker
googlebot_headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
}

html = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>13ft Ladder</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans&display=swap" rel="stylesheet">

    <style>
        div.centered {
            position: absolute;
            left: 50%;
            top: 50%;
            -webkit-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
        }

        h1{
            font-family: 'Product Sans', 'Open Sans', sans-serif;
            text-rendering: optimizeLegibility;
            margin: 0;
            text-align: center;
        }
        h3{
            font-family: 'Product Sans', 'Open Sans', sans-serif;
            text-rendering: optimizeLegibility;
            margin: 0;
            text-align: center;
        }

        input[type=text] {
            padding: 10px;
            margin-bottom: 10px;
            border: 0;
            box-shadow: 0 0 15px 4px rgba(0,0,0,0.3);
            border-radius: 10px;
            width:100%;
            font-family: 'Product Sans', 'Open Sans', sans-serif;
            font-size: inherit;
            text-rendering: optimizeLegibility;
        }

        input[type="submit"] {
            /* remove default behavior */
            -webkit-appearance:none;
            appearance:none;

            /* usual styles */
            padding:10px;
            border:none;
            background-color:#6a0dad;
            color:#fff;
            font-weight:600;
            border-radius:5px;
            width:100%;
            text-transform: uppercase;
            font-family: 'Product Sans', 'Open Sans', sans-serif;
            font-size: 1rem;
            text-rendering: optimizeLegibility;
        }
        input[type="submit"]:active {
            scale: 1.02;
        }
    </style>
    
</head>
<body>
    <div class="centered">
        <form action="/link" method="get">
             <h1>
                <label for="link">Enter Website Link</label>
            </h1>
            <br>
            <input
                title="Link of the website you want to remove paywall for"
                type="text"
                name="url"
                required
            >
            <input type="submit" value="submit">

        </form>
    </div>
</body>
</html>
"""

def bypass_paywall(url):
    """
    Bypass paywall for a given URL
    """
    proxies = {}
    
    # Retrieve the proxy value from the form
    proxy = os.environ.get("PROXY")
    hostname = os.environ.get("HOSTNAME")
    
    if proxy:
        proxies["http"] = proxy
        proxies["https"] = proxy

    try:
        response = requests.get(url, proxies=proxies, headers=googlebot_headers)
        response.encoding = response.apparent_encoding
        response_text = response.text + """
        <script>
// JavaScript to intercept link clicks
document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll("a");  // Select all <a> elements on the page

    links.forEach(function(link) {
        link.addEventListener("click", function(event) {
            // Prevent the default link behavior (navigation)
            event.preventDefault();

            // Get the href attribute of the clicked link
            var href = link.getAttribute("href");

            // Check if href is a valid URL component
            if (!isValidUrlComponent(href)) {
                // Get the base URL of the current page
                var currentUrl = window.location.href;
                var url = new URL(currentUrl);
                var baseUrl = url.searchParams.get("url");

                // Construct the new URL with the additional query parameter
                var newUrl = "http://"""+hostname+"""/link?url=" + baseUrl + encodeURIComponent(href);
            } else {
                // Construct the new URL with the additional query parameter
                var newUrl = "http://"""+hostname+"""/link?url=" + encodeURIComponent(href);
            }

            // Redirect the user to the new URL
            window.location.href = newUrl;
        });
    });
});

function isValidUrlComponent(url) {
    // Use a regular expression to check if the URL component is valid
    // Modify the regular expression pattern as needed
    var pattern = /^[\w-]+:[\/]+/;
    return pattern.test(url);
}

        </script>
        """
        return response_text
    except requests.exceptions.RequestException as e:
        return str(e), 400

@app.route("/")
def main_page():
    return html
@app.route("/link", methods=["GET"])
def simulate_link_request():
    link = request.args.get("url")  # Get the URL from the request parameters
    if link:
        try:
            article_content = bypass_paywall(link)
            return article_content
        except requests.exceptions.RequestException as e:
            return str(e), 400
    else:
        return "URL parameter is missing.", 400
@app.route("/article", methods=["POST"])
def show_article():
    link = flask.request.form.get("link")
    
    try:
        article_content = bypass_paywall(link)
        return article_content
    except requests.exceptions.RequestException as e:
        return str(e), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False, port=8084)

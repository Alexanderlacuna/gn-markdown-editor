# requirements are markdown,flask and python
from flask import Flask
import markdown
app = Flask(__name__)



def authenticator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def renderer():
    return render_template("preview.html")

@app.route('/commit', methods=['POST'])
def commit():
    changes = request.form.get('changes')
    commit_message = request.form.get("message")

    try:
        repo = git.Repo(REPO_PATH)
        repo.index.add('*') #commit message
        repo.index.commit(commit_message
            )
        repo.remotes.origin.push()
        return "Changes committed and pushed successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/login')
def login():
    # github auth
    pass



def render_markdown(file_name, is_remote_file=True):
    """Try to fetch the file name from Github and if that fails, try to
look for it inside the file system """
    github_url = ("https://raw.githubusercontent.com/"
                  "genenetwork/gn-docs/master/")

    if not is_remote_file:
        text = ""
        with open(file_name, "r", encoding="utf-8") as input_file:
            text = input_file.read()
        return markdown.markdown(text,
                                 extensions=['tables'])

    md_content = requests.get(f"{github_url}{file_name}")

    if md_content.status_code == 200:
        return markdown.markdown(md_content.content.decode("utf-8"),
                                 extensions=['tables'])

    return (f"\nContent for {file_name} not available. "
            "Please check "
            "(here to see where content exists)"
            "[https://github.com/genenetwork/gn-docs]. "
            "Please reach out to the gn2 team to have a look at this")

def get_file_from_python_search_path(pathname_suffix):
    cands = [os.path.join(d, pathname_suffix) for d in sys.path]
    try:
        return list(filter(os.path.exists, cands))[0]
    except IndexError:
        return None

def get_blogs(user: str = "genenetwork",
              repo_name: str = "gn-docs") -> dict:

    blogs: Dict[int, List] = {}
    github_url = f"https://api.github.com/repos/{user}/{repo_name}/git/trees/master?recursive=1"

    repo_tree = requests.get(github_url).json()["tree"]

    for data in repo_tree:
        path_name = data["path"]
        if path_name.startswith("blog") and path_name.endswith(".md"):
            split_path = path_name.split("/")[1:]
            try:
                year, title, file_name = split_path
            except Exception as e:
                year, file_name = split_path
                title = ""

            subtitle = os.path.splitext(file_name)[0]

            blog = {
                "title": title,
                "subtitle": subtitle,
                "full_path": path_name
            }

            if year in blogs:
                blogs[int(year)].append(blog)
            else:
                blogs[int(year)] = [blog]

    return dict(sorted(blogs.items(), key=lambda x: x[0], reverse=True))

if __name__ == "__main__":
	app.run(port=5000,debug=True)
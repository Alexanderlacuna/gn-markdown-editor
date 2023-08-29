# requirements are markdown,flask and python
from flask import Flask, request, render_template,redirect,url_for
from github import Github
from github import InputGitTreeElement
app = Flask(__name__)



def authenticator(f):
    # modify for token h
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def gn_auth_access():
    # the idea for this is to try to authenticate using gn 
    #auth if success give users gn access token to  commit
    # check for gn authentication then get access token to repo
    pass 

def fetch_repo_name_from_url(url: str) -> str:
    # add this for git url
    last_slash_index = url.rfind("/")
    last_suffix_index = url.rfind(".git")
    if last_suffix_index < 0:
        last_suffix_index = len(url)

    if last_slash_index < 0 or last_suffix_index <= last_slash_index:
        raise Exception("Badly formatted url {}".format(url))

    return url[last_slash_index + 1:last_suffix_index]


@app.route("/", methods=["GET","POST"])
def edit_file_content():
    #repo_name = request.get("repo_name")
    #file_path = request.get("file_path")
    repo_name = "data-vault-2"
    file_path = "README.md"
    # handle exception for this
    g = Github(access_token)
    user = g.get_user()
    repo = user.get_repo(repo_name)
    try:
        file_content = repo.get_contents(
            file_path).decoded_content.decode('utf-8')

        return render_template("preview.html",data=file_content)
    except Exception as e:
        # add error page
        return f"Error fetching file: {str(e)}"



@app.route('/commit', methods=['POST'])
def commit():



    if request.method == 'POST':
#        repo_name = request.form.get('repo_name')
#        file_path = request.form.get('file_path')
        repo_name = "data-vault-2"
        file_path = "README2.md"
        # handle exception for this
        g = Github(access_token)
        user = g.get_user()
        repo = user.get_repo(repo_name)
        results = request.json
        master_ref = repo.get_git_ref('heads/master')
        master_sha = master_ref.object.sha
        master_tree = repo.get_git_tree(master_sha)
        # fix this below
        blob = repo.create_git_blob(results["new_changes"], 'utf-8')
        # blob.sha try content
        tree_elements = [
            InputGitTreeElement(file_path,"100644", "blob",results["new_changes"])
        ]
        new_tree = repo.create_git_tree(tree_elements, base_tree=master_tree)
        commit = repo.create_git_commit(results["msg"], new_tree, [repo.get_git_commit(master_sha)])
        master_ref.edit(commit.sha)
    
        breakpoint()
        return render_template("success.html", text="Successfully made changes")


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
    app.run(port=5000, debug=True)

# requirements are markdown,flask and python
from flask import Flask, request, render_template, redirect, url_for
from github import Github
from urllib.parse import urlparse
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
    # auth if success give users gn access token to  commit
    # check for gn authentication then get access token to repo
    pass


def parse_github_url(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split("/")

    owner = path_parts[1]
    repository_name = path_parts[2].split(".")[0]
    file_path = "/".join(path_parts[5:])
    branch = path_parts[4]

    return {
        "owner": owner,
        "repository_name": repository_name,
        "file_path": file_path,
        "branch": branch
    }


def git_diff(repo,branch,file_path,commit):
    last_head = repo.get_branch(branch)
    diff_url = repo.compare(last_head.commit.sha,
                            commit.sha)
    return diff_url.diff_url

@app.route("/", methods=["GET","POST"])
def edit_file_content():

    parsed_data = parse_github_url(edit_file)
    repo_name = parsed_data.get("repository_name")
    file_path = parsed_data.get("file_path")

    # handle exception for this
    g = Github(access_token)  # auth for token
    user = g.get_user()
    repo = user.get_repo(repo_name)
    try:
        file_content = repo.get_contents(
            file_path).decoded_content.decode('utf-8')

        return render_template("preview.html", data=file_content)
    except Exception as e:
        # add error page
        return f"Error fetching file: {str(e)}"

@app.route('/commit', methods=['POST'])
def commit():

    '''
    route to commit changes for  an existing file or new file

    '''

    if request.method == 'POST':
        parsed_data = request.json["git_url"]
        repo_name = parsed_data.get("repository_name")
        file_path = parsed_data.get("file_path")
        g = Github(access_token)
        user = g.get_user()
        repo = user.get_repo(repo_name)
        results = request.json
        master_ref = repo.get_git_ref('heads/master')
        master_sha = master_ref.object.sha
        master_tree = repo.get_git_tree(master_sha)
        # fix this below
        blob = repo.create_git_blob(results["new_changes"], 'utf-8')
        tree_elements = [
            InputGitTreeElement(file_path, "100644", "blob",
                                results["new_changes"])
        ]
        new_tree = repo.create_git_tree(tree_elements, base_tree=master_tree)
        commit = repo.create_git_commit(results["msg"], new_tree, [
                                        repo.get_git_commit(master_sha)])
        master_ref.edit(commit.sha)
        return render_template("success.html", text="Successfully made changes")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

# requirements are markdown,flask and python
import markdown
from flask import Flask, request, render_template, redirect, url_for, jsonify
from github import Github
from urllib.parse import urlparse
from github import InputGitTreeElement
from app import app

from functools import wraps
from github import Github, GithubException


def authenticator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        github_token = get_github_access_token()
        if not github_token:
            return "Unauthorized: GitHub token not provided", 401
        try:
            g = Github(github_token)
            user = g.get_user()
            if user:
                return f(g, *args, **kwargs)
        except GithubException as e:
            return f"GitHub authentication failed: {str(e)}", 401
        return "Unauthorized: GitHub authentication failed", 401
    return decorated_function


def get_github_access_token():
    # override this method to get the token from  elsewhere
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


def git_diff(repo, branch, file_path, commit):
    last_head = repo.get_branch(branch)
    diff_url = repo.compare(last_head.commit.sha,
                            commit.sha)
    return diff_url.diff_url


@app.route("/", methods=["GET", "POST"])
def edit_file_content():
    edit_file = request.args.get("refresh_link")
    if not edit_file:
        edit_file = "https://github.com/Alexanderlacuna/data-vault-2/blob/master/README.md"

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

        return render_template("preview.html", data=file_content, refresh_link=edit_file)
    except Exception as e:
        # add error page
        return f"Error fetching file: {str(e)}"


@app.route('/commit', methods=['POST'])
def commit():
    '''
    route to commit changes for  an existing file or new file
    '''
    request.json["git_url"] = "https://github.com/Alexanderlacuna/data-vault-2/blob/master/README.md"
    if request.method == 'POST':
        parsed_data = parse_github_url(request.json["git_url"])
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
        return jsonify({"commit": commit.sha, "commit_message": results["msg"]})


@app.route('/parser', methods=['POST'])
def marked_down_parser():
    ''' this route uses python-markdown to parse markdown to html
     ::expensive  to call for live preview
    '''
    try:

        results = markdown.markdown(
            request.json["text"], extensions=["tables"])
        return jsonify({"data": results})
    except Exception as e:
        raise e
        return f"error while parsing markdown  {str(e)}"

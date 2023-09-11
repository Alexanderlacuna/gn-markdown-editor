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
            if g.get_user().name:
                return f(g, *args, **kwargs)
        except GithubException as e:
            return f"GitHub authentication failed: {str(e)}", 401
        return "Unauthorized: GitHub authentication failed", 401
    return decorated_function


def get_github_access_token():
    # override this method to get the token from  elsewhere
    return app.config["GITHUB_ACCESS_TOKEN"]


def parse_github_url(url):
    """require format for this 
    https://github.com/{username}/{repo_name}/blob/{branch}/README.md
    """
    path_parts = urlparse(url).path.split("/")
    return {
        "owner": path_parts[1],
        "repository_name": path_parts[2].split(".")[0],
        "file_path": "/".join(path_parts[5:]),
        "branch":  path_parts[4]
    }


def git_diff(repo, branch, file_path, commit):
    """function to equivalent to git diff
    """
    diff_url = repo.compare(repo.get_branch(branch).commit.sha,
                            commit.sha)
    return diff_url.diff_url


@app.route("/", methods=["GET", "POST"])
@authenticator
def edit_file_content(g):
    edit_file = request.args.get("refresh_link")
    if not edit_file:
        edit_file = "https://github.com/Alexanderlacuna/data-vault-2/blob/master/README.md"
    parsed_data = parse_github_url(edit_file)
    repo = g.get_user().get_repo(parsed_data.get("repository_name"))
    try:
        file_content = repo.get_contents(
            parsed_data.get("file_path")).decoded_content.decode('utf-8')
        return render_template("preview.html", data=file_content, refresh_link=edit_file)
    except Exception as e:
        return f"Error fetching file: {str(e)}"


@app.route('/commit', methods=['POST'])
@authenticator
def commit(g):
    '''
    route to commit changes for  an existing file or new file
    '''
    request.json["git_url"] = "https://github.com/Alexanderlacuna/data-vault-2/blob/master/README.md"
    if request.method == 'POST':
        parsed_data = parse_github_url(request.json["git_url"])
        repo = g.get_user().get_repo(parsed_data.get("repository_name"))
        results = request.json
        master_ref = repo.get_git_ref('heads/master')
        master_sha = master_ref.object.sha
        master_tree = repo.get_git_tree(master_sha)
        # fix this below
        try:

            blob = repo.create_git_blob(results["new_changes"], 'utf-8')
            tree_elements = [
                InputGitTreeElement(parsed_data.get("file_path"), "100644", "blob",
                                    results["new_changes"])
            ]
            new_tree = repo.create_git_tree(
                tree_elements, base_tree=master_tree)
            commit = repo.create_git_commit(results["msg"], new_tree, [
                                            repo.get_git_commit(master_sha)])
            master_ref.edit(commit.sha)
            return jsonify({"commit": commit.sha, "commit_message": results["msg"]})
        except Exception as error:
            return jsonify({"error": str(error)})


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
        return f"error while parsing markdown  {str(e)}"

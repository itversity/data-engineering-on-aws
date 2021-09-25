import requests, json
from multiprocessing import Process, Manager
from process import extract_repo_fields


def list_repos(token, since):
    res = requests.get(
        f'https://api.github.com/repositories?since={since}',
        headers={'Authorization': f'token {token}'}
    )
    return json.loads(res.content.decode('utf-8'))


def get_repo_details(owner, name, token):
    repo_details = json.loads(requests.get(
        f'https://api.github.com/repos/{owner}/{name}',
        headers={'Authorization': f'token {token}'}
    ).content.decode('utf-8'))
    return repo_details


def get_repo_details_parallel(repos_details, owner, name, token):
    repo_details = json.loads(requests.get(
        f'https://api.github.com/repos/{owner}/{name}',
        headers={'Authorization': f'token {token}'}
    ).content.decode('utf-8'))
    repos_details.append(repo_details)


def get_repos(token, repos):
    repos_details = []
    for repo in repos:
        try:
            owner = repo['owner']['login']
            name = repo['name']
            repo_details = get_repo_details(owner, name, token)
            repo_fields = extract_repo_fields(repo_details)
            repos_details.append(repo_fields)
        except Exception as e:
            print(f'Failed extracting information for {repo["id"]}')
            pass
    return repos_details


def get_repos_parallel(token, repos):
    with Manager() as manager:
        repos_details = manager.list()
        repo_get_processes = []
        for repo in repos:
            owner = repo['owner']['login']
            name = repo['name']
            process = Process(target=get_repo_details_parallel, args=(repos_details, owner, name, token))
            process.start()
            repo_get_processes.append(process)
        for p in repo_get_processes:
            p.join()

        repo_field_details = []
        for repo_details in repos_details:
            try:
                repo_fields = extract_repo_fields(repo_details)
                repo_field_details.append(repo_fields)
            except:
                raise
    return repo_field_details


def list_and_get_repo_details(token, since):
    repos = list_repos(token, since)
    repos_details = get_repos(token, repos)
    # repos_details = get_repos_parallel(token, repos)
    return repos_details


def get_rate_remaining(token):
    res = requests.get(
        f'https://api.github.com/rate_limit',
        headers={'Authorization': f'token {token}'}
    )
    rate_details = json.loads(res.content.decode('utf-8'))
    return rate_details['rate']['remaining']
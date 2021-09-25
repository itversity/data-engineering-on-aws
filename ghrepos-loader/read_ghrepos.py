import requests, json
from multiprocessing import Manager, Process
from process import extract_repo_fields


def list_repos(token, since):
    res = requests.get(
        f'https://api.github.com/repositories?since={since}',
        headers={'Authorization': f'token {token}'}
    )
    return json.loads(res.content.decode('utf-8'))


def get_repo_details(repo):
    owner = repo[0]['owner']['login']
    name = repo[0]['name']
    token = repo[1]
    repo_details = json.loads(requests.get(
        f'https://api.github.com/repos/{owner}/{name}',
        headers={'Authorization': f'token {token}'}
    ).content.decode('utf-8'))
    return {'id': repo[0]['id'], 'contents': repo_details}


def get_repos_details(repos_details, repos, thread, no_of_threads=8):
    try:
        repos_filtered = filter(lambda repo: int(repo[0]['id']) % no_of_threads == thread, repos)
        repos_details += list(map(get_repo_details, repos_filtered))
    except:
        pass


def get_repos(token, repos):
    repos_with_token = list(map(lambda repo: (repo, token), repos))
    no_of_threads = 4
    repos_extracted_fields = []
    with Manager() as manager:
        repos_details = manager.list()
        processes = []
        for i in range(no_of_threads):
            p = Process(target=get_repos_details, args=(repos_details, repos_with_token, i, no_of_threads))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        for repo_details in repos_details:
            try:
                repo_fields = extract_repo_fields(repo_details['contents'])
                repos_extracted_fields.append(repo_fields)
            except Exception as e:
                print(f'Failed processing repo with id {repo_details["id"]}')
                pass
    return repos_extracted_fields


def list_and_get_repo_details(token, since):
    repos = list_repos(token, since)
    repos_details = get_repos(token, repos)
    return repos_details


def get_rate_remaining(token):
    res = requests.get(
        f'https://api.github.com/rate_limit',
        headers={'Authorization': f'token {token}'}
    )
    rate_details = json.loads(res.content.decode('utf-8'))
    return rate_details['rate']['remaining']

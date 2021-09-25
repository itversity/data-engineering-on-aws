import os
from read_ghrepos import list_and_get_repo_details, get_rate_remaining
from load_db import load_repos_into_table
from marker import get_marker_table, \
    get_marker, update_marker


def main(context, event):
    token = os.environ.get('GITHUB_TOKEN')
    if os.environ.get('ENVIRON') == 'DEV':
        os.environ.setdefault('AWS_PROFILE', 'itvgithub')
        os.environ.setdefault('AWS_DEFAULT_REGION', 'us-east-1')
    since = extract_and_load_repos(token)
    return {'last_repo_id': since}


def extract_and_load_repos(token):
    marker_table = get_marker_table()
    marker_item = get_marker(marker_table, 'ghrepos')
    since = marker_item['marker']
    if get_rate_remaining(token) <= 100:
        print(f'GitHub API Rate limit is less than 100 and hence not triggering any API Calls')
        return since
    while True:
        try:
            print(f'Processing repos since {since}')
            repos_details = list_and_get_repo_details(token, since)
            last_repo_id = load_repos_into_table(repos_details, 50)
            since = update_marker(marker_table, 'ghrepos', last_repo_id, 'SUCCESS')
            if get_rate_remaining(token) <= 100:
                print(f'GitHub API Rate limit is less than 100')
                break
        except Exception as e:
            print(e)
            break
    return since


if __name__ == '__main__':
    main()

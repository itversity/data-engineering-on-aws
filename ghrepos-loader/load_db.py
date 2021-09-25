import boto3


def load_repos(repos_details, table, batch_size=50):
    with table.batch_writer() as batch:
        repos_count = len(repos_details)
        for i in range(0, repos_count, batch_size):
            for repo in repos_details[i:i+batch_size]:
                batch.put_item(Item=repo)
    last_repo_id = repos_details[-1]['id']
    return last_repo_id


def load_repos_into_table(repos_details, batch_size=50):
    dynamodb = boto3.resource('dynamodb')
    ghrepos = dynamodb.Table('ghrepos')
    last_repo_id = load_repos(repos_details, ghrepos, batch_size)
    return last_repo_id

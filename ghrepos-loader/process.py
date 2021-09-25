def extract_repo_fields(repo_details):
    repo_fields = {
        'id': repo_details['id'],
        'node_id': repo_details['node_id'],
        'name': repo_details['name'],
        'full_name': repo_details['full_name'],
        'owner': {
            'login': repo_details['owner']['login'],
            'id': repo_details['owner']['id'],
            'node_id': repo_details['owner']['node_id'],
            'type': repo_details['owner']['type'],
            'site_admin': repo_details['owner']['site_admin']
        },
        'html_url': repo_details['html_url'],
        'description': repo_details['description'],
        'fork': repo_details['fork'],
        'created_at': repo_details['created_at']
    }
    return repo_fields
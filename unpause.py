from actionkit.api.user import AKUserAPI
from pywell.entry_points import run_from_cli, run_from_lamba
from pywell.get_psql_results import get_psql_results


DESCRIPTION = 'Unpause AK users based on DB query.'

ARG_DEFINITIONS = {
    'AK_BASEURL': 'ActionKit Base URL.',
    'AK_USER': 'ActionKit API username.',
    'AK_PASSWORD': 'ActionKit API password.',
    'AK_IMPORT_PAGE': 'ActionKit import page name.',
    'DB_HOST': 'Database host IP or hostname.',
    'DB_PORT': 'Database port number.',
    'DB_USER': 'Database user.',
    'DB_PASS': 'Database password.',
    'DB_NAME': 'Database name.',
    'DB_QUERY': 'Query to get user IDs.'
}

REQUIRED_ARGS = [
    'AK_BASEURL', 'AK_USER', 'AK_PASSWORD', 'AK_IMPORT_PAGE', 'DB_HOST',
    'DB_PORT', 'DB_USER', 'DB_PASS', 'DB_NAME', 'DB_QUERY'
]


def unpause(args):
    user_ids = [row.get('user_id') for row in get_psql_results(args)]
    api = AKUserAPI(args)
    api.bulk_upload_rows(
        args.AK_IMPORT_PAGE, ['user_id'], [[user_id] for user_id in user_ids]
    )
    return user_ids


def aws_lambda(event, context):
    return run_from_lamba(unpause, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS, event)


if __name__ == '__main__':
    run_from_cli(unpause, DESCRIPTION, ARG_DEFINITIONS, REQUIRED_ARGS)

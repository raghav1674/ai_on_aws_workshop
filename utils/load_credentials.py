

def load_aws_credentials(credential_file_path=None):

    try:
        from csv import reader
        from os import path

        # check if path exists or not
        if credential_file_path is None:
            raise Exception(
                'credential_file_path parameter value not provided')

        if path.exists(credential_file_path):

            with open(credential_file_path) as fp:

                reader = csv.reader(fp)

                credentials = [row for row in reader][1:][0]

                ACCESS_KEY, SECRET_KEY = credentials[2:4]

            return {'success': 1, 'access_key': ACCESS_KEY, 'secret_key': SECRET_KEY}

    except Exception as e:
        return {'success': 0, 'error': e}

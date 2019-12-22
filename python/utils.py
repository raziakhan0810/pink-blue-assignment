from django.conf import settings


def get_version(debug=True):
    if debug:
        return ""
    with open('.version', 'r') as myfile:
        data = myfile.read().replace('\n', '')
        return "-" + data

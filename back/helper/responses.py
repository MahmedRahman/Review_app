import json
from datetime import date, datetime
from urllib.parse import urlparse, parse_qs

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime and date objects."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

def create_response(data=None, success=True, code=200, errors=None):
    response = {
        "success": success,
        "code": code
    }
    if data is not None:
        response["data"] = data
    if errors is not None:
        response["errors"] = errors

    return json.dumps(response, cls=DateTimeEncoder)


def extract_app_id(app_url):
    # Parse the URL into components
    url_components = urlparse(app_url)

    # Extract the query string
    query_string = url_components.query

    # Parse the query string into a dictionary
    query_params = parse_qs(query_string)

    # Check if 'id' is in the query parameters
    if 'id' in query_params:
        # Extract the app_id
        app_id = query_params['id'][0]
        return app_id
    else:
        return 'Invalid URL'

 
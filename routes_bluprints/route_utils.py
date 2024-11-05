import flask

def handle_route_error():
    '''
    Function that handles exceptions. Renders the error page. Logs the error. etc.
    '''
    return flask.render_template('error_page.html')

def handle_route_invalid_request():
    """
    Function that returns the template for invalid requests.
    """
    return flask.render_template('invalid_request.html'), 400
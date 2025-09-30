"""
Helper functions for session management in tests
"""


def setup_authenticated_session(client, access_token='test_token'):
    """Set up an authenticated session for testing"""
    with client.session_transaction() as sess:
        sess['access_token'] = access_token
    return client


def setup_demo_session(client):
    """Set up a demo mode session for testing"""
    with client.session_transaction() as sess:
        sess['demo_mode'] = True
        sess['access_token'] = 'demo_token'
    return client


def clear_session(client):
    """Clear all session data"""
    with client.session_transaction() as sess:
        sess.clear()
    return client


def get_session_data(client):
    """Get current session data"""
    with client.session_transaction() as sess:
        return dict(sess)


def set_session_data(client, data):
    """Set session data from dictionary"""
    with client.session_transaction() as sess:
        sess.update(data)
    return client

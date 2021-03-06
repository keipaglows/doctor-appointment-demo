from requests import Session


class SessionMiddleware:

    session: Session = Session()

    def __getattr__(self, name):
        return getattr(self.session, name)

    def process_resource(self, req, resp, resource, params):
        req.context.session = self

    def set_headers(self, access_token: str, _refresh_token: str):
        self.session.headers['Authorization'] = f'Bearer {access_token}' 

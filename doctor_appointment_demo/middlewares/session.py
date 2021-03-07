import falcon
from requests import Session


class SessionMiddleware:

    session: Session = Session()

    def __getattr__(self, name: str):
        return getattr(self.session, name)

    def process_request(self, req: falcon.Request, _resp: falcon.Response):
        req.context.session = self

    def set_headers(self, access_token: str, _refresh_token: str):
        self.session.headers['Authorization'] = f'Bearer {access_token}'

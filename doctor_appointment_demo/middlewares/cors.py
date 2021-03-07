import falcon
from falcon.http_status import HTTPStatus


class CORSMiddleware:

    def process_request(self, req: falcon.Request, resp: falcon.Response):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')

        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200)

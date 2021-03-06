from falcon import HTTPUnprocessableEntity, Request
from marshmallow import ValidationError, Schema


def get_and_validate_schema(schema: Schema, request: Request, many=None):
    data = request.params or request.media

    try:
        return schema().load(data, many=many)
    except ValidationError as e:
        raise HTTPUnprocessableEntity(e.messages) from e

from marshmallow import Schema, fields


class NamedEntitySchema(Schema):
    text = fields.Str(description='Named entity text', required=True)
    type = fields.Str(description='Named entity type', required=True)


class PostIndexSchema(Schema):
    title = fields.Str(description='New title', required=True)
    url = fields.Str(description='New url', required=True)
    source = fields.Str(description='New source name', required=True)
    sentiment = fields.Float(description='New sentiment', required=False)
    date = fields.Float(description='New publish date', required=True)
    hydrated = fields.Boolean(description='New hydration flag', required=False)
    content = fields.Str(description='New content', required=True)
    summary = fields.Str(description='New content summary', required=False)
    entities = fields.List(fields.Nested(NamedEntitySchema), description="New named entities", required=False)

from flask import Blueprint


{{ blueprint }} = Blueprint(__name__, '{{ blueprint }}')


@{{ blueprint }}.route('/')
def index():
  return 'Hello, world'

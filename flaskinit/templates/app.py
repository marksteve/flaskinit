from flask import Flask

from .extensions import *
from .views import *


def register_blueprints(app):
{%- for blueprint in blueprints -%}
{%- if blueprint == root %}
  app.register_blueprint({{ blueprint }})
{%- else %}
  app.register_blueprint({{ blueprint }}, url_prefix='/{{ blueprint }}')
{%- endif %}
{%- endfor %}


{% if inits|length -%}
def init_extensions(app):
{%- for init in inits %}
{{ init|indent(2, True) }}
{%- endfor %}


{% endif -%}
def create_app():
  app = Flask(__name__)
  app.config.from_object('{{ project }}.config')
  register_blueprints(app)
{%- if inits|length %}
  init_extensions(app)
{%- endif %}
  return app

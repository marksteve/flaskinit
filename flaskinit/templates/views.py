{% for blueprint in blueprints -%}
from .{{ blueprint }} import {{ blueprint }}
{% endfor %}

__all__ = {{ blueprints }}

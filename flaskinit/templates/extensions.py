{% if imports|length -%}
{% for imp in imports -%}
{{ imp }}
{% endfor %}

__all__ = {{ assigns.keys() }}


{{ '\n'.join(assigns.values()) }}
{%- endif %}

{% set name = 'Flask-SQLAlchemy' %}
{% set var_name = 'db' %}

{% macro imp() %}from flask_sqlalchemy import SQLAlchemy{% endmacro %}

{% macro assign() %}{{ var_name }} = SQLAlchemy(){% endmacro %}

{% macro config() -%}
SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/database'
{%- endmacro %}

{% macro init() -%}
db.init_app(app)
{%- endmacro %}

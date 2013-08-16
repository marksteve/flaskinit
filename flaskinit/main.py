from functools import partial
import argparse
import base64
import os
import stat

from jinja2 import Environment, PackageLoader
from jinja2.exceptions import TemplateNotFound

# Silence python_fu by monkey-patching
from python_fu import commandline
# Re-assign for our use
info, error = commandline.info, commandline.error
commandline.info = lambda msg: None
commandline.error = lambda msg: None

from python_fu.module import Module

from .metadata import __version__, __description__


__all__ = ['main']


def parse_args():
  parser = argparse.ArgumentParser(
    prog=__package__,
    description=__description__)
  parser.add_argument('project', action='store',
                      help="project name")
  parser.add_argument('-b', '--blueprint', action='append', dest='blueprints',
                      help="add a blueprint", default=[])
  parser.add_argument('-e', '--extension', action='append', dest='extensions',
                      help="include an extension", default=[])

  parser.add_argument('--root', action='store', dest='root',
                      help="set root blueprint", default='root')
  parser.add_argument('--session', action='store_true', dest='session',
                      help="enable session")

  parser.add_argument('-v', '--version', action='version',
                      version="{} {}".format(__package__, __version__))

  return parser.parse_args()


def create_mod(package, *modules, **kwargs):
  mod_path = [package]
  if len(modules):
    mod_path.extend(modules)
  mod = Module('.'.join(mod_path))
  mod.create(**kwargs)
  return mod


create_package = partial(create_mod, promote=True)


def title_info(title, msg):
  info('{}: {}'.format(title.rjust(20), msg))


def render_template(template, filename, **kwargs):
  with open(filename, 'w') as f:
    content = template.render(**kwargs).rstrip()
    if content:
      f.write(content + '\n')


def main():
  # Parse args
  args = parse_args()

  info('\n{}\n'.format(__package__.rjust(20)))

  # Jinja env
  env = Environment(loader=PackageLoader(__package__, 'templates'))

  # Project package
  project = create_package(args.project)
  title_info('project package', project.package_file)

  # Views package
  views = create_package(args.project, 'views')
  title_info('views package', views.package_file)

  # Blueprint imports
  blueprints = list(set(args.blueprints) | set([args.root]))
  render_template(env.get_template('views.py'), views.package_file,
                  blueprints=blueprints)

  # Blueprint modules
  blueprint_template = env.get_template('blueprint.py')
  for blueprint in blueprints:
    blueprint_mod = create_mod(args.project, 'views', blueprint)
    render_template(blueprint_template, blueprint_mod.module_file,
                    blueprint=blueprint)
    title_info('blueprint', blueprint_mod.module_file)

  # Extensions
  ext_imports = []
  ext_assigns = {}
  ext_configs = []
  ext_inits = []
  ext_reqs = []
  for extension in args.extensions:
    try:
      ext_template = env.get_template('extensions/{}.py'.format(extension))
      ext_reqs.append(ext_template.module.name)
      ext_imports.append(ext_template.module.imp())
      ext_assigns[ext_template.module.var_name] = ext_template.module.assign()
      ext_configs.append(ext_template.module.config())
      ext_inits.append(ext_template.module.init())
      title_info('extension', extension)
    except TemplateNotFound:
      title_info('extension', '{} not available'.format(extension))

  # Requirements file
  render_template(env.get_template('requirements.txt'), 'requirements.txt',
                  requirements=ext_reqs)
  title_info('requirements', 'requirements.txt')

  # Extensions module
  extensions_mod = create_mod(args.project, 'extensions')
  render_template(env.get_template('extensions.py'),
                  extensions_mod.module_file,
                  imports=ext_imports,
                  assigns=ext_assigns)
  title_info('extensions module', extensions_mod.module_file)

  # Config module
  config_mod = create_mod(args.project, 'config')
  with open(config_mod.module_file, 'w') as f:
    for config in ext_configs:
      f.write(config)
    if args.session:
      secret = repr(base64.urlsafe_b64encode(os.urandom(15)))
      f.write('\nSECRET_KEY = {}'.format(secret))
  title_info('config module', config_mod.module_file)

  # App module
  app_mod = create_mod(args.project, 'app')
  render_template(env.get_template('app.py'), app_mod.module_file,
                  project=args.project,
                  root=args.root,
                  blueprints=blueprints,
                  inits=ext_inits)
  title_info('app module', app_mod.module_file)

  # WSGI module
  wsgi_mod = create_mod(args.project, 'wsgi')
  render_template(env.get_template('wsgi.py'), wsgi_mod.module_file)
  title_info('wsgi module', wsgi_mod.module_file)

  # Run script
  runserver_mod = create_mod('runserver')
  render_template(env.get_template('runserver.py'), runserver_mod.module_file,
                  project=args.project)
  os.chmod(runserver_mod.module_file, stat.S_IRWXU)
  title_info('runserver module', runserver_mod.module_file)

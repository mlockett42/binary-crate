from fabric.api import abort, lcd, local, task, warn_only
from fabric.colors import green, red, yellow
from sys import platform
import os

local_pwd = os.path.realpath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

project_name = os.path.split(local_pwd)[-1]

@task
def build():
    print(yellow('Building docker image...'))
    with lcd('.'):
        local('docker build --tag="{0}" .'.format(project_name))

@task
def runserver():
    run(command='runserver 0.0.0.0:8000')
    #print(yellow('Running docker process...'))
    #with lcd('.'):
    #    local('docker run --tty --interactive --volume "${PWD}":/opt/project --publish=8000:8000 "${PWD##*/}" runserver 0.0.0.0:8000')


@task
def harvest():
    run(command='harvest -a landingpage --verbosity=3')

@task
def run(**kwargs):
    command = kwargs.get('command', 'check')
    print(yellow('Running docker process...'))
    with lcd('.'):
        with warn_only():
            result = local('docker start {project_name}-chrome'.format(
                project_name=project_name))
        if result.failed:
            abort(red('Could not start chrome. Have you run '
                      '\'setup_chrome\'?'))

        local('docker run --tty '
              '--interactive '
              '--publish=8000:8000 '
              '--volume "{local_pwd}":/opt/project '
              '--network={project_name}-network '
              '--network-alias=webserver '
              '{project_name} {command}'.format(command=command,
                            local_pwd=local_pwd,
                            project_name=project_name))


@task
def migrate():
    print(yellow('Running docker process...'))
    with lcd('.'):
        local('docker run --tty --interactive --volume "${PWD}":/opt/project --publish=8000:8000 "${PWD##*/}" migrate')

@task
def test():
    print(yellow('Running docker process...'))
    with lcd('.'):
        local('docker run --tty --interactive --volume "${PWD}":/opt/project --entrypoint="pytest" --publish=8000:8000 "${PWD##*/}"')

@task
def makemigrations():
    print(yellow('Running docker process...'))
    with lcd('.'):
        local('docker run --tty --interactive --volume "${PWD}":/opt/project --publish=8000:8000 "${PWD##*/}" makemigrations')

@task
def bash():
    print(yellow('Running docker process...'))
    with lcd('.'):
        local('docker run --tty --interactive --volume "${PWD}":/opt/project --publish=8000:8000 --entrypoint="bash" "${PWD##*/}"')

@task
def setup():
    build()
    migrate()

@task
def setup_network():
    print(yellow('Launching detached postgres docker process...'))
    with lcd('.'):
        local('docker network create --driver bridge {project_name}-network'
              ''.format(project_name=project_name))


@task
def setup_chrome():
    print(yellow('Launching detached postgres docker process...'))
    with lcd('.'):
        with warn_only():
            result = local('docker run --detach --name={project_name}-chrome '
                           '--network={project_name}-network '
                           '--network-alias=chrome '
                           'selenium/standalone-chrome'.format(
                            project_name=project_name))
            if result.failed:
                abort(red('Could not setup chrome. Have you run '
                          '\'setup_network\'?'))



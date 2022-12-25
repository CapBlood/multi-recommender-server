import subprocess

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

from hybrid_rs.server.django_setup import setup


def get_server_app() -> WSGIHandler:
    setup()
    application = get_wsgi_application()
    application = WhiteNoise(
        application,
        root="hybrid_rs/server")
    application.add_files("hybrid_rs/server", prefix="static/")
    return application


def run_server():
    subprocess.run(
        ['gunicorn', '-c', 'hybrid_rs/server/gunicorn_config.py', 'hybrid_rs.server.server:get_server_app()'],
    )

def manager() -> None:
    import sys
    from django.core.management import execute_from_command_line
    
    setup()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    manager()

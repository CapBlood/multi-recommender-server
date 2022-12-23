import asyncio

import uvicorn
from django.core.handlers.asgi import ASGIHandler
from django.core.asgi import get_asgi_application

from hybrid_rs.server.django_setup import setup
from hybrid_rs.server.config import config


def get_server_app() -> ASGIHandler:
    setup()
    application = get_asgi_application()
    return application


async def main() -> None:
    app = get_server_app()
    uvicorn_config = uvicorn.Config(
        app, host=config['SERVER_ADDRESS'],
        port=config['SERVER_PORT'], log_level="info")
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


def run() -> None:
    asyncio.run(main())


def manager() -> None:
    import sys
    from django.core.management import execute_from_command_line
    
    setup()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    manager()

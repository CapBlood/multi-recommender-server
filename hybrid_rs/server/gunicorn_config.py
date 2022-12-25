from hybrid_rs.server.config import config as server_config

bind = f'{server_config["ADDRESS"]}:{server_config["PORT"]}'

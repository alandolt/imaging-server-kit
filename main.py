import imaging_server_kit as serverkit

server = serverkit.Server(algorithm_name="foo", parameters_model=serverkit.Parameters)
app = server.app

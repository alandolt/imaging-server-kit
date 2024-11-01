![EPFL Center for Imaging logo](https://imaging.epfl.ch/resources/logo-for-gitlab.svg)
# 🪐 Deployment

Start the server:

```
docker compose up -d
```

**Add a new algorithm**

Start from the template:

```
cookiecutter cookiecutter_template/
```

Edit the `Parameters` and `Server` in your `main.py` to your liking.

Move your `serverkit-my-algo` folder to `./servers`.

Add an entry to `docker-compose.yml`:

```
my-algo:
  build:
    context: ./servers/serverkit-my-algo
  depends_on:
    - servers_registry
```

Restart the server:

```
docker compose restart
```

## Contributing

Contributions are very welcome.

## License

This project is distributed under the terms of the [BSD-3](http://opensource.org/licenses/BSD-3-Clause) license.

## Issues

If you encounter any problems, please file an issue along with a detailed description.

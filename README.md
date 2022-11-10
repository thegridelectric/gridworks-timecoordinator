# Gridworks Timecoordinator

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Local Demo setup

1. Set up python envirnment

   ```
   poetry install

   poetry shell
   ```

2. Install [docker](https://docs.docker.com/get-docker/)

3. Start docker containers

- **X86 CPU**:

  ```
  docker compose -f world-rabbit-x86.yml up -d
  ```

- **arm CPU**:

  ```
  docker compose -f world-rabbit-arm.yml up -d
  ```

4. Check rabbit on its console at [http://0.0.0.0:15672/#/](http://0.0.0.0:15672/#/)

   - username/password are both

     ```
     smqPublic
     ```

5. Run demo:

   ```
   python demo.py
   ```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Gridworks Timecoordinator_ is free and open source software.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/thegridelectric/gridworks-timecoordinator/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/thegridelectric/gridworks-timecoordinator/blob/main/LICENSE
[contributor guide]: https://github.com/thegridelectric/gridworks-timecoordinator/blob/main/CONTRIBUTING.md
[command-line reference]: https://gridworks-timecoordinator.readthedocs.io/en/latest/usage.html

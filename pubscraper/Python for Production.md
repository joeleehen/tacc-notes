# Python for Production
You can't just have your scripts and dependencies floating around in some random directory. Different companies/teams will have different preferences for writing Python, but here's what we did at TACC. Most of this comes from Erik's guidelines.

In general, [Erik's example repo](https://github.com/eriksf/calculate-pi/tree/main) is a good resource for a lot of different production Python stuff.

## Poetry
### Libraries
We use [Poetry](https://python-poetry.org/) to manage libraries and development. Poetry can also be used to create and distribute *packages*, but we mainly use it to handle dependencies.

Poetry should **NOT** be installed in a virtual environment, and you shouldn't `source ./bin/activate` inside a Poetry project to run scripts! This is counterintuitive, but Poetry creates its own virtual environment under the hood. RTFM for more info; the *Installation* guide can be followed exactly without creating a `venv` or anything.

>[!info] Version Management
> Erik prefers to use [asdf](https://asdf-vm.com/) to manage languages, libraries, and whatnot. I think he said he prefers to install Poetry and initialize a Poetry project *inside* of an `asdf` instance for better version handling, but I couldn't get `asdf` to work on my work machine.
> If you aren't using `asdf`, I'm pretty sure it's ok to initialize a Poetry project as normal (outside of a virtual environment)
> Use `pipx` to install Poetry if you aren't using `asdf`. If you're on a Windows machine you should fuck yourself.


Once you're inside your Poetry project, **do not** `pipx install` libraries! Add them using `poetry add {some_library}`, which will keep the libraries contained in your Poetry project and add them to `poetry.lock`. If the libraries are callable from the command line (like `pytest` or `coverage`), you might have to `pipx install` them from *outside* the Poetry project.

### Development
Running a script as normal (i.e., `python pubscraper/main.py`) won't work since the libraries are only available in Poetry's virtual environment. Run a script using `poetry run python {some_python_script}` instead. The same applies to executable libraries, like `poetry run pytest`.
Typing all that out can be a pain in the ass, so Poetry allows you to define entry points in the auto-generated `pyproject.toml` file.
##### Entry Point Scripts
Here's our file hierarchy:
```
├── LICENSE
├── README.md
├── config.py
├── poetry.lock
├── pubscraper
│   ├── APIClasses
│   │   ├── Base.py
│   │   ├── Elsevier.py
│   │   ├── IEEE.py
│   │   ├── MDPI.py
│   │   ├── PubMed.py
│   │   ├── Springer.py
│   │   ├── Wiley.py
│   │   ├── __init__.py
│   │   └── arXiv.py
│   ├── __init__.py
│   ├── main.py
│   └── version.py
├── pyproject.toml
├── requirements.txt
├── secrets.sample
└── tests
    ├── __init__.py
    ├── test_Elsevier.py
    ├── test_PubMed.py
    ├── test_Springer.py
    └── test_arXiv.py
```
If we want to add an entry point to make our `main.py` script easier to execute, we place the following in our `pyproject.toml` config file:
```toml
[tool.poetry.scripts]
pubscraper = "pubscraper.main:main"
```
We can then run our main script using
```bash
poetry run pubscraper
```
#### Misc Development
##### Testing
We use `pyteset` to write our testing suite.
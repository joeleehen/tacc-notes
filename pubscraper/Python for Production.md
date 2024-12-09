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
We use `pyteset` to write our testing suite. There's some misc configuration to do in `pyproject.toml`, but that's mainly for path management and whatnot. Here's what we have for the pubscraper project:
```toml
[tool.pytest.ini_options]
minversion = "6.0"
pythonpath = ["pubscraper/APIClasses"]
testpaths = ["tests"]
```
`pythonpath` tells Poetry where to look for our python libraries, while `testpaths` tells Poetry where to look for our actual tests.
Writing tests with `pytest` is straightforward. Every test function must begin with `test_` (e.g., `test_some_functionality()`) to be detected by `pytest`. Invoke the tests using `poetry run pytest` (I like to pass in the `-vv` flag to see each test name as it's run).
##### Responses for API Testing
It's bad practice to make actual HTTP requests in your tests for a litany of reasons:
- Tests should test your app functionality, not the API functionality
- Tests take longer to run when querying the actual API
- You waste daily query limits on testing
- Tests will fail when the API is down/some networking error occurs (this is *not* a problem with your app!)

You should mock your API requests when testing to fix these issues. We use the `responses` library to mock API requests.
I think `responses` works by intercepting HTTP requests to a given URL and serving a pre-configured response. The HTTP request never leaves the machine!
Here's one of the tests I wrote for our PubMed class:
###### Responses Example
```python
@responses.activate
def test_partial_empty_input():
    response_1 = responses.Response(
        method="GET",
        url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        status=200,
        json={"esearchresult": {"idlist": ["12345678"]}},
    )
    responses.add(response_1)
    response_2 = responses.Response(
        method="GET",
        url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        status=200,
        json={
            "result": {
                "uids": ["12345678"],
                "12345678": {
                    "authors": [{"name": "albert"}],
                    "title": "some title",
                    "fulljournalname": "some journal",
                    "sortdate": "2000/09/06",
                },
            }
        },
    )
    responses.add(response_2)
    results = PubMed.search_multiple_authors(["albert", ""])
    assert len(results) == 1
```
Each test function is decorated with `responses.activate`. We specify the status code and write a mock response that our request should return. Writing the response by hand is a pain in the ass, but it's helpful to see a (condensed) version of what output we expect from the API.
>[!faq] Caching Results
>`responses` can record an actual API response and store it in a `.yaml` file.
> The `.yaml` response can then be referenced in your tests. Recording actual responses means you don't have to write mock responses by hand, and you have actual API data to reference for development!
> We chose not to use this feature, since the resulting `.yaml` file is kinda big and hard to parse. We found it faster and leaner to write the mock data by hand.
> Use `responses._recorder` to record an API result for a given test. **Remember to stop recording** (deleting the `@recorder.record` decorator) **after recording a response!**

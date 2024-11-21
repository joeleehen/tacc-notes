# Getting Code Reviewed
#### Code is read more often than it is written.
Erik wants to review my and Magret's code before for our `pubScraper.py` app. We're designing the app, in Erik's words, "super object-oriented". I'm not used to super-OOP architecting, so I'm writing my code extra carefully.

- Docstrings at the top of every function are common. Kelsey and Erik usually explain the arguments of a function/method (what datatype they are, where they're coming from, etc.) and the output of the function.
- Linters are essential! Erik recommend `ruff` for Python. I should figure out how to use this with neovim
- We need to *test as we go!*

I did wider-scope integration tests (mainly testing `get_publications_by_author`) rather than finer-grain unit testing. I wrote my tests to maximize my code coverage and got like 97% coverage.

Here's a short script I wrote to pull publishing data from PubMed, searching by author name:
###### pubScraper/APIClasses/PubMed.py
```python
import requests
import json
import time


class Publication:
    def __init__(self, journal, pub_date, title, authors):
        self.journal = journal,
        self.pub_date = pub_date,
        self.title = title,
        self.authors = authors


# FIXME: passing an empty string for a name should remove it from the list!!
class PubMed:
    def __init__(self):
        self.search_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        self.summary_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'

    def get_UIDs_by_author(self, author_name, rows=10):
        """
        Retrieve a given author's UID publications.
        :param author_name: name of author
        :param rows: number of results to return (default is 10)
        :return: A list of UIDs corresponding to papers written by the author
        """
        # prepare Entrez query
        entrez_author_name = author_name.replace(" ", "+")
        entrez_author_name += "[author]"
        params = {
            'db':'pmc',
            'term': entrez_author_name,
            'retmax': rows,
            'retmode': 'JSON',
        }

        response = requests.get(self.search_url, params=params)

        if response.status_code != 200:
            print(f"Error fetching data from PubMed: {response.status_code}")
            return

        data = response.json()
        id_list = data['esearchresult']['idlist']

        if not id_list:
            return None

        return id_list

    def get_summary_by_UIDs(self, UIDs):
        """
        Given a list of UIDs, retrieve summary information for each UID
        :params UIDs: a list of UIDs
        :return: a list of Publication instances holding summary data for each publication
        """
        if not UIDs:
            return None
        
        # join UIDs list into one 'csv' string
        stringified_UIDs = ','.join(UIDs)
        params = {
            'db': 'pmc',
            'id': stringified_UIDs,
            'retmode': 'JSON',
        }

        response = requests.get(self.summary_url, params=params)
        if response.status_code != 200:
            print(f'Error fetching summaries from PubMed: {response.status_code}')
            return

        data = response.json()

        publications = []
        for uid in data['result']['uids']:
            summary_object = data['result'][uid]
            author_list = []
            for author_object in summary_object['authors']:
                author_list.append(author_object['name'])

            # pub = Publication(
            #     journal=summary_object['fulljournalname'],
            #     pub_date=summary_object['sortdate'],
            #     title=summary_object['title'],
            #     authors=author_list
            # )
            pub = {
                'id': uid,
                'journal': summary_object['fulljournalname'],
                'publication_date': summary_object['pubdate'],
                'title': summary_object['title'],
                'authors': ",".join(author_list)
            }
            publications.append(pub)

        return publications


    def get_publications_by_author(self, author_name, rows=10):
        UIDs = self.get_UIDs_by_author(author_name, rows)
        summary_info = self.get_summary_by_UIDs(UIDs)

        return summary_info


def search_multiple_authors(authors):
    pubmed = PubMed()
    all_results = {}

    for author in authors:
        print(f"Searching for publications by {author}...")

        try:
            publications = pubmed.get_publications_by_author(author)
            all_results[author] = publications
        except Exception as e:
            print(f"Error fetching data for {author}: {e}")
        time.sleep(0.4)    # avoids RESPONSE 429 (rate limit violation)

    return all_results

def main():
    # authors = ['albert', 'albert einstein', 'albert einsten']
    # authors = ['albert einstein']
    author_names = input("Enter author names (comma-separated): ").split(",")
    author_names = [name.strip() for name in author_names]

    results = search_multiple_authors(author_names)
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
```
###### Feedback
I'm currently missing docstrings, there aren't enough comments, and I have commented out blocks of code that looks sloppy.
Here's Erik's comment after looking over what I wrote:
*I've got lots of comments on logging, using config files, code structure, testing, and remote calls that it's probably easier to talk about them. Since this is the early days, there's no reason not to merge these in right now and then sit down and discuss.*
$$\text{damn bruh I thought my shit looked good}$$

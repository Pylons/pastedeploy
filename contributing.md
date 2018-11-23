# Contributing

All projects under the Pylons Project, including this one, follow the guidelines established at [How to Contribute](https://pylonsproject.org/community-how-to-contribute.html), [Coding Style and Standards](https://pylonsproject.org/community-coding-style-standards.html), and [Pylons Project Documentation Style Guide](https://docs.pylonsproject.org/projects/pastedeploy/).

You can contribute to this project in several ways.

*   [File an Issue on GitHub](https://github.com/Pylons/pastedeploy/issues)
*   Fork this project, create a new branch, commit your suggested change, and push to your fork on GitHub.
    When ready, submit a pull request for consideration.
    [GitHub Flow](https://guides.github.com/introduction/flow/index.html) describes the workflow process and why it's a good practice.
*   Join the [IRC channel #pyramid on irc.freenode.net](https://webchat.freenode.net/?channels=pyramid).


## Running Tests and Building Docs

Run `tox` from within your checkout. This will run the tests across all supported systems and attempt to build the docs.

To run the tests for Python 3.7 only:

    $ tox -epy3.7

To build the docs:

    $ tox -edocs

See the `tox.ini` file for details.

.. # ********** Please don't edit this file!
.. # ********** It has been generated automatically by dae_devops version 0.4.0.
.. # ********** For repository_name dls-logformatter

Developing
=======================================================================

If you plan to make change to the code in this repository, you can use the steps below.

Clone the repository::

    $ git clone https://gitlab.diamond.ac.uk/scisoft/dls-logformatter.git

It is recommended that you install into a virtual environment so this
installation will not interfere with any existing Python software.
Make sure to have at least python version 3.8 then::

    $ python3 -m venv /scratch/$USER/myvenv
    $ source /scratch/$USER/myvenv/bin/activate
    $ pip install --upgrade pip

Install the package in edit mode which will also install all its dependencies::

    $ cd dls-logformatter
    $ export PIP_FIND_LINKS=/dls_sw/apps/bxflow/artifacts
    $ pip install -e .[dev]

Now you may begin modifying the code.

|

If you plan to modify the docs, you will need to::

    $ pip install -e .[docs]

    


.. # dae_devops_fingerprint 8716693386b36e9b8dd2af71471f01ab

def convertpy2ipynb(script_name, cell_type = "code"):

    with open(script_name, "r") as f:
        lines = f.readlines()

    header = f"""
    {{
    "cells": [
    {{
    "cell_type": "{cell_type}",
    "outputs": [],
    "execution_count": null,
    "metadata": {{}},

    "source": [
    """
    source = ["    \""+line.strip("\n").replace("\\", "\\\\").replace("\"", "\\\"")+"\\n\",\n" for line in lines]
    footer = """
    ]
    }
    ],
    "metadata": {
    "kernelspec": {
    "display_name": "(1) Python 3",
    "language": "python",
    "name": "iow_python"
    },
    "language_info": {
    "codemirror_mode": {
        "name": "ipython",
        "version": 3
    },
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3",
    "version": "3.7.7"
    }
    },
    "nbformat": 4,
    "nbformat_minor": 4
    }
    """

    f = open(script_name[:-3]+".ipynb", "w")
    f.write(header)
    for line in source:
        f.write(line)
    f.write("    \"\\n\"")
    f.write(footer)
    f.close()
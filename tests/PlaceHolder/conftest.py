import ape
import pytest


@pytest.fixture(scope="module")
def placeholder(project, alice, charlie):
    # charlie is arg1
    placeholder = alice.deploy(project.PlaceHolder, charlie)
    return placeholder
#!/usr/bin/env python

"""Tests for `chemistry_nodes` package."""

import pytest
from src.chemistry_nodes.danbooru import BooruTags
from src.chemistry_nodes.tag import Tag, TagCollection, Prompt


@pytest.fixture
def boorutags_node():
    """Fixture to create an Example node instance."""
    return BooruTags()


def test_boorutags_node_initialization(boorutags_node):
    """Test that the node can be instantiated."""
    assert isinstance(boorutags_node, BooruTags)


def test_return_types():
    """Test the node's metadata."""
    assert BooruTags.RETURN_TYPES == (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    assert BooruTags.FUNCTION == "get_tags_from_id"
    assert BooruTags.CATEGORY == "Chemistry Nodes"

import pytest
from src.chemistry_nodes.tag import Tag, TagCollection, Prompt


# Tag Tests
def test_tag_init():
    # Basic initialization
    tag = Tag("test_tag")
    assert tag.raw == "test_tag"
    assert tag.normalized == "test tag"

    # Edge cases for stripping
    tag = Tag("  multiple_spaces  ")
    assert tag.raw == "multiple_spaces"
    assert tag.normalized == "multiple spaces"

    # Handling of special characters
    tag = Tag("special-char_!@#")
    assert tag.raw == "special-char_!@#"
    assert tag.normalized == "special-char !@#"


def test_tag_normalize():
    # Test with mixed case
    tag = Tag("MiXeD_CaSe")
    assert tag.normalized == "mixed case"

    # Test with numbers and special characters
    tag = Tag("tag_123_with_special!@#")
    assert tag.normalized == "tag 123 with special!@#"

    # Test multiple underscores
    tag = Tag("multiple___underscores")
    assert tag.normalized == "multiple   underscores"


def test_tag_display():
    # Test with special characters
    tag = Tag("tag-with-hyphens")
    assert tag.display == "tag-with-hyphens"

    # Test with nested parentheses
    tag = Tag("tag_with_(nested_(parentheses))")
    assert tag.display == "tag with \\(nested \\(parentheses\\)\\)"


def test_tag_matches_edge_cases():
    # Test with empty tags
    empty_tag = Tag("")
    assert empty_tag.matches("")
    assert empty_tag.matches(Tag(""))

    # Test case sensitivity
    upper_tag = Tag("ALL_CAPS")
    lower_tag = Tag("all_caps")
    mixed_tag = Tag("AlL_CaPs")
    assert upper_tag.matches(lower_tag)
    assert upper_tag.matches(mixed_tag)


# TagCollection Tests
def test_tag_collection_from_list_edge_cases():
    # Test with empty list
    collection = TagCollection.from_list([])
    assert len(collection) == 0

    # Test with None values (should be filtered)
    collection = TagCollection.from_list(["tag1", None, "tag3"])
    assert len(collection) == 2
    assert collection[0].raw == "tag1"
    assert collection[1].raw == "tag3"

    # Test with duplicate tags
    collection = TagCollection.from_list(["tag1", "tag1", "tag2"])
    assert len(collection) == 3  # Duplicates are preserved


def test_tag_collection_from_string_advanced():
    # Test with multiple separators
    collection = TagCollection.from_string("tag1,tag2,tag3", sep=",")
    assert len(collection) == 3

    # Test with tabs as separator
    collection = TagCollection.from_string("tag1\ttag2\ttag3", sep="\t")
    assert len(collection) == 3

    # Test with mixed spaces in separator
    collection = TagCollection.from_string("tag1 | tag2  |  tag3", sep="|")
    assert len(collection) == 3


def test_tag_collection_filter_out_complex():
    # Create a collection with mixed case and formatting
    collection = TagCollection.from_list(["tag1", "Tag_2", " tag3 ", "TAG4"])

    # Filter with mixed case exclusions
    filtered = collection.filter_out(["TAG1", "tAg3"])
    assert len(filtered) == 2
    assert filtered[0].raw == "Tag_2"
    assert filtered[1].raw == "TAG4"

    # Filter with exact matches only (no normalization)
    exact_matches = [tag for tag in collection if any(tag.raw == ex for ex in ["tag1", "tag3"])]
    assert len(exact_matches) == 2
    assert exact_matches[0].raw == "tag1"


def test_tag_collection_display_methods():
    # Test with empty collection
    empty_collection = TagCollection()
    assert empty_collection.to_display_list() == []
    assert empty_collection.to_display_string() == ""

    # Test with custom separator
    collection = TagCollection.from_list(["tag1", "tag2", "tag3"])
    assert collection.to_display_string(separator=" | ") == "tag1 | tag2 | tag3"

    # Test with complex tags
    complex_collection = TagCollection.from_list(["tag(1)", "tag_(2)", "tag-3"])
    assert complex_collection.to_display_list() == ["tag\\(1\\)", "tag \\(2\\)", "tag-3"]


# Prompt Tests
def test_prompt_complex_cases():
    # Test with complex prompt structure
    prompt = Prompt("(detailed:1.2), (high quality:1.3), simple background, (character:0.8)")
    assert len(prompt.tag_collection) == 4
    assert prompt.tag_collection[0].raw == "detailed"
    assert prompt.tag_collection[3].raw == "character"

    # Test with empty components
    prompt = Prompt("tag1, , tag3, ,")
    assert len(prompt.tag_collection) == 2

    # Test with deeply nested escaped parentheses
    prompt = Prompt("tag1, nested_\\(level1_\\(level2\\)_back\\), tag3")
    assert prompt.tag_collection[1].raw == "nested_(level1_(level2)_back)"


def test_prompt_remove_parentheses_complex():
    # Test with weight at the end
    assert Prompt.remove_promt_paraentheses("tag:1.5)") == "tag"

    # Test with multiple colons
    assert Prompt.remove_promt_paraentheses("tag:sub:1.2") == "tag"

    # Test with no modifications needed
    assert Prompt.remove_promt_paraentheses("simple_tag") == "simple_tag"

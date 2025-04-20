from collections.abc import Iterable


class Tag:
    def __init__(self, raw_tag):
        """Initialize a Tag object with the raw tag string from the API."""
        self.raw = raw_tag.strip()
        self.normalized = self._normalize(raw_tag)

    def _normalize(self, tag):
        """Convert tag to a standard internal format (with spaces instead of underscores)."""
        # Replace underscores with spaces and standardize
        return tag.strip().lower().replace("_", " ")

    @property
    def display(self):
        """Return the display format (spaces instead of underscores, escaped parentheses)."""
        result = self.raw.replace("_", " ")
        result = result.replace("(", "\\(").replace(")", "\\)")
        return result

    def matches(self, other):
        """
        Check if this tag matches another tag, regardless of format.
        `other` can be a string or another Tag object.
        """
        if isinstance(other, Tag):
            return self.normalized == other.normalized
        return self.normalized == self._normalize(other)

    def __eq__(self, other):
        if isinstance(other, Tag):
            return self.raw == other.raw
        return self.raw == other

    def __str__(self):
        return self.display

    def __repr__(self):
        return f"Tag({self.raw!r})"


class Prompt:
    def __init__(self, text):
        """Initialize a Prompt object with the prompt text."""
        self.text = text.strip()
        tags = self.text.split(",")
        # remove escape characters
        tags = [tag.replace("\\(", "(").replace("\\)", ")") for tag in tags]
        tags = [self.remove_promt_paraentheses(tag.strip()) for tag in tags]
        self.tag_collection = TagCollection.from_list(tags)

    @staticmethod
    def remove_promt_paraentheses(tag: str) -> str:
        """Remove parentheses and their content from a tag string."""
        if tag.startswith("("):
            tag = tag[1:]
        tag = tag.split(":")[0]
        if "(" in tag:
            return tag
        if tag.endswith(")"):
            tag = tag[:-1]
        return tag

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"Prompt({self.text!r})"


class TagCollection:
    def __init__(self):
        """Initialize with a list of raw tags, or empty list if None."""
        self.tags = []

    @staticmethod
    def from_list(tag_list: Iterable) -> "TagCollection":
        """Create a TagCollection from a list of raw tags."""
        tag_collection = TagCollection()
        if not isinstance(tag_list, Iterable):
            raise TypeError("tag_list must be an iterable of strings")
        for tag in tag_list:
            if tag:  # Skip empty tags
                tag_collection.tags.append(Tag(tag))
        return tag_collection

    @staticmethod
    def from_string(tag_string, sep: str = " ") -> "TagCollection":
        """Create a TagCollection from a string of raw tags."""
        if "," in tag_string and sep != ",":
            msg = "Comma-separated tags detected. Use a different separator or remove commas."
            raise ValueError(msg)
        tag_list = tag_string.split(sep=sep)
        tag_list = [tag.strip() for tag in tag_list]

        return TagCollection.from_list(tag_list)

    def filter_out(self, exclusion_list):
        """
        Remove tags that match any in the exclusion list.
        exclusion_list can be a list of strings or Tag objects.
        Returns a new TagCollection.
        """
        exclusion_tags = [t if isinstance(t, Tag) else Tag(t) for t in exclusion_list]
        result = TagCollection()
        result.tags = [t for t in self.tags if not any(t.matches(ex) for ex in exclusion_tags)]
        return result

    @property
    def as_list(self):
        """Return a list of raw tags."""
        return self.to_display_list()

    @property
    def as_string(self):
        """Return a string of raw tags, joined by spaces."""
        return self.to_display_string()

    def to_display_list(self):
        """Return a list of tags in display format."""
        return [tag.display for tag in self.tags]

    def to_display_string(self, separator=", "):
        """Return a string of tags in display format, joined by separator."""
        return separator.join(self.to_display_list())

    def __len__(self):
        return len(self.tags)

    def __iter__(self):
        return iter(self.tags)

    def __getitem__(self, index):
        return self.tags[index]

    def __str__(self):
        return f"TagCollection({len(self.tags)} tags)"

    def __repr__(self):
        return f"TagCollection({self.tags!r})"

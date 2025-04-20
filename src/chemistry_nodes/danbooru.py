import requests

from .tag import Tag, TagCollection, Prompt


class BooruTags:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "id": (
                    "INT",
                    {
                        "default": 9173633,
                        "min": 0,  # Minimum value
                        "max": 2147483648,  # Maximum value
                        "step": 1,  # Slider's step
                        "display": "number",  # Cosmetic only: display as "number" or "slider"
                    },
                ),
                "black_list": ("STRING", {"multiline": True, "placeholder": "twitter username", "dynamicPrompts": True}),
            },
            "optional": {
                "positive": ("STRING", {"forceInput": True}),
                "negative": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "positive prompt",
        "tags",
        "character",
        "artist",
        "id",
    )
    FUNCTION = "get_tags_from_id"
    OUTPUT_NODE = True
    CATEGORY = "Chemistry Nodes"

    def get_tags_from_id(self, id: int, black_list: str, positive: str = "", negative: str = ""):
        negative_prompt = Prompt(negative)
        positive_prompt = Prompt(positive)
        black_list = Prompt(black_list)

        danbooru_json = Danbooru(id).get_json()

        general_collection = TagCollection.from_string(danbooru_json.get("tag_string_general"))

        character_tag = Tag(danbooru_json.get("tag_string_character"))
        artist_tag = Tag(danbooru_json.get("tag_string_artist"))

        filtered = general_collection.filter_out(positive_prompt.tag_collection.as_list)
        filtered = filtered.filter_out(negative_prompt.tag_collection.as_list)
        filtered = filtered.filter_out(black_list.tag_collection.as_list)

        return (positive, filtered.as_string, character_tag.display, artist_tag.display, str(id))


class Danbooru:
    def __init__(self, id: int) -> None:
        self.id = id
        self.json = None

    def get_json(self) -> str:
        base_url = "https://danbooru.donmai.us/posts/"
        response = requests.get(f"{base_url}{self.id}.json")
        response.raise_for_status()
        self.json = response.json()
        return self.json

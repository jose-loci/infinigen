import os
import numpy as np
from infinigen.assets.objects.trees.generate import TreeFactory
from openai import OpenAI
from infinigen.core import init, surface

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

SEED = 0
IDX = 0


def get_tree(**kwargs):
    location = kwargs.get(
        "location", (np.random.uniform(-10, 10), np.random.uniform(-10, 10))
    )
    x, y = location
    if "location" in kwargs:
        del kwargs["location"]

    print(kwargs)

    fac = TreeFactory(**kwargs)
    asset = fac.spawn_asset(IDX, loc=(x, y, 0))

    return asset

def init_surface():
    init.apply_gin_configs(
        [
            "infinigen_examples/configs_nature",
        ],
        configs=None,
        overrides=None,
        skip_unknown=True,
    )
    surface.registry.initialize_from_gin()

def run_mvp_function():
    init_surface()
    tree = get_tree()
    return tree

system_prompt = """You are a helpful assistant that modifies a list of dictionaries representing two trees.
You can only modify the values of the configuration file. 
The possible values of a dictionary are "seed", "season", "fruit_chance" and location.
An example of a configuration file is: [{"seed": 0, "season": "winter", "fruit_chance": 0.0, location(5, 10)}, null]
Seasons are "winter", "spring", "summer" and "autumn".
You can not add or remove trees from the list. To add a tree you can only replace a null value with a dictionary.
To add a tree to the list, you must provide a dictionary.
To remove a tree from the list, you must provide a null value.
Your response is always a modified version of the input list of dictionaries."""

default_config = """TreeFactory.seed = 0
TreeFactory.season = "winter"
TreeFactory.fruit_chance = 0.5
TreeFactory.fruit_weights = {"apple": 0.0, "blackberry": 0.0, "coconutgreen": 0.0, "durian": 0.0, "starfruit": 1.0, "strawberry": 0.0, "compositional_fruit": 0.0}
TreeFactory.leaf_density = 1.0
TreeFactory.tree_species_code = {
        "tree_size_or_age": 0.5,
        "trunk_warp": 0.5,
        "n_trunks": 0.5,
        "branch_start": 0.5,
        "branch_angle": 0.5,
        "multi_branch": 0.5,
        "branch density": 0.5,
        "branch_len": 0.5,
        "branch_warp": 0.5,
        "pull_dir_vt": 0.5,
        "pull_dir_hz": 0.5,
        "outgrowth": 0.5,
        "branch_thickness": 0.5,
        "twig_density": 0.5,
        "twig_scale": 0.5,
}"""


def change_config(user_prompt: str, config_str: str = None) -> str:
    user_prompt = f"{user_prompt}: {config_str}"

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    gpt_output = completion.choices[0].message.content
    return gpt_output

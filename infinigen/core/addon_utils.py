def get_tree():
    from infinigen.assets.objects.trees.generate import TreeFactory
    from infinigen.core import init, surface

    SEED = 0
    IDX = 0

    init.apply_gin_configs(
        ["infinigen_examples/configs_indoor", "infinigen_examples/configs_nature"],
        configs=None,
        overrides=None,
        skip_unknown=True,
    )
    surface.registry.initialize_from_gin()

    print("---- HELLO ----")
    fac = TreeFactory(seed=SEED)
    asset = fac.spawn_asset(IDX)

    return asset

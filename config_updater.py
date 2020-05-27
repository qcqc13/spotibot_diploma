def update_config(config_file, config_obj):
    with open(config_file, 'w') as config:
        config_obj.write(config)
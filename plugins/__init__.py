# db_tool/plugins/__init__.py

# Implement this as an entry point for plugins
def load_plugin(plugin_name):
    try:
        plugin = __import__(f'db_tool.plugins.{plugin_name}', fromlist=[''])
        return plugin
    except ImportError:
        raise RuntimeError(f"Plugin {plugin_name} could not be loaded.")



try:
    import ddgs
    print("Imported ddgs successfully")
except ImportError:
    print("Could not import ddgs")

try:
    import duckduckgo_search
    print("Imported duckduckgo_search successfully")
    print(f"Version: {duckduckgo_search.__version__}")
except ImportError:
    print("Could not import duckduckgo_search")

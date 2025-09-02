import zepp_cloud


def test_package_import_and_version():
    assert hasattr(zepp_cloud, "__version__")
    assert isinstance(zepp_cloud.__version__, str)

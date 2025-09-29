def test_import_package():
    import csvtojson
    assert hasattr(csvtojson, "__version__")
def test_docs():
    from doctest import testfile
    import os
    docdir = '../doc'
    total_failures = 0
    total_tests = 0
    for root, dirs, files in os.walk(docdir):
        for fn in files:
            if fn.endswith('.rst'):
                docfile = os.path.join(root, fn)
                fail, nt = testfile(docfile)
                total_failures += fail
                total_tests += nt
    assert total_failures == 0
        
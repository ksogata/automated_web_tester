class CustomAssertions():
    def assertListContains(self, results_list, *args):
        # for each string supplied in *args, check if present in results_list
        for arg in args:
            if arg not in results_list:
                raise AssertionError(str('Element: ' + arg +
                                         ' not in autocomplete results.'))

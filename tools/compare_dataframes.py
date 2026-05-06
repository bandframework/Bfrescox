from pandas.testing import assert_frame_equal


def compare_dataframes(result, expected, abs_diff_tolr, rel_diff_tolr):
    """
    .. todo::
        * This should be in utils.py in the package.
    """
    assert (abs_diff_tolr >= 0.0) and (rel_diff_tolr >= 0.0)
    if (abs_diff_tolr == 0.0) and (rel_diff_tolr == 0.0):
        assert_frame_equal(
            result, expected,
            check_dtype=True, check_index_type=True, check_column_type=True,
            check_frame_type=True, check_names=True, check_like=False,
            check_exact=True,
        )
    else:
        # Assume that if only one tolerance is positive that the user would
        # never intend for us to check that the arrays are also identical.
        if abs_diff_tolr > 0.0:
            assert_frame_equal(
                result, expected,
                check_dtype=True, check_index_type=True, check_column_type=True,
                check_frame_type=True, check_names=True, check_like=False,
                check_exact=False, rtol=0.0, atol=abs_diff_tolr,
            )
        if rel_diff_tolr > 0.0:
            assert_frame_equal(
                result, expected,
                check_dtype=True, check_index_type=True, check_column_type=True,
                check_frame_type=True, check_names=True, check_like=False,
                check_exact=False, rtol=rel_diff_tolr, atol=0.0,
            )

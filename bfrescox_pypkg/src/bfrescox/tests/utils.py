import numpy as np


def compare_arrays(result, expected, abs_diff_tolr, rel_diff_tolr):
    if (abs_diff_tolr == 0.0) and (rel_diff_tolr == 0.0):
        np.testing.assert_equal(result, expected)
    else:
        if abs_diff_tolr > 0.0:
            np.testing.assert_allclose(
                result,
                expected,
                rtol=0.0,
                atol=abs_diff_tolr,
            )
        if rel_diff_tolr > 0.0:
            np.testing.assert_allclose(
                result,
                expected,
                rtol=rel_diff_tolr,
                atol=0.0,
            )

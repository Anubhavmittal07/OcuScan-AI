import pytest
from src.database import sanitize_for_json

def test_sanitize_numpy_integers():
    import numpy as np
    data = {"val": np.int64(42)}
    clean = sanitize_for_json(data)
    assert isinstance(clean["val"], int)
    assert clean["val"] == 42

def test_sanitize_numpy_floats():
    import numpy as np
    data = {"hb": np.float32(12.75)}
    clean = sanitize_for_json(data)
    assert isinstance(clean["hb"], float)
    assert round(clean["hb"], 2) == 12.75

def test_sanitize_numpy_arrays():
    import numpy as np
    data = {"matrix": np.array([1, 2, 3])}
    clean = sanitize_for_json(data)
    assert isinstance(clean["matrix"], list)
    assert clean["matrix"] == [1, 2, 3]

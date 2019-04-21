import json
import os

import pytest


@pytest.fixture
def config():
	data = {
	    "generator": {
	        "decay_masses": [
	            0,
	            0
	        ],
	        "original_mass": 0.134
	    },
	    "momentum_distribution": {
	        "function": [
	            "x[0] * [0] + [1]",
	            20,
	            100
	        ],
	        "parameters": [
	            -1,
	            100
	        ]
	    },
	    "n_events": 1000
	}
	conffile = "config/conf_test.json"
	with open(conffile, "w") as file:
		json.dump(data, file)

	yield conffile
	os.remove(conffile)

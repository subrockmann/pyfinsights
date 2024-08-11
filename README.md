# pyfinsights


## Developer Information

To run the tests use
```
python setup.py pytest
```

To create a library for installation
```
python setup.py bdist_wheel
```

The library will be in the "dist" folder. To install the library into another project use

```
% pip install /path/to/wheelfile.whl
```
#!/bin/bash
twine upload --config-file ~/.pypirc --repository spellcrypt dist/* --verbose

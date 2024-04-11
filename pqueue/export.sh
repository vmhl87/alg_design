#!/bin/bash

mkdir state-sorting-project/

cp README.md heap.py docs.py container.py state.py stats.py regions.py main.py state-sorting-project/

zip -r state-sorting-project.zip state-sorting-project/

rm -rf state-sorting-project/

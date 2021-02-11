package de test pour comprendre comment les utiliser

______ utilisation ______

import pptest
>>> coucou je suis ini

import pptest.testA
>>> coucou je suis ini
>>> coucou je suis a

______ installation ______

cd pptest-container/
python setup.py install

j'ai créé

pptest-container/
	setup.py	# le nom peut être modifié
	pptest/
		__init__.py
		testA.py
		testB.py

après l'installation

pptest-container/
	build/
	dist/
	pp_test.egg-info/
	setup.py
	pptest/
		__init__.py
		testA.py
		testB.py

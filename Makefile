run-server:
	./bin/gunicorn -b 127.0.0.1:8010 --reload 'doctor_appointment_demo.app:get_app()'

setup-server:
	python3 -m virtualenv venv && \
	./venv/bin/pip install --upgrade "setuptools<52" zc.buildout && \
	./venv/bin/buildout

code-check:
	./bin/pylint doctor_appointment_demo

run-client:
	npm run serve --prefix web_app

setup-client:
	npm i --prefix web_app

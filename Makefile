run:
	./bin/gunicorn -b 127.0.0.1:8010 --reload -t 300 'doctor_appointment_demo.app:get_app()'

code-check:
	./bin/pylint doctor_appointment_demo

setup:
	python3 -m virtualenv venv && \
	./venv/bin/pip install --upgrade "setuptools<52" zc.buildout && \
	./venv/bin/buildout

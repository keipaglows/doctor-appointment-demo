from setuptools import setup


setup(
    name='doctor_appointment_demo',
    version='0.1',
    packages=['doctor_appointment_demo'],
    zip_safe=False,
    python_requires='>=3.8',
    install_requires=[
        'falcon',
        'marshmallow',
        'requests'
    ]
)

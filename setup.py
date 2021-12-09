import setuptools 

setuptools.setup( 
    name='lwm2pdf', 
    version='1.0', 
    author='Danny Elfanbaum', 
    author_email='drelfanbuam@gmail.com', 
    description='Creates a PDF from lightweight markup source files', 
    packages=setuptools.find_packages(), 
    entry_points={ 
        'console_scripts': [ 
            'lwm2pdf = lwm2pdf.lwm2pdf:main' 
        ] 
    }, 
    classifiers=[ 
        'Programming Language :: Python :: 3', 
        # 'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent', 
    ], 
)
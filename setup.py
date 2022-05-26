from setuptools import setup, find_packages 
  
long_description = 'Simple command line tool for launching an image search app using elasticsearch and mobilenet embeddings.' 
  
setup( 
        name ='photoscope', 
        version ='1.0.2', 
        author ='Smells Like ML', 
        author_email ='contact@smellslikeml.com', 
        url ='https://github.com/smellslikeml/photoscope', 
        description ='Elasticsearch + Flask for diy image search', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'photoscope = photoscope.main:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='smellslikeml, machine learning, search', 
        include_package_data=True,
        install_requires = [
            'tensorflow==2.7.2',
            'tensorflow_hub==0.7.0',
            'elasticsearch==7.6.0',
            'pillow==7.0.0',
            'flask==1.1.1',
            'requests'
            ], 
        zip_safe = False
) 


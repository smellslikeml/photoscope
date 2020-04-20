from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = 'Simple command line tool for launching an image search app using elasticsearch and mobilenet embeddings.' 
  
setup( 
        name ='photoscope', 
        version ='1.0.0', 
        author ='Smells Like ML', 
        author_email ='contact@smellslikeml.com', 
        url ='https://github.com/smellslikeml/ImageSearchApp', 
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
        install_requires = requirements, 
        zip_safe = False
) 


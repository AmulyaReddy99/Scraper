from distutils.core import setup

setup(
	name = 'scraper',
	version = '1.0.1',
	py_modules = ['scraper'],
	author = 'Amulya Reddy',
	author_email = 'amulyareddyk97@gmail.com',
	url = 'https://github.com/AmulyaReddy99/Scraper',
	entry_points = ''' 
		[console_scripts]
		scraper = scraper: cli
	''',
	description = 'A web scraper that provides an interface for data, collected from a website, in the form of graphs.This software, from users corner, helps in a quicklook at the trends rather than the going through long tedious data sheets. The expected users are extensively business oriented and sports oriented. Business organisations can select Top Companies by the category for the charts/analytics. The other important users are from sports field. For improvement in any field, esp. in sports, analysis of opponents plays a key role. For sports enthusiasts, this platform serves best to see the trends of sports',
)

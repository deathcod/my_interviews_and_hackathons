import pytest
import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))


from src import scrapping_sites
def test__codeforces():
	print (scrapping_sites.codeforces(DEPLOY = True))
	print (scrapping_sites.codeforces(DEPLOY = False))
	pass


def test__codechef():
	print (scrapping_sites.codechef(DEPLOY = True))
	print (scrapping_sites.codechef(DEPLOY = False))
	pass


#test__codeforces()
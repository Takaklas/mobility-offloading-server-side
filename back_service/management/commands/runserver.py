# Override the value of the constant coded into django...
import django.core.management.commands.runserver as runserver
runserver.DEFAULT_PORT="8002"

# ...print out a warning...
# (This gets output twice because runserver fires up two threads (one for autoreload).
#  We're living with it for now :-)
import os
dir_path = os.path.splitext(os.path.relpath(__file__))[0]
python_path = dir_path.replace(os.sep, ".")
print "Using %s with default port %s" % (python_path, runserver.DEFAULT_PORT)

# ...and then just import its standard Command class.
# Then manage.py runserver behaves normally in all other regards.
from django.core.management.commands.runserver import Command

# Configuration file, useful to avoid hard-coded ip's 
# and other options.

# Back Service:

# Here, define list of edge server ips:'
server_ips = ['10.0.0.1','10.0.0.2']

# Front Service:

# Choose whether servers should do the image classification.
# If not, define the server url and port which should do it

local_classify = True

# classification_server = "http://0.0.0.0:8002/ca_tf/imageUpload/"
classification_server = "http://10.0.0.4:8002/ca_tf/imageUpload/"

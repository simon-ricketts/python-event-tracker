# SERVERS #

http_server:
	cd server; python3 main.py

test_server:
	cd server; python3 main.py -t


# TESTING #

unit:
	cd server; python3 -m unittest discover -v test/unit

# IMPORTANT - Ensure test_server is running prior
integration:
	cd server; python3 -m unittest discover -v test/integration

# IMPORTANT - Ensure test_server is running prior
test:
	cd server; python3 -m unittest discover -v test/unit; python3 -m unittest discover -v test/integration




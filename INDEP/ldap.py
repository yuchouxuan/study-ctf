from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, MOCK_SYNC
REAL_SERVER = 'my_real_server'
REAL_USER = 'cn=my_real_user,ou=test,o=lab'
REAL_PASSWORD = 'my_real_password'

# Retrieve server info and schema from a real server
server = Server(REAL_SERVER, get_info=ALL)
connection = Connection(server, REAL_USER, REAL_PASSWORD, auto_bind=True)

# Store server info and schema to json files
server.info.to_file('my_real_server_info.json')
server.schema.to_file('my_real_server_schema.json')

# Read entries from a portion of the DIT from real server and store them in a json file
if connection.search('ou=test,o=lab', '(objectclass=*)', attributes=ALL_ATTRIBUTES):
    connection.response_to_file('my_real_server_entries.json', raw=True)

# Close the connection to the real server
connection.unbind()

# Create a fake server from the info and schema json files
fake_server = Server.from_definition('my_fake_server', 'my_real_server_info.json', 'my_real_server_schema.json')

# Create a MockSyncStrategy connection to the fake server
fake_connection = Connection(fake_server, user='cn=my_user,ou=test,o=lab', password='my_password', client_strategy=MOCK_SYNC)

# Populate the DIT of the fake server
fake_connection.strategy.entries_from_json('my_real_server_entries.json')

# Add a fake user for Simple binding
fake_connection.strategy.add_entry('cn=my_user,ou=test,o=lab', {'userPassword': 'my_password', 'sn': 'user_sn', 'revision': 0})

# Bind to the fake server
fake_connection.bind()
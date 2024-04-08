from src.model.database import connect, close, add_expected_values

conn = connect()
add_expected_values(conn)
close(conn)
// Insert the TestMarker node to mark the database as a test database
MERGE (n:TestMarker {name: 'TEST_DATABASE'});

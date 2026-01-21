// 1) Replace Employment Indexes
DROP INDEX officerRanks IF EXISTS;
DROP INDEX officerBadgeNumbers IF EXISTS;

CREATE FULLTEXT INDEX officerRanks IF NOT EXISTS
FOR (n:Employment) ON EACH [n.highest_rank];

CREATE FULLTEXT INDEX officerBadgeNumbers IF NOT EXISTS
FOR (n:Employment) ON EACH [n.badge_number];

// 2) Migrate (:Officer)-[:employment_rel]-(:Unit) to ->
//            (:Officer)-[]-(:Employment)-[]-(:Unit)

// Process in batches for safety/performance
CALL () {
  MATCH (o:Officer)-[r:MEMBER_OF_UNIT]->(u:Unit)
  WHERE r.highest_rank IS NULL
  MERGE (o)<-[:HELD_BY]-(e:Employment)-[:IN_UNIT]->(u)
    ON CREATE SET e.uid = replace(randomUUID(), "-", "")
    SET
      e.earliest_date = r.earliest_date,
      e.latest_date   = r.latest_date,
      e.badge_number  = r.badge_number
} IN TRANSACTIONS OF 500 ROWS;

CALL () {
  MATCH (o:Officer)-[r:MEMBER_OF_UNIT]->(u:Unit)
  WHERE r.highest_rank IS NOT NULL
  MERGE (o)<-[:HELD_BY]-(e:Employment {highest_rank: r.highest_rank})-[:IN_UNIT]->(u)
    ON CREATE SET e.uid = replace(randomUUID(), "-", "")
    SET
      e.earliest_date = r.earliest_date,
      e.latest_date   = r.latest_date,
      e.badge_number  = r.badge_number
} IN TRANSACTIONS OF 500 ROWS;

// Remove old relationships
CALL () {
  MATCH (o:Officer)-[r:MEMBER_OF_UNIT]->(u:Unit)
  DELETE r
} IN TRANSACTIONS OF 1000 ROWS;



// 3) Migrate Citation timestamps from Epoch to neo4j datetime
CALL () {
  MATCH ()-[r:UPDATED_BY]->()
  WHERE r.date IS NOT NULL
    AND r.timestamp IS NULL
  SET r.timestamp = datetime({ epochSeconds: toInteger(r.date) })
  REMOVE r.date
} IN TRANSACTIONS OF 500 ROWS;

// 4) Migrate Unit properties to new schema
CALL () {
  MATCH (u:Unit)
  WHERE u.address IS NOT NULL
    OR u.city IS NOT NULL
    OR u.state IS NOT NULL
    OR u.zip IS NOT NULL
  SET u.hq_address = u.address,
      u.hq_city    = u.city,
      u.hq_state   = u.state,
      u.hq_zip     = u.zip
  REMOVE u.address,
         u.city,
         u.state,
         u.zip
} IN TRANSACTIONS OF 500 ROWS;

CALL () {
  MATCH (u:Unit)-[]-(a:Agency)
  WHERE u.hq_state IS NULL
    AND a.hq_state IS NOT NULL
  SET u.hq_state   = a.hq_state
} IN TRANSACTIONS OF 500 ROWS;

// Optional: Prune Agency nodes with no hq_state
CALL () {
  MATCH (a:Agency)
  WHERE a.hq_state IS NULL
    AND NOT (a)-[]-(:Unit)
  DETACH DELETE a
} IN TRANSACTIONS OF 500 ROWS;
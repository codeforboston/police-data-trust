// 1) Migrate legacy UPDATED_BY relationship citations to Change nodes
MATCH (n)-[r:UPDATED_BY]->(s:Source)
CALL (n, r, s) {
  CREATE (c:Change {
    uid: replace(randomUUID(), "-", ""),
    timestamp: coalesce(r.timestamp, datetime()),
    url: r.url,
    diff: r.diff
  })

  CREATE (c)-[:ATTRIBUTED_TO]->(s)
  CREATE (c)-[:CHANGE_TO]->(n)

  WITH c, r
  OPTIONAL MATCH (u:User {uid: r.user_uid})
  FOREACH (_ IN CASE WHEN u IS NULL THEN [] ELSE [1] END |
    CREATE (c)-[:MADE_BY]->(u)
  )
} IN TRANSACTIONS OF 25 ROWS;


// 2) Remove legacy UPDATED_BY relationships after backfill
CALL () {
  MATCH ()-[r:UPDATED_BY]->(:Source)
  DELETE r
} IN TRANSACTIONS OF 1000 ROWS;

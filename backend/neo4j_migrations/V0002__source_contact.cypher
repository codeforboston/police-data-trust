// 1) Ensure unique EmailContact.email
CREATE CONSTRAINT emailcontact_email_unique IF NOT EXISTS
FOR (e:EmailContact) REQUIRE e.email IS UNIQUE;

// 2) Migrate Source.contact_email -> (:EmailContact {email}) + [:HAS_CONTACT_EMAIL]

// Process in batches for safety/performance
CALL () {
  MATCH (u:Source)
  WHERE u.contact_email IS NOT NULL AND toString(u.contact_email) <> ""

  // Create or reuse the EmailContact for this address
  MERGE (e:EmailContact {email: u.contact_email})
    ON CREATE SET
      e.confirmed = false   // default; adjust if you want to infer from user props
  // If you previously stored confirmation timestamp on User, carry it over if present
  SET e.email_confirmed_at =
        coalesce(e.email_confirmed_at, u.email_confirmed_at)

  // Connect as primary email (idempotent)
  MERGE (u)-[:HAS_CONTACT_EMAIL]->(e)

  // Remove legacy property from User
  REMOVE u.contact_email

} IN TRANSACTIONS OF 500 ROWS;


// 3) Add Social Media Contacts if not present on Source
CALL () {
  MATCH (u:Source)
  WHERE NOT (u)-[:HAS_SOCIAL_MEDIA_CONTACT]->(:SocialMediaContact)

  // Create a SocialMediaContact and connect (idempotent)
  CREATE (s:SocialMediaContact)
  MERGE (u)-[:HAS_SOCIAL_MEDIA_CONTACT]->(s)
} IN TRANSACTIONS OF 500 ROWS;

// 4) Add slugs to Sources if not present
CALL () {
  MATCH (s:Source)
  WHERE s.slug IS NULL AND s.name IS NOT NULL
  WITH s, toLower(trim(s.name)) AS n

  WITH s,
    replace(replace(replace(replace(replace(replace(replace(replace(replace(replace(
      n,
      "&", " and "
    ), ".", ""
    ), ",", ""
    ), ":", ""
    ), ";", ""
    ), "'", ""
    ), "\"", ""
    ), "(", ""
    ), ")", ""
    ), "/", "-"
    ) AS cleaned

  WITH s, replace(cleaned, " ", "-") AS dashed
  WITH s, replace(replace(replace(replace(dashed, "--", "-"), "--", "-"), "--", "-"), "--", "-") AS collapsed
  WITH s, btrim(collapsed, "-") AS base

  SET s.slug_base = CASE
    WHEN base IS NULL OR base = "" THEN toString(s.uid)
    ELSE base
  END
} IN TRANSACTIONS OF 1000 ROWS;

CALL () {
  MATCH (s:Source)
  WHERE s.slug IS NULL AND s.slug_base IS NOT NULL
  WITH DISTINCT s.slug_base AS base
  
  MATCH (n:Source)
  WHERE n.slug IS NULL AND n.slug_base = base
  WITH base, collect(n) AS nodes

  OPTIONAL MATCH (e:Source {slug: base})
  WITH base, nodes, count(e) AS existing

  UNWIND range(0, size(nodes)-1) AS i
  WITH base, nodes[i] AS n, existing, i
  SET n.slug =
    CASE
      WHEN existing + i = 0 THEN base
      ELSE base + "-" + toString(existing + i + 1)
    END,
    n.slug_generated = true,
    n.slug_generated_from = n.name
  REMOVE n.slug_base
} IN TRANSACTIONS OF 50 ROWS;



// 5) Optional clean-up / reporting helpers (safe to keep or run separately)

// Verify no Sources still have an email property
// MATCH (u:Source) WHERE exists(u.email) RETURN count(u) AS sources_still_with_email;

// Count how many Sources have a primary email relationship after migration
// MATCH (u:Source)-[:HAS_CONTACT_EMAIL]->(:EmailContact) RETURN count(u) AS sources_with_primary_email;
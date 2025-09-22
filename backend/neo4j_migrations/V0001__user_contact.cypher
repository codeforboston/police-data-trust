// 1) Ensure unique EmailContact.email
CREATE CONSTRAINT emailcontact_email_unique IF NOT EXISTS
FOR (e:EmailContact) REQUIRE e.email IS UNIQUE;

// 2) Migrate User.email -> (:EmailContact {email}) + [:HAS_PRIMARY_EMAIL]

// Process in batches for safety/performance
CALL () {
  MATCH (u:User)
  WHERE u.email IS NOT NULL AND toString(u.email) <> ""

  // Create or reuse the EmailContact for this address
  MERGE (e:EmailContact {email: u.email})
    ON CREATE SET
      e.confirmed = false   // default; adjust if you want to infer from user props
  // If you previously stored confirmation timestamp on User, carry it over if present
  SET e.email_confirmed_at =
        coalesce(e.email_confirmed_at, u.email_confirmed_at)

  // Connect as primary email (idempotent)
  MERGE (u)-[:HAS_PRIMARY_EMAIL]->(e)

  // Remove legacy property from User
  REMOVE u.email

} IN TRANSACTIONS OF 500 ROWS;

// 3) Migrate User.phone_number -> (:PhoneContact {phone_number}) + [:HAS_PHONE_CONTACT]
CALL () {
  MATCH (u:User)
  WHERE u.phone_number IS NOT NULL AND toString(u.phone_number) <> ""

  // Create or reuse the PhoneContact for this number
  MERGE (p:PhoneContact {phone_number: u.phone_number})

  // Connect as a phone contact (idempotent)
  MERGE (u)-[:HAS_PHONE_CONTACT]->(p)

  // Remove legacy property from User
  REMOVE u.phone_number

} IN TRANSACTIONS OF 500 ROWS;

// 4) Add Social Media Contacts if not present on User
CALL () {
  MATCH (u:User)
  WHERE NOT (u)-[:HAS_SOCIAL_MEDIA_CONTACT]->(:SocialMediaContact)

  // Create a SocialMediaContact and connect (idempotent)
  CREATE (s:SocialMediaContact)
  MERGE (u)-[:HAS_SOCIAL_MEDIA_CONTACT]->(s)
} IN TRANSACTIONS OF 500 ROWS;

// 5) Optional clean-up / reporting helpers (safe to keep or run separately)

// Verify no Users still have an email property
// MATCH (u:User) WHERE exists(u.email) RETURN count(u) AS users_still_with_email;

// Count how many Users have a primary email relationship after migration
// MATCH (u:User)-[:HAS_PRIMARY_EMAIL]->(:EmailContact) RETURN count(u) AS users_with_primary_email;

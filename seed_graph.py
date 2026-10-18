"""
BreachPath - Graph Seeder
Populates FalkorDB Cloud with a realistic multi-hop Cloud Security IAM graph.
"""
from config import get_graph

def seed_database():
    print("[*] Connecting to FalkorDB Cloud...")
    g = get_graph()
    
    print("[*] Resetting graph schema for clean demo...")
    try:
        g.delete()
    except Exception:
        pass
    
    # Re-select after delete
    g = get_graph()
    
    print("[*] Creating Cloud Infrastructure Entities (Users, Roles, Compute, Secrets, Crown Jewels)...")
    
    create_query = """
    // 1. Users
    CREATE (dave:User {id: 'usr-1', name: 'dave-contractor', role: 'External Contractor', mfa_enabled: false, status: 'Compromised'})
    CREATE (alice:User {id: 'usr-2', name: 'alice-lead', role: 'Security Architect', mfa_enabled: true, status: 'Active'})
    CREATE (bob:User {id: 'usr-3', name: 'bob-intern', role: 'Frontend Intern', mfa_enabled: true, status: 'Active'})

    // 2. Groups
    CREATE (grp_contractor:Group {id: 'grp-1', name: 'Contractors-Dev-Group'})
    CREATE (grp_eng:Group {id: 'grp-2', name: 'Core-Engineering-Group'})

    // 3. IAM Roles
    CREATE (role_staging:Role {id: 'role-1', name: 'StagingDeployerRole', max_session_duration: 3600})
    CREATE (role_readonly:Role {id: 'role-2', name: 'ReadOnlyViewerRole', max_session_duration: 7200})

    // 4. Compute Resources
    CREATE (ec2_ci:Compute {id: 'ec2-1', name: 'CI-Runner-Instance', type: 'EC2', public_ip: true, vpc: 'vpc-staging'})
    CREATE (ec2_web:Compute {id: 'ec2-2', name: 'Public-Web-Server', type: 'EC2', public_ip: true, vpc: 'vpc-dmz'})

    // 5. Secrets and Keys
    CREATE (key_kms:Secret {id: 'sec-1', name: 'CI_KMS_KEY', type: 'KMS_Key', region: 'ap-south-1'})
    CREATE (sec_prod:Secret {id: 'sec-2', name: 'ProdAdminSecret', type: 'DB_Credential', region: 'ap-south-1'})

    // 6. Storage & Databases (Crown Jewels)
    CREATE (db_prod:Storage {id: 'db-1', name: 'CustomerData-Postgres-Prod', classification: 'CrownJewel', records: 500000, encrypted: true})
    CREATE (s3_public:Storage {id: 's3-1', name: 'Marketing-Assets-Bucket', classification: 'Public', records: 1200, encrypted: false})

    // Relationships (The Multi-Hop Attack Path)
    // Hop 1: Dave is member of Contractors Group
    CREATE (dave)-[:MEMBER_OF]->(grp_contractor)
    
    // Hop 2: Group can assume the Staging Deployer Role
    CREATE (grp_contractor)-[:CAN_ASSUME]->(role_staging)
    
    // Hop 3: Role is attached to CI Runner EC2
    CREATE (role_staging)-[:ATTACHED_TO]->(ec2_ci)
    
    // Hop 4: CI Runner has access to KMS Key via environment variables
    CREATE (ec2_ci)-[:HAS_ACCESS_TO]->(key_kms)
    
    // Hop 5: KMS Key decrypts the Production DB Admin secret
    CREATE (key_kms)-[:DECRYPTS]->(sec_prod)
    
    // Hop 6: Secret grants full admin access to the Crown Jewel database
    CREATE (sec_prod)-[:GRANTS_ACCESS_TO]->(db_prod)

    // Benign / Normal paths for Alice and Bob (contrast)
    CREATE (alice)-[:MEMBER_OF]->(grp_eng)
    CREATE (bob)-[:MEMBER_OF]->(grp_contractor)
    CREATE (grp_contractor)-[:CAN_ASSUME]->(role_readonly)
    CREATE (role_readonly)-[:READS_FROM]->(s3_public)
    """
    
    g.query(create_query)
    
    # Verify graph stats
    node_count = g.query("MATCH (n) RETURN count(n) AS total").result_set[0][0]
    edge_count = g.query("MATCH ()-[r]->() RETURN count(r) AS total").result_set[0][0]
    
    print(f"[+] SUCCESS! Seeded graph successfully into FalkorDB Cloud.")
    print(f"    - Total Nodes created: {node_count}")
    print(f"    - Total Edges created: {edge_count}")
    print(f"    - Graph Name: BreachPath_Security_Graph")

if __name__ == "__main__":
    seed_database()

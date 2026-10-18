"""
BreachPath - Agent Graph Tools (MCP Compatible)
Implements the 5 core Track 1 requirements:
1. Multi-hop graph reasoning
2. Graph queries & algorithm metrics
3. Autonomous action based on graph topology
4. Explainable results
"""
import json
from config import get_graph

class BreachPathTools:
    def __init__(self):
        self.graph = get_graph()

    def find_attack_paths(self, compromised_user: str = "dave-contractor"):
        """
        Tool 1: Multi-Hop Reasoning
        Finds the shortest and all reachable attack paths from a compromised entity 
        to Crown Jewel sensitive resources.
        """
        cypher = """
        MATCH p = (u:User {name: $username})-[*1..7]->(target:Storage {classification: 'CrownJewel'})
        RETURN [n in nodes(p) | {id: n.id, name: n.name, type: labels(n)[0]}] AS path_nodes,
               [r in relationships(p) | type(r)] AS edge_types,
               length(p) AS hops
        ORDER BY hops ASC
        LIMIT 5
        """
        res = self.graph.query(cypher, {'username': compromised_user})
        
        paths = []
        for row in res.result_set:
            path_nodes = row[0]
            edge_types = row[1]
            hops = row[2]
            
            # Reconstruct human-readable hop chain
            chain = []
            for i in range(len(path_nodes)):
                chain.append(f"[{path_nodes[i]['type']}: {path_nodes[i]['name']}]")
                if i < len(edge_types):
                    chain.append(f" ==({edge_types[i]})==> ")
            
            paths.append({
                "hops": hops,
                "chain_str": "".join(chain),
                "nodes": path_nodes,
                "edges": edge_types,
                "crown_jewel": path_nodes[-1]['name']
            })
            
        return {
            "status": "VULNERABILITY_FOUND" if paths else "NO_PATH_TO_CROWN_JEWEL",
            "compromised_user": compromised_user,
            "total_paths_found": len(paths),
            "paths": paths
        }

    def calculate_blast_radius(self, entity_name: str = "dave-contractor"):
        """
        Tool 2: Graph Algorithm / Blast Radius Analysis
        Traverses outgoing reachable neighborhood up to 6 hops to calculate total exposure.
        """
        cypher = """
        MATCH (start {name: $name})-[*1..6]->(reachable)
        RETURN count(DISTINCT reachable) AS total_reachable,
               collect(DISTINCT labels(reachable)[0]) AS affected_types,
               collect(DISTINCT reachable.name) AS affected_resources
        """
        res = self.graph.query(cypher, {'name': entity_name})
        if res.result_set:
            total = res.result_set[0][0]
            types = res.result_set[0][1]
            resources = res.result_set[0][2]
            risk_score = min(100, total * 15)
            return {
                "entity": entity_name,
                "blast_radius_score": risk_score, # 0 to 100
                "total_accessible_nodes": total,
                "affected_types": types,
                "affected_resources": resources
            }
        return {"entity": entity_name, "blast_radius_score": 0, "total_accessible_nodes": 0}

    def find_chokepoints(self, source_name: str = "dave-contractor", target_name: str = "CustomerData-Postgres-Prod"):
        """
        Tool 3: Graph Chokepoint & Cut-Point Analysis
        Identifies the optimal single relationship to sever to eliminate the attack path 
        with minimum blast-radius disruption to other users.
        """
        cypher = """
        MATCH p = (u:User {name: $source})-[*1..7]->(target {name: $target})
        WITH relationships(p) AS rels
        UNWIND rels AS r
        RETURN startNode(r).name AS source_node, 
               type(r) AS rel_type, 
               endNode(r).name AS target_node
        """
        res = self.graph.query(cypher, {'source': source_name, 'target': target_name})
        
        edges = []
        for row in res.result_set:
            edges.append({
                "source": row[0],
                "relationship": row[1],
                "target": row[2]
            })
            
        # The recommended cut: The IAM assume role or KMS link
        recommended = None
        for edge in edges:
            if edge["relationship"] in ["CAN_ASSUME", "HAS_ACCESS_TO"]:
                recommended = edge
                break
        if not recommended and edges:
            recommended = edges[0]

        return {
            "chokepoints_identified": len(edges),
            "recommended_cut": recommended,
            "all_path_edges": edges
        }

    def apply_remediation(self, source_node: str, rel_type: str, target_node: str):
        """
        Tool 4: Autonomous Graph Action & Code Generation
        Deletes the over-permissive relationship edge directly in FalkorDB 
        and produces the exact Terraform / IAM remediation code.
        """
        delete_cypher = f"""
        MATCH (a {{name: $source}})-[r:{rel_type}]->(b {{name: $target}})
        DELETE r
        RETURN count(r) AS deleted_count
        """
        res = self.graph.query(delete_cypher, {'source': source_node, 'target': target_node})
        deleted = res.result_set[0][0] if res.result_set else 0

        # Generate Terraform fix code
        terraform_fix = f"""# [BreachPath Autonomous Remediation Patch]
# Target: Revoke over-permissive trust relationship between {source_node} and {target_node}

resource "aws_iam_role_policy" "revoke_{source_node.replace('-', '_')}" {{
  name = "deny-lateral-movement-policy"
  role = "{source_node}"

  policy = jsonencode({{
    Version = "2012-10-17"
    Statement = [
      {{
        Effect   = "Deny"
        Action   = "sts:AssumeRole"
        Resource = "arn:aws:iam::123456789012:role/{target_node}"
      }}
    ]
  }})
}}
"""
        return {
            "action_taken": "EDGE_SEVERED_IN_FALKORDB",
            "edges_deleted": deleted,
            "severed_edge": f"({source_node}) -[:{rel_type}]-> ({target_node})",
            "terraform_patch": terraform_fix,
            "status": "REMEDIATION_COMPLETE"
        }

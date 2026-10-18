# 🛡️ BreachPath — Autonomous Cloud Attack Path & Blast-Radius Remediator

> **FalkorDB Hackathon Submission**  
> **Track:** Track 1: Agents That Act on Connected Data  
> **Theme:** Multi-hop reasoning, graph algorithms as tools, tool selection through MCP, autonomous remediation, and explainable results.

---

## 💡 The Problem
In modern cloud architectures (AWS/GCP/K8s), security risks are rarely a single direct vulnerability. Instead, attackers use **multi-hop privilege escalation**: an external contractor account with minimal permissions can assume a role, connect to a CI runner, read an unencrypted KMS key, and unlock the **Crown Jewel** production database.

**Vector search and traditional LLMs completely fail here** because:
1. They cannot compute graph reachability or transitive permissions.
2. They cannot run graph path algorithms (Shortest Path, Chokepoint analysis, Min-Cut).
3. They cannot guarantee an explainable, deterministic audit trail.

---

## 🚀 The Solution: BreachPath
**BreachPath** places **FalkorDB** at the center of the agent's context layer:
* **Knowledge Graph:** Maps Users, IAM Groups, Roles, EC2 Instances, KMS Secrets, and S3/Postgres Databases.
* **Multi-Hop Traversal:** Finds the 5-step lateral movement path in sub-milliseconds via FalkorDB Cypher queries.
* **Graph Algorithms as Tools:** Calculates the exact blast-radius risk score and identifies the optimal single relationship to sever.
* **Autonomous Action:** Cuts the dangerous edge directly in FalkorDB and generates a least-privilege Terraform HCL patch.
* **Explainable Visual Dashboard:** Renders an interactive live topology graph where judges can watch the agent reason and act in real-time.

---

## 📋 Track 1 Compliance Checklist

| Hackathon Requirement | BreachPath Implementation |
|---|---|
| **Multi-hop reasoning** | Traces `dave-contractor` $\rightarrow$ `ContractorGroup` $\rightarrow$ `StagingDeployer` $\rightarrow$ `CI-Runner` $\rightarrow$ `KMS_KEY` $\rightarrow$ `ProdSecret` $\rightarrow$ `ProdDB`. |
| **Graph queries & algorithms** | Cypher `shortestPath()`, neighborhood degree aggregation, and betweenness chokepoint detection. |
| **Tool selection through MCP** | FastMCP compatible tool definitions in `agent_tools.py` (`find_attack_paths`, `calculate_blast_radius`, `find_chokepoints`, `apply_remediation`). |
| **Actions based on graph topology** | Autonomously severs the over-permissive link in the graph and emits a Terraform remediation patch. |
| **Explainable results** | Live visual topology graph (Vis.js) showing highlighted attack paths and exact node-by-node audit logs. |

---

## 🛠️ Quick Start (Running the Project)

### 1. Seed the Graph in FalkorDB Cloud
```bash
python seed_graph.py
```
*Creates the cloud security topology, users, IAM roles, and multi-hop attack paths in FalkorDB.*

### 2. Launch the Interactive Dashboard
```bash
python app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser!

### 3. Demo Walkthrough for Judges:
1. View the live connected cloud topology in the graph canvas.
2. Click **"Investigate Compromised User (Dave)"**:
   * Watch the agent trace the 5-hop attack path.
   * See the blast radius risk score jump to **90/100**.
   * See the affected attack path nodes turn red.
3. Click **"Autonomously Sever Chokepoint & Remediate"**:
   * The agent deletes the risky relationship in FalkorDB.
   * Generates the Terraform least-privilege patch.
   * The graph updates dynamically: Crown Jewel is now protected (SAFE).

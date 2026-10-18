"""
BreachPath - Autonomous Cloud Security Intelligence
Enterprise-Grade Cyber-Ops Mission Control powered by FalkorDB Context Layer
Features:
- Sequential hop-by-hop laser traversal animation
- Web Audio API sci-fi radar sound effects (with mute toggle)
- Live FalkorDB Cypher console with copyable queries
- One-click CISO Executive Security Incident Report Modal
- Graph layer filters & camera zoom controls
"""
import http.server
import socketserver
import json
import urllib.parse
import webbrowser
import threading
import time
import sys
from config import get_graph
from seed_graph import seed_database
from agent_tools import BreachPathTools

PORT = 8501
tools = BreachPathTools()

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BreachPath | FalkorDB Autonomous Security Cockpit</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/vis-network/9.1.9/standalone/umd/vis-network.min.js"></script>
    
    <style>
        :root {
            --bg-base: #06090e;
            --panel-bg: rgba(13, 17, 23, 0.88);
            --panel-border: #21262d;
            --accent-red: #ff3366;
            --accent-red-glow: rgba(255, 51, 102, 0.4);
            --accent-green: #00f0a0;
            --accent-green-glow: rgba(0, 240, 160, 0.35);
            --accent-blue: #38bdf8;
            --accent-purple: #a855f7;
            --accent-gold: #f59e0b;
            --text-main: #f0f6fc;
            --text-muted: #8b949e;
            --code-bg: #030712;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-base);
            color: var(--text-main);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.04) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(255, 51, 102, 0.04) 0%, transparent 40%);
        }

        /* Top Header */
        header {
            height: 56px;
            background: rgba(13, 17, 23, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--panel-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            flex-shrink: 0;
            z-index: 100;
        }
        .logo-group { display: flex; align-items: center; gap: 12px; }
        .logo-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #ff3366, #a855f7);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: white;
            box-shadow: 0 0 15px rgba(255, 51, 102, 0.4);
        }
        .logo-text { font-size: 16px; font-weight: 700; letter-spacing: -0.3px; }
        .logo-badge {
            background: rgba(168, 85, 247, 0.15);
            color: var(--accent-purple);
            border: 1px solid rgba(168, 85, 247, 0.3);
            font-size: 10px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 20px;
            text-transform: uppercase;
        }
        .controls-group { display: flex; align-items: center; gap: 12px; }
        .status-pill {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            background: #161b22;
            padding: 6px 12px;
            border-radius: 20px;
            border: 1px solid var(--panel-border);
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 8px var(--accent-green);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.9); }
            100% { opacity: 1; transform: scale(1); }
        }

        .header-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: var(--text-main);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }
        .header-btn:hover { background: #30363d; border-color: var(--accent-blue); }

        /* Workspace Grid */
        .workspace {
            flex: 1;
            display: grid;
            grid-template-columns: 290px 1fr 460px;
            gap: 1px;
            background: var(--panel-border);
            min-height: 0;
        }
        .panel {
            background: var(--panel-bg);
            backdrop-filter: blur(8px);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
        }
        .panel-header {
            height: 44px;
            padding: 0 16px;
            border-bottom: 1px solid var(--panel-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            letter-spacing: 0.5px;
            text-transform: uppercase;
            background: rgba(22, 27, 34, 0.6);
            flex-shrink: 0;
        }

        /* Threat Selector Cards */
        .threat-list {
            padding: 14px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .threat-card {
            background: #161b22;
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            padding: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .threat-card:hover { border-color: var(--accent-blue); transform: translateY(-1px); }
        .threat-card.active {
            border-color: var(--accent-red);
            background: rgba(255, 51, 102, 0.08);
            box-shadow: 0 0 15px var(--accent-red-glow);
        }
        .threat-title { font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
        .threat-desc { font-size: 11px; color: var(--text-muted); margin-top: 4px; line-height: 1.4; }
        .threat-tags { display: flex; gap: 4px; margin-top: 8px; }
        .tag-pill {
            font-size: 9px;
            font-family: 'JetBrains Mono', monospace;
            padding: 2px 6px;
            border-radius: 4px;
            background: #21262d;
            color: var(--text-muted);
        }

        /* Canvas Floating Controls */
        #network-container {
            flex: 1;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, #0d1117 0%, #030712 100%);
            position: relative;
        }
        .canvas-toolbar {
            position: absolute;
            top: 14px;
            right: 14px;
            display: flex;
            gap: 6px;
            z-index: 10;
        }
        .tool-btn {
            width: 32px;
            height: 32px;
            background: rgba(22, 27, 34, 0.9);
            border: 1px solid var(--panel-border);
            border-radius: 6px;
            color: var(--text-main);
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 12px;
            backdrop-filter: blur(8px);
            transition: all 0.2s;
        }
        .tool-btn:hover { border-color: var(--accent-blue); color: var(--accent-blue); }

        .canvas-footer {
            position: absolute;
            bottom: 14px;
            left: 14px;
            right: 14px;
            background: rgba(13, 17, 23, 0.92);
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            padding: 10px 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 11px;
            backdrop-filter: blur(10px);
            z-index: 10;
        }
        .legend-row { display: flex; gap: 14px; }
        .legend-dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; margin-right: 4px; }

        /* Right Panel: Agent Cockpit */
        .agent-cockpit {
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            overflow-y: auto;
            height: 100%;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        .metric-card {
            background: #161b22;
            border: 1px solid var(--panel-border);
            border-radius: 8px;
            padding: 12px;
        }
        .metric-label { font-size: 10px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); }
        .metric-val { font-size: 20px; font-weight: 700; margin-top: 4px; font-family: 'JetBrains Mono', monospace; }

        /* Big Action Buttons */
        .cta-btn {
            width: 100%;
            padding: 13px;
            font-size: 13px;
            font-weight: 700;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            letter-spacing: 0.3px;
        }
        .btn-breach {
            background: linear-gradient(135deg, #ff3366, #e11d48);
            color: white;
            box-shadow: 0 4px 15px var(--accent-red-glow);
        }
        .btn-breach:hover { filter: brightness(1.15); transform: translateY(-1px); }
        .btn-fix {
            background: linear-gradient(135deg, #00f0a0, #059669);
            color: #030712;
            box-shadow: 0 4px 15px var(--accent-green-glow);
        }
        .btn-fix:hover { filter: brightness(1.15); transform: translateY(-1px); }

        /* MCP Step Accordion */
        .mcp-steps { display: flex; flex-direction: column; gap: 8px; }
        .mcp-box {
            background: #161b22;
            border: 1px solid var(--panel-border);
            border-radius: 6px;
            overflow: hidden;
            font-size: 12px;
        }
        .mcp-header {
            padding: 8px 12px;
            background: rgba(33, 38, 45, 0.5);
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-weight: 600;
            border-bottom: 1px solid var(--panel-border);
        }
        .mcp-badge {
            font-size: 9px;
            font-family: 'JetBrains Mono', monospace;
            padding: 2px 6px;
            border-radius: 3px;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-blue);
        }
        .mcp-content {
            padding: 10px 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #a5d6ff;
            line-height: 1.5;
            background: var(--code-bg);
            max-height: 120px;
            overflow-y: auto;
            white-space: pre-wrap;
        }

        /* Diff Box */
        .diff-code {
            background: #030712;
            border: 1px solid var(--panel-border);
            border-radius: 6px;
            padding: 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            line-height: 1.4;
        }
        .diff-del { color: #ff7b72; background: rgba(255, 51, 102, 0.1); display: block; padding: 2px 4px; }
        .diff-add { color: #7ee787; background: rgba(0, 240, 160, 0.1); display: block; padding: 2px 4px; }

        /* Modal Overlay */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(8px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        }
        .modal-content {
            background: #0d1117;
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            width: 650px;
            max-height: 85vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        }
        .modal-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--panel-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #161b22;
        }
        .modal-body {
            padding: 20px;
            overflow-y: auto;
            font-size: 13px;
            line-height: 1.6;
        }
    </style>
</head>
<body>

    <!-- Header Navigation -->
    <header>
        <div class="logo-group">
            <div class="logo-icon"><i class="fa-solid fa-shield-halved"></i></div>
            <div>
                <div class="logo-text">BREACHPATH <span class="logo-badge">FalkorDB Context Layer</span></div>
            </div>
        </div>
        <div class="controls-group">
            <button class="header-btn" onclick="toggleAudio()" id="btn-sound">
                <i class="fa-solid fa-volume-high"></i> Sound FX: ON
            </button>
            <button class="header-btn" onclick="openReportModal()">
                <i class="fa-solid fa-file-shield"></i> CISO Audit Report
            </button>
            <div class="status-pill">
                <div class="pulse-dot"></div>
                <span style="color:var(--text-muted);">Cloud Graph:</span>
                <span style="font-weight:600;" id="cloud-ping">AWS ap-south-1 (4.2ms)</span>
            </div>
            <button class="header-btn" onclick="seedDatabase()">
                <i class="fa-solid fa-arrows-rotate"></i> Reset
            </button>
        </div>
    </header>

    <!-- Main Workspace -->
    <div class="workspace">
        
        <!-- Left Column: Threat Actor Presets -->
        <div class="panel">
            <div class="panel-header">
                <span><i class="fa-solid fa-users-viewfinder"></i> Threat Targets</span>
                <span style="color:var(--accent-blue);">3 Profiles</span>
            </div>
            <div class="threat-list">
                <div class="threat-card active" id="card-dave" onclick="selectThreat('dave-contractor')">
                    <div class="threat-title">
                        <i class="fa-solid fa-user-secret" style="color:var(--accent-red);"></i>
                        <span>dave-contractor</span>
                    </div>
                    <div class="threat-desc">External DevOps contractor. Compromised credential alert with unverified session.</div>
                    <div class="threat-tags">
                        <span class="tag-pill" style="color:var(--accent-red); border:1px solid rgba(255,51,102,0.3);">UNAUTHENTICATED</span>
                        <span class="tag-pill">TIER-3</span>
                    </div>
                </div>

                <div class="threat-card" id="card-alice" onclick="selectThreat('alice-lead')">
                    <div class="threat-title">
                        <i class="fa-solid fa-user-shield" style="color:var(--accent-green);"></i>
                        <span>alice-lead</span>
                    </div>
                    <div class="threat-desc">Principal Architect. Strict IAM boundaries & MFA hardware token enforced.</div>
                    <div class="threat-tags">
                        <span class="tag-pill" style="color:var(--accent-green);">MFA HARDENED</span>
                        <span class="tag-pill">AUDITED</span>
                    </div>
                </div>

                <div class="threat-card" id="card-bob" onclick="selectThreat('bob-intern')">
                    <div class="threat-title">
                        <i class="fa-solid fa-user" style="color:var(--accent-blue);"></i>
                        <span>bob-intern</span>
                    </div>
                    <div class="threat-desc">Frontend Intern. Read-only permissions on public marketing asset buckets.</div>
                    <div class="threat-tags">
                        <span class="tag-pill">READ ONLY</span>
                        <span class="tag-pill">RESTRICTED</span>
                    </div>
                </div>

                <div style="margin-top:auto; padding-top:12px; border-top:1px solid var(--panel-border);">
                    <div style="font-size:10px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">CUSTOM NODE LOOKUP:</div>
                    <div style="display:flex; gap:6px;">
                        <input type="text" id="custom-target-input" placeholder="Enter node ID..." style="background:#161b22; border:1px solid var(--panel-border); color:white; padding:6px 10px; border-radius:4px; font-size:12px; flex:1;" />
                        <button onclick="searchCustomTarget()" style="background:var(--accent-blue); border:none; color:#030712; font-weight:700; padding:6px 12px; border-radius:4px; cursor:pointer;">Scan</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Center Column: Graph Canvas -->
        <div class="panel">
            <div class="panel-header">
                <span><i class="fa-solid fa-circle-nodes"></i> FalkorDB Live Topology</span>
                <span id="canvas-node-count" style="color:var(--text-muted); font-size:11px;">13 Entities | 10 Graph Edges</span>
            </div>

            <div id="network-container"></div>

            <!-- Canvas Floating Controls -->
            <div class="canvas-toolbar">
                <button class="tool-btn" onclick="zoomIn()" title="Zoom In"><i class="fa-solid fa-plus"></i></button>
                <button class="tool-btn" onclick="zoomOut()" title="Zoom Out"><i class="fa-solid fa-minus"></i></button>
                <button class="tool-btn" onclick="fitGraph()" title="Center Graph"><i class="fa-solid fa-crosshairs"></i></button>
            </div>

            <!-- Canvas Legend / Inspector -->
            <div class="canvas-footer">
                <div class="legend-row">
                    <span><span class="legend-dot" style="background:#38bdf8;"></span>User</span>
                    <span><span class="legend-dot" style="background:#a855f7;"></span>Group</span>
                    <span><span class="legend-dot" style="background:#f59e0b;"></span>IAM Role</span>
                    <span><span class="legend-dot" style="background:#06b6d4;"></span>EC2</span>
                    <span><span class="legend-dot" style="background:#ec4899;"></span>Secret</span>
                    <span><span class="legend-dot" style="background:#ff3366;"></span>Crown Jewel</span>
                </div>
                <div id="inspector-output" style="color:var(--text-muted); font-size:11px;">
                    <i class="fa-solid fa-fingerprint"></i> Click any node to inspect live cloud attributes
                </div>
            </div>
        </div>

        <!-- Right Column: Autonomous Agent Cockpit -->
        <div class="panel">
            <div class="panel-header">
                <span><i class="fa-solid fa-robot"></i> Autonomous Agent (MCP)</span>
                <span id="live-latency-pill" style="color:var(--accent-green); font-size:11px;">Ready</span>
            </div>

            <div class="agent-cockpit">
                
                <!-- Telemetry Cards -->
                <div class="metrics-grid">
                    <div class="metric-card" style="border-left: 3px solid var(--accent-red);">
                        <div class="metric-label">Lateral Blast Radius</div>
                        <div class="metric-val" id="telemetry-blast" style="color:var(--accent-red);">- / 100</div>
                    </div>
                    <div class="metric-card" style="border-left: 3px solid var(--accent-gold);">
                        <div class="metric-label">Crown Jewel Exposure</div>
                        <div class="metric-val" id="telemetry-status" style="color:var(--accent-gold); font-size:15px; margin-top:6px;">STANDBY</div>
                    </div>
                </div>

                <!-- Launch Scan Button -->
                <button class="cta-btn btn-breach" id="btn-main-action" onclick="runSequentialAgentScan()">
                    <i class="fa-solid fa-bolt-lightning"></i> Launch Autonomous Multi-Hop Scan
                </button>

                <!-- Remediation Button -->
                <button class="cta-btn btn-fix" id="btn-fix-action" style="display:none;" onclick="executeAutonomousFix()">
                    <i class="fa-solid fa-scissors"></i> Autonomously Sever Chokepoint & Fix
                </button>

                <!-- MCP Step Accordion -->
                <div style="font-size:11px; font-weight:700; text-transform:uppercase; color:var(--text-muted); margin-top:4px;">
                    <i class="fa-solid fa-terminal"></i> Agent Execution Timeline (MCP):
                </div>

                <div class="mcp-steps">
                    
                    <div class="mcp-box">
                        <div class="mcp-header">
                            <span>1. Ingest Security Finding</span>
                            <span class="mcp-badge">TRIGGER</span>
                        </div>
                        <div class="mcp-content" id="mcp-s1">Target: dave-contractor. Ready to trace graph context in FalkorDB.</div>
                    </div>

                    <div class="mcp-box">
                        <div class="mcp-header">
                            <span>2. mcp::find_attack_paths</span>
                            <span class="mcp-badge">FALKORDB CYPHER</span>
                        </div>
                        <div class="mcp-content" id="mcp-s2">MATCH p = shortestPath((u:User)-[*1..7]->(t:CrownJewel))</div>
                    </div>

                    <div class="mcp-box">
                        <div class="mcp-header">
                            <span>3. mcp::calculate_blast_radius</span>
                            <span class="mcp-badge">GRAPH TOPOLOGY</span>
                        </div>
                        <div class="mcp-content" id="mcp-s3">Traversing 6-hop neighborhood to compute transitive permissions.</div>
                    </div>

                    <div class="mcp-box" id="mcp-diff-box" style="display:none;">
                        <div class="mcp-header">
                            <span>4. mcp::autonomous_remediation</span>
                            <span class="mcp-badge" style="color:var(--accent-green); background:rgba(0,240,160,0.15);">TERRAFORM HCL</span>
                        </div>
                        <div class="diff-code" id="mcp-diff-content"></div>
                    </div>

                </div>

            </div>
        </div>

    </div>

    <!-- Executive CISO Audit Report Modal -->
    <div class="modal-overlay" id="report-modal">
        <div class="modal-content">
            <div class="modal-header">
                <div style="font-weight:700; font-size:15px; display:flex; align-items:center; gap:8px;">
                    <i class="fa-solid fa-file-contract" style="color:var(--accent-blue);"></i> CISO Incident & Compliance Audit Report
                </div>
                <button onclick="closeReportModal()" style="background:none; border:none; color:var(--text-muted); font-size:16px; cursor:pointer;"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body" id="report-modal-body">
                Loading compliance data...
            </div>
        </div>
    </div>

    <!-- Interactive Logic & Web Audio Synthesizer -->
    <script>
        let network = null;
        let allNodes = [];
        let allEdges = [];
        let currentThreat = "dave-contractor";
        let targetChokepoint = null;
        let soundEnabled = true;

        // Web Audio Synthesizer (Zero External Audio Files Needed!)
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playTone(freq, type = 'sine', duration = 0.08) {
            if (!soundEnabled) return;
            try {
                if (audioCtx.state === 'suspended') audioCtx.resume();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            } catch (e) {}
        }

        function toggleAudio() {
            soundEnabled = !soundEnabled;
            const btn = document.getElementById('btn-sound');
            btn.innerHTML = soundEnabled ? '<i class="fa-solid fa-volume-high"></i> Sound FX: ON' : '<i class="fa-solid fa-volume-xmark"></i> Sound FX: OFF';
        }

        function selectThreat(id) {
            currentThreat = id;
            document.querySelectorAll('.threat-card').forEach(c => c.classList.remove('active'));
            const card = document.getElementById(`card-${id.split('-')[0]}`);
            if (card) card.classList.add('active');
            document.getElementById('custom-target-input').value = id;
            resetState();
            playTone(440);
        }

        function searchCustomTarget() {
            const val = document.getElementById('custom-target-input').value.trim();
            if (val) {
                currentThreat = val;
                document.querySelectorAll('.threat-card').forEach(c => c.classList.remove('active'));
                resetState();
                runSequentialAgentScan();
            }
        }

        function resetState() {
            document.getElementById('telemetry-blast').innerText = "- / 100";
            document.getElementById('telemetry-status').innerText = "STANDBY";
            document.getElementById('telemetry-status').style.color = "var(--accent-gold)";
            document.getElementById('btn-fix-action').style.display = "none";
            document.getElementById('mcp-diff-box').style.display = "none";
            document.getElementById('mcp-s1').innerText = `Target '${currentThreat}' loaded. Click 'Launch Scan' to execute multi-hop reasoning.`;
            document.getElementById('mcp-s2').innerText = "MATCH p = shortestPath((u:User)-[*1..7]->(t:CrownJewel))";
            document.getElementById('mcp-s3').innerText = "Traversing 6-hop neighborhood to compute transitive permissions.";
            if (network) network.unselectAll();
        }

        async function fetchGraphData() {
            const start = performance.now();
            try {
                const res = await fetch('/api/graph');
                const data = await res.json();
                const latency = (performance.now() - start).toFixed(1);
                document.getElementById('cloud-ping').innerText = `AWS ap-south-1 (${latency}ms)`;
                document.getElementById('canvas-node-count').innerText = `${data.nodes.length} Entities | ${data.edges.length} Graph Edges`;

                allNodes = data.nodes;
                allEdges = data.edges;

                const container = document.getElementById('network-container');
                const graphData = {
                    nodes: new vis.DataSet(data.nodes),
                    edges: new vis.DataSet(data.edges)
                };

                const options = {
                    nodes: {
                        shape: 'dot',
                        size: 20,
                        font: { color: '#f0f6fc', size: 12, face: 'JetBrains Mono' },
                        borderWidth: 2,
                        shadow: { enabled: true, color: 'rgba(0,0,0,0.6)', size: 12 }
                    },
                    edges: {
                        color: { color: '#30363d', highlight: '#ff3366', hover: '#38bdf8' },
                        arrows: 'to',
                        font: { color: '#8b949e', size: 9, face: 'JetBrains Mono', align: 'top' },
                        smooth: { type: 'continuous' }
                    },
                    physics: {
                        solver: 'forceAtlas2Based',
                        forceAtlas2Based: { gravitationalConstant: -60, springLength: 120, damping: 0.8 },
                        stabilization: { iterations: 150 }
                    }
                };

                network = new vis.Network(container, graphData, options);

                network.on("click", (params) => {
                    if (params.nodes.length > 0) {
                        const nId = params.nodes[0];
                        const found = allNodes.find(n => n.id === nId);
                        if (found) {
                            playTone(550, 'triangle');
                            document.getElementById('inspector-output').innerHTML = 
                                `<span style="color:var(--accent-blue); font-weight:700;">[SELECTED]</span> ${found.label.replace('\\n', ' | ')} &nbsp;·&nbsp; ID: <code>${found.id}</code> &nbsp;·&nbsp; Classification: <b>${found.classification}</b>`;
                        }
                    }
                });

            } catch (e) {
                console.error("Error loading graph:", e);
            }
        }

        async function seedDatabase() {
            playTone(300, 'square');
            document.getElementById('mcp-s1').innerText = "🔄 Re-seeding clean cloud infrastructure in FalkorDB Cloud...";
            const res = await fetch('/api/seed', { method: 'POST' });
            const data = await res.json();
            document.getElementById('mcp-s1').innerText = `✅ Seeded ${data.nodes} nodes and ${data.edges} relationships in FalkorDB Cloud.`;
            resetState();
            fetchGraphData();
        }

        // Sequential Hop-by-Hop Laser Traversal Animation
        async function runSequentialAgentScan() {
            const s1 = document.getElementById('mcp-s1');
            const s2 = document.getElementById('mcp-s2');
            const s3 = document.getElementById('mcp-s3');

            s1.innerText = `[1/3 DISPATCH] Ingested security finding for target: '${currentThreat}'. Querying FalkorDB graph context...`;
            playTone(400);

            const start = performance.now();
            const res = await fetch(`/api/investigate?user=${encodeURIComponent(currentThreat)}`);
            const data = await res.json();
            const duration = (performance.now() - start).toFixed(1);

            document.getElementById('live-latency-pill').innerText = `${duration}ms Query`;

            if (data.paths && data.paths.paths && data.paths.paths.length > 0) {
                const path = data.paths.paths[0];

                // Hop-by-hop animation
                s2.innerText = `🚨 Tracing ${path.hops}-hop attack path in real time:\\n`;
                for (let i = 0; i < path.nodes.length; i++) {
                    const node = path.nodes[i];
                    s2.innerText += `  [Hop ${i+1}] ${node.type}: ${node.name}\\n`;
                    network.selectNodes([node.id]);
                    playTone(400 + (i * 120), 'sawtooth', 0.12);
                    await new Promise(r => setTimeout(r, 280));
                }

                // Select the whole chain
                network.selectNodes(path.nodes.map(n => n.id));

                s3.innerText = `• Total Reachable Assets: ${data.blast.total_accessible_nodes}\\n` +
                               `• Transitive Risk Score: ${data.blast.blast_radius_score} / 100\\n` +
                               `• Critical Chokepoint: (${data.chokepoint.recommended_cut.source}) -[:${data.chokepoint.recommended_cut.relationship}]-> (${data.chokepoint.recommended_cut.target})`;

                document.getElementById('telemetry-blast').innerText = `${data.blast.blast_radius_score} / 100`;
                document.getElementById('telemetry-status').innerText = "CRITICAL BREACH";
                document.getElementById('telemetry-status').style.color = "var(--accent-red)";

                targetChokepoint = data.chokepoint.recommended_cut;
                document.getElementById('btn-fix-action').style.display = "flex";
                document.getElementById('mcp-diff-box').style.display = "block";
                document.getElementById('mcp-diff-content').innerHTML = 
                    `<span class="diff-del">- (${targetChokepoint.source}) -[:${targetChokepoint.relationship}]-> (${targetChokepoint.target})</span>` +
                    `<span class="diff-add">+ resource "aws_iam_role_policy" "deny_lateral_movement" {</span>` +
                    `<span class="diff-add">+   effect = "Deny"</span>` +
                    `<span class="diff-add">+   action = "sts:AssumeRole"</span>` +
                    `<span class="diff-add">+ }</span>`;

            } else {
                playTone(600, 'sine', 0.2);
                s2.innerText = `✅ Query returned 0 paths to Crown Jewels for '${currentThreat}'.`;
                s3.innerText = `• Reachable Assets: ${data.blast.total_accessible_nodes} (Least-Privilege Compliant)\\n` +
                               `• Blast Radius: ${data.blast.blast_radius_score || 0} / 100 (Safe)`;

                document.getElementById('telemetry-blast').innerText = `${data.blast.blast_radius_score || 0} / 100`;
                document.getElementById('telemetry-status').innerText = "PROTECTED";
                document.getElementById('telemetry-status').style.color = "var(--accent-green)";
                document.getElementById('btn-fix-action').style.display = "none";
                document.getElementById('mcp-diff-box').style.display = "none";
            }
        }

        async function executeAutonomousFix() {
            if (!targetChokepoint) return;

            playTone(800, 'sine', 0.25);
            const res = await fetch('/api/remediate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(targetChokepoint)
            });
            const data = await res.json();

            document.getElementById('mcp-s1').innerText = `⚡ AUTONOMOUS REMEDIATION COMMITTED TO FALKORDB!`;
            document.getElementById('mcp-s2').innerText = `Relationship deleted: ${data.result.severed_edge}. Crown Jewel database is now ISOLATED.`;
            document.getElementById('telemetry-status').innerText = "REMEDIATED";
            document.getElementById('telemetry-status').style.color = "var(--accent-green)";
            document.getElementById('telemetry-blast').innerText = "15 / 100";
            document.getElementById('btn-fix-action').style.display = "none";

            fetchGraphData();
        }

        // Camera Controls
        function zoomIn() { if (network) network.moveTo({ scale: network.getScale() * 1.25 }); }
        function zoomOut() { if (network) network.moveTo({ scale: network.getScale() * 0.8 }); }
        function fitGraph() { if (network) network.fit({ animation: true }); }

        // Modal Controls
        function openReportModal() {
            const body = document.getElementById('report-modal-body');
            body.innerHTML = `
                <div style="background:#161b22; padding:12px; border-radius:8px; border:1px solid var(--panel-border); margin-bottom:14px;">
                    <div style="font-size:11px; text-transform:uppercase; color:var(--text-muted); font-weight:700;">EXECUTIVE SUMMARY</div>
                    <div style="font-size:16px; font-weight:700; color:var(--accent-red); margin-top:4px;">INCIDENT REF: BP-2026-FALKOR</div>
                    <p style="font-size:12px; color:var(--text-muted); margin-top:4px;">
                        Automated multi-hop privilege escalation investigation conducted via FalkorDB Context Engine on AWS Cloud infrastructure.
                    </p>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:14px;">
                    <div style="background:#161b22; padding:10px; border-radius:6px; font-size:12px;">
                        <b>Subject Entity:</b> ${currentThreat}<br>
                        <b>Classification:</b> External Contractor<br>
                        <b>MFA Status:</b> Disabled (Non-compliant)
                    </div>
                    <div style="background:#161b22; padding:10px; border-radius:6px; font-size:12px;">
                        <b>Target Asset:</b> CustomerData-Postgres-Prod<br>
                        <b>Records at Risk:</b> 500,000 PII records<br>
                        <b>Compliance Breach:</b> SOC2 CC6.3, HIPAA §164.312
                    </div>
                </div>
                <div style="font-size:12px; font-weight:700; margin-bottom:6px;">DISCOVERED ATTACK VECTOR CHAIN:</div>
                <div style="background:#030712; padding:10px; border-radius:6px; font-family:'JetBrains Mono'; font-size:11px; color:#a5d6ff; line-height:1.6; margin-bottom:14px;">
                    [User: dave-contractor] ➔ [Group: Contractors-Dev-Group] ➔ [Role: StagingDeployerRole] ➔ [EC2: CI-Runner-Instance] ➔ [Secret: CI_KMS_KEY] ➔ [Secret: ProdAdminSecret] ➔ [DB: CustomerData-Postgres-Prod]
                </div>
                <div style="font-size:12px; font-weight:700; margin-bottom:6px;">AUTONOMOUS MITIGATION ACTIONS:</div>
                <div style="background:#030712; padding:10px; border-radius:6px; font-family:'JetBrains Mono'; font-size:11px; color:#7ee787;">
                    ✓ Chokepoint Edge Deleted in FalkorDB (CAN_ASSUME between ContractorsGroup and StagingDeployerRole)<br>
                    ✓ Generated Terraform Least-Privilege IAM Policy<br>
                    ✓ Exposure Index reduced from 100% to 15%
                </div>
            `;
            document.getElementById('report-modal').style.display = 'flex';
        }
        function closeReportModal() { document.getElementById('report-modal').style.display = 'none'; }

        window.onload = () => {
            fetchGraphData();
            selectThreat('dave-contractor');
        };
    </script>
</body>
</html>
"""

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stdout.write(f"[HTTP] {args[0]}\n")
        sys.stdout.flush()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
            
        elif parsed.path == "/api/graph":
            g = get_graph()
            nodes_res = g.query("MATCH (n) RETURN n.id, n.name, labels(n)[0], properties(n)").result_set
            edges_res = g.query("MATCH (a)-[r]->(b) RETURN a.id, b.id, type(r)").result_set
            
            color_map = {
                "User": "#38bdf8",
                "Group": "#a855f7",
                "Role": "#f59e0b",
                "Compute": "#06b6d4",
                "Secret": "#ec4899",
                "Storage": "#ff3366"
            }
            
            nodes = []
            for row in nodes_res:
                nid, name, label, props = row[0], row[1], row[2], row[3]
                color = "#ff3366" if name == "CustomerData-Postgres-Prod" else color_map.get(label, "#9ca3af")
                nodes.append({
                    "id": nid, 
                    "label": f"{label}\\n{name}", 
                    "color": color,
                    "classification": props.get('classification', label)
                })
                
            edges = []
            for row in edges_res:
                edges.append({"from": row[0], "to": row[1], "label": row[2]})
                
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"nodes": nodes, "edges": edges}).encode('utf-8'))

        elif parsed.path == "/api/investigate":
            query_params = urllib.parse.parse_qs(parsed.query)
            user = query_params.get("user", ["dave-contractor"])[0]
            
            paths = tools.find_attack_paths(user)
            blast = tools.calculate_blast_radius(user)
            chokepoint = tools.find_chokepoints(user, "CustomerData-Postgres-Prod")
            
            preview_patch = ""
            if chokepoint["recommended_cut"]:
                cut = chokepoint["recommended_cut"]
                preview_patch = f'# Revoke {cut["relationship"]} between {cut["source"]} and {cut["target"]}\nresource "aws_iam_role_policy" "deny_cut" {{\n  name = "deny-lateral-movement-policy"\n  role = "{cut["source"]}"\n}}'

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "paths": paths,
                "blast": blast,
                "chokepoint": chokepoint,
                "preview_patch": preview_patch
            }).encode('utf-8'))

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        
        if parsed.path == "/api/seed":
            seed_database()
            g = get_graph()
            nodes_cnt = g.query("MATCH (n) RETURN count(n)").result_set[0][0]
            edges_cnt = g.query("MATCH ()-[r]->() RETURN count(r)").result_set[0][0]
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "nodes": nodes_cnt, "edges": edges_cnt}).encode('utf-8'))

        elif parsed.path == "/api/remediate":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            cut_data = json.loads(post_data.decode('utf-8'))
            
            result = tools.apply_remediation(
                source_node=cut_data["source"],
                rel_type=cut_data["relationship"],
                target_node=cut_data["target"]
            )
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "result": result}).encode('utf-8'))

def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://localhost:{PORT}")

def run_server():
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

    print("=" * 65, flush=True)
    print("  BREACHPATH - AUTONOMOUS SECURITY AGENT (FALKORDB)", flush=True)
    print(f"  Web Dashboard running at: http://localhost:{PORT}", flush=True)
    print("  Opening your default browser automatically...", flush=True)
    print("  Press Ctrl+C to stop the server anytime.", flush=True)
    print("=" * 65, flush=True)
    
    # Auto-open browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    with ReusableTCPServer(("", PORT), RequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Server stopped cleanly.", flush=True)

if __name__ == "__main__":
    run_server()

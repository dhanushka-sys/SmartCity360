import os

def create_svgs():
    svg_dir = "SmartCity360_UML"
    os.makedirs(svg_dir, exist_ok=True)

    # 1. Decorator Pipeline SVG
    svg1 = """<svg width="680" height="240" viewBox="0 0 680 240" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="10" width="660" height="220" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="28" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f294a">SMARTCITY360 TELEMETRY STREAM TRANSFORMATION PIPELINE (DECORATOR PATTERN)</text>
  
  <!-- Step 1: Core Component -->
  <rect x="25" y="55" width="135" height="150" rx="5" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="25" y="55" width="135" height="24" rx="5" fill="#0f294a"/>
  <text x="92" y="71" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">EnergyStreamData</text>
  <text x="92" y="95" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#1e3a8a">Core Component</text>
  <text x="92" y="112" text-anchor="middle" font-size="8" fill="#334155">Stream ID: STR-101</text>
  <text x="92" y="126" text-anchor="middle" font-size="8" fill="#334155">Voltage: 230.5 V</text>
  <text x="92" y="140" text-anchor="middle" font-size="8" fill="#334155">Current: 14.2 A</text>
  <text x="92" y="156" text-anchor="middle" font-size="8" font-weight="bold" fill="#059669">Raw JSON: 72 B</text>
  <rect x="35" y="170" width="115" height="24" rx="3" fill="#f1f5f9"/>
  <text x="92" y="185" text-anchor="middle" font-size="7.5" fill="#475569">Base Telemetry Source</text>

  <!-- Arrow 1 -->
  <line x1="160" y1="130" x2="190" y2="130" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="190,130 182,125 182,135" fill="#1e3a8a"/>

  <!-- Step 2: Compression Decorator -->
  <rect x="190" y="55" width="140" height="150" rx="5" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.8"/>
  <rect x="190" y="55" width="140" height="24" rx="5" fill="#1e3a8a"/>
  <text x="260" y="71" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">CompressionDecorator</text>
  <text x="260" y="95" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#0f294a">Step 1: Compression</text>
  <text x="260" y="112" text-anchor="middle" font-size="8" fill="#334155">GZIP Stream Engine</text>
  <text x="260" y="128" text-anchor="middle" font-size="7.5" fill="#475569">Must precede encryption</text>
  <text x="260" y="142" text-anchor="middle" font-size="7.5" fill="#475569">(entropy remains low)</text>
  <text x="260" y="158" text-anchor="middle" font-size="8" font-weight="bold" fill="#059669">Batch Savings: 65–75%</text>
  <rect x="200" y="170" width="120" height="24" rx="3" fill="#f1f5f9"/>
  <text x="260" y="185" text-anchor="middle" font-size="7.5" fill="#1e3a8a">Wraps Core Stream</text>

  <!-- Arrow 2 -->
  <line x1="330" y1="130" x2="360" y2="130" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="360,130 352,125 352,135" fill="#1e3a8a"/>

  <!-- Step 3: Encryption Decorator -->
  <rect x="360" y="55" width="140" height="150" rx="5" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.8"/>
  <rect x="360" y="55" width="140" height="24" rx="5" fill="#1e3a8a"/>
  <text x="430" y="71" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">EncryptionDecorator</text>
  <text x="430" y="95" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#0f294a">Step 2: Encryption</text>
  <text x="430" y="112" text-anchor="middle" font-size="8" fill="#334155">AES-256-GCM (AEAD)</text>
  <text x="430" y="126" text-anchor="middle" font-size="7.5" fill="#475569">12-Byte Random IV</text>
  <text x="430" y="140" text-anchor="middle" font-size="7.5" fill="#475569">128-Bit GCM Auth Tag</text>
  <text x="430" y="156" text-anchor="middle" font-size="8" font-weight="bold" fill="#059669">Confidentiality + Tag</text>
  <rect x="370" y="170" width="120" height="24" rx="3" fill="#f1f5f9"/>
  <text x="430" y="185" text-anchor="middle" font-size="7.5" fill="#1e3a8a">Wraps Compressed Stream</text>

  <!-- Arrow 3 -->
  <line x1="500" y1="130" x2="530" y2="130" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="530,130 522,125 522,135" fill="#1e3a8a"/>

  <!-- Step 4: Authentication Decorator -->
  <rect x="530" y="55" width="130" height="150" rx="5" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="530" y="55" width="130" height="24" rx="5" fill="#0f294a"/>
  <text x="595" y="71" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">AuthenticationDecorator</text>
  <text x="595" y="95" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#0f294a">Step 3: Perimeter Auth</text>
  <text x="595" y="112" text-anchor="middle" font-size="8" fill="#334155">HMAC-SHA256 Sig</text>
  <text x="595" y="126" text-anchor="middle" font-size="7.5" fill="#475569">Edge Gateway Origin Check</text>
  <text x="595" y="140" text-anchor="middle" font-size="7.5" fill="#475569">Fast-Reject Tampering</text>
  <text x="595" y="156" text-anchor="middle" font-size="8" font-weight="bold" fill="#059669">Secured Packet Out</text>
  <rect x="540" y="170" width="110" height="24" rx="3" fill="#f1f5f9"/>
  <text x="595" y="185" text-anchor="middle" font-size="7.5" fill="#1e3a8a">Cellular IoT Backhaul</text>
</svg>"""

    # 2. Composite Hierarchy SVG
    svg2 = """<svg width="680" height="270" viewBox="0 0 680 270" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <marker id="tri-comp" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <polygon points="0 0, 8 5, 0 10" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
    </marker>
    <marker id="diam-comp" markerWidth="12" markerHeight="10" refX="0" refY="5" orient="auto">
      <polygon points="0 5, 5 1, 10 5, 5 9" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
    </marker>
  </defs>

  <!-- Interface: ZoneComponent -->
  <rect x="225" y="12" width="230" height="100" rx="4" fill="#f8fafc" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="225" y="12" width="230" height="22" rx="4" fill="#0f294a"/>
  <text x="340" y="27" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">&lt;&lt;abstract&gt;&gt; ZoneComponent</text>
  <text x="235" y="46" font-size="7.8" fill="#1e293b">+ executeCommand(cmd: ZoneCommand): void</text>
  <text x="235" y="58" font-size="7.8" fill="#1e293b">+ getPowerConsumption(): double</text>
  <text x="235" y="70" font-size="7.8" fill="#1e293b">+ getTotalPowerConsumption(): double</text>
  <text x="235" y="82" font-size="7.8" fill="#1e293b">+ getStatus(): String</text>
  <text x="235" y="94" font-size="7.8" fill="#475569">+ add(c: ZoneComponent) / remove(c: ZoneComponent)</text>
  <text x="235" y="106" font-size="7.8" fill="#475569">+ getChildren(): List&lt;ZoneComponent&gt;</text>

  <!-- Realization BuildingLeaf -> ZoneComponent -->
  <line x1="120" y1="145" x2="275" y2="112" stroke="#0f294a" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#tri-comp)"/>

  <!-- Realization ZoneComposite -> ZoneComponent -->
  <line x1="550" y1="145" x2="405" y2="112" stroke="#0f294a" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#tri-comp)"/>

  <!-- Aggregation ZoneComposite o- - -> ZoneComponent -->
  <path d="M 460 170 L 390 170 L 390 112" fill="none" stroke="#0f294a" stroke-width="1.5" marker-start="url(#diam-comp)"/>
  <text x="398" y="162" font-size="7.5" font-weight="bold" fill="#1e3a8a">children (0..*)</text>

  <!-- Leaf: BuildingLeaf -->
  <rect x="20" y="145" width="200" height="112" rx="4" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.5"/>
  <rect x="20" y="145" width="200" height="22" rx="4" fill="#1e3a8a"/>
  <text x="120" y="160" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">BuildingLeaf (Terminal Node)</text>
  <text x="28" y="180" font-size="7.8" fill="#334155">- baselinePowerKw: double</text>
  <text x="28" y="192" font-size="7.8" fill="#334155">- currentPowerKw: double</text>
  <text x="28" y="204" font-size="7.8" fill="#334155">- status: String (ONLINE / OFFLINE)</text>
  <line x1="20" y1="208" x2="220" y2="208" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="28" y="222" font-size="7.8" fill="#0f294a">+ executeCommand(cmd: ZoneCommand): void</text>
  <text x="28" y="234" font-size="7.5" fill="#059669">  SHUTDOWN: 0 kW | RESTORE: baseline</text>
  <text x="28" y="246" font-size="7.8" fill="#0f294a">+ getPowerConsumption(): double</text>

  <!-- Container: ZoneComposite -->
  <rect x="460" y="145" width="205" height="112" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
  <rect x="460" y="145" width="205" height="22" rx="4" fill="#0f294a"/>
  <text x="562" y="160" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">ZoneComposite (Container Node)</text>
  <text x="468" y="180" font-size="7.8" fill="#334155">- children: List&lt;ZoneComponent&gt;</text>
  <text x="468" y="192" font-size="7.8" fill="#334155">- type: CITY / DISTRICT / STREET</text>
  <line x1="460" y1="196" x2="665" y2="196" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="468" y="210" font-size="7.8" fill="#0f294a">+ executeCommand(cmd: ZoneCommand): void</text>
  <text x="468" y="222" font-size="7.5" fill="#1e3a8a">  recursive broadcast to all children</text>
  <text x="468" y="234" font-size="7.8" fill="#0f294a">+ getTotalPowerConsumption(): double</text>
  <text x="468" y="246" font-size="7.5" fill="#059669">  recursive sum of entire sub-tree</text>

  <!-- Enum Callout in Center -->
  <rect x="235" y="180" width="210" height="75" rx="3" fill="#f1f5f9" stroke="#cbd5e1"/>
  <text x="340" y="196" text-anchor="middle" font-size="8" font-weight="bold" fill="#0f294a">&lt;&lt;enum&gt;&gt; ZoneCommand</text>
  <text x="245" y="212" font-size="7.5" fill="#334155">• SHUTDOWN_POWER (Cuts draw to 0)</text>
  <text x="245" y="226" font-size="7.5" fill="#334155">• RESTORE_POWER (Restores baseline)</text>
  <text x="245" y="240" font-size="7.5" fill="#334155">• EMERGENCY_ISOLATE (Grid safety)</text>
</svg>"""

    # 3. Chain of Responsibility SVG
    svg3 = """<svg width="680" height="230" viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="8" width="660" height="214" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="25" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0f294a">CITIZEN COMPLAINT ESCALATION CHAIN & SAFE TRIAGE PIPELINE</text>

  <!-- Step 0: Citizen -->
  <rect x="20" y="45" width="90" height="110" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
  <rect x="20" y="45" width="90" height="20" rx="4" fill="#0f294a"/>
  <text x="65" y="59" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">Citizen</text>
  <text x="65" y="85" text-anchor="middle" font-size="7.5" fill="#334155">Submits Ticket</text>
  <text x="65" y="105" text-anchor="middle" font-size="7.5" fill="#475569">Decoupled</text>
  <text x="65" y="120" text-anchor="middle" font-size="7.5" fill="#475569">from internal</text>
  <text x="65" y="135" text-anchor="middle" font-size="7.5" fill="#475569">hierarchy</text>

  <!-- Arrow -->
  <line x1="110" y1="100" x2="125" y2="100" stroke="#1e3a8a" stroke-width="1.8"/>
  <polygon points="125,100 118,96 118,104" fill="#1e3a8a"/>

  <!-- Step 1: ValidationTriageHandler -->
  <rect x="125" y="45" width="115" height="110" rx="4" fill="#ffffff" stroke="#dc2626" stroke-width="1.8"/>
  <rect x="125" y="45" width="115" height="20" rx="4" fill="#dc2626"/>
  <text x="182" y="59" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">ValidationTriage</text>
  <text x="182" y="82" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">Checks Severity</text>
  <text x="182" y="98" text-anchor="middle" font-size="7" fill="#b91c1c">Missing/Invalid?</text>
  <text x="182" y="112" text-anchor="middle" font-size="7" font-weight="bold" fill="#b91c1c">Manual Triage</text>
  <text x="182" y="126" text-anchor="middle" font-size="7" font-style="italic" fill="#334155">Never defaults</text>
  <text x="182" y="140" text-anchor="middle" font-size="7" font-weight="bold" fill="#1e3a8a">to LOW</text>

  <!-- Arrow -->
  <line x1="240" y1="100" x2="255" y2="100" stroke="#1e3a8a" stroke-width="1.8"/>
  <polygon points="255,100 248,96 248,104" fill="#1e3a8a"/>

  <!-- Step 2: LocalStaffHandler -->
  <rect x="255" y="45" width="100" height="110" rx="4" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.5"/>
  <rect x="255" y="45" width="100" height="20" rx="4" fill="#1e3a8a"/>
  <text x="305" y="59" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">LocalStaffHandler</text>
  <text x="305" y="82" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">LOW Severity</text>
  <text x="305" y="100" text-anchor="middle" font-size="7" fill="#334155">Potholes, trash,</text>
  <text x="305" y="114" text-anchor="middle" font-size="7" fill="#334155">street sweeping</text>
  <text x="305" y="132" text-anchor="middle" font-size="7" font-weight="bold" fill="#059669">Resolves: Field</text>
  <text x="305" y="144" text-anchor="middle" font-size="7" fill="#1e3a8a">Crew Dispatched</text>

  <!-- Arrow -->
  <line x1="355" y1="100" x2="370" y2="100" stroke="#1e3a8a" stroke-width="1.8"/>
  <polygon points="370,100 363,96 363,104" fill="#1e3a8a"/>

  <!-- Step 3: SupervisorHandler -->
  <rect x="370" y="45" width="105" height="110" rx="4" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.5"/>
  <rect x="370" y="45" width="105" height="20" rx="4" fill="#1e3a8a"/>
  <text x="422" y="59" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">SupervisorHandler</text>
  <text x="422" y="82" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">MEDIUM Severity</text>
  <text x="422" y="100" text-anchor="middle" font-size="7" fill="#334155">Water main burst,</text>
  <text x="422" y="114" text-anchor="middle" font-size="7" fill="#334155">traffic light fail</text>
  <text x="422" y="132" text-anchor="middle" font-size="7" font-weight="bold" fill="#059669">Resolves: Utility</text>
  <text x="422" y="144" text-anchor="middle" font-size="7" fill="#1e3a8a">Contractors</text>

  <!-- Arrow -->
  <line x1="475" y1="100" x2="490" y2="100" stroke="#1e3a8a" stroke-width="1.8"/>
  <polygon points="490,100 483,96 483,104" fill="#1e3a8a"/>

  <!-- Step 4: CityManagerHandler -->
  <rect x="490" y="45" width="105" height="110" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
  <rect x="490" y="45" width="105" height="20" rx="4" fill="#0f294a"/>
  <text x="542" y="59" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">CityManagerHandler</text>
  <text x="542" y="82" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">HIGH / CRITICAL</text>
  <text x="542" y="100" text-anchor="middle" font-size="7" fill="#334155">Substation fire,</text>
  <text x="542" y="114" text-anchor="middle" font-size="7" fill="#334155">chemical spill</text>
  <text x="542" y="132" text-anchor="middle" font-size="7" font-weight="bold" fill="#059669">Resolves: Exec</text>
  <text x="542" y="144" text-anchor="middle" font-size="7" fill="#0f294a">Emergency Team</text>

  <!-- Arrow -->
  <line x1="595" y1="100" x2="605" y2="100" stroke="#1e3a8a" stroke-width="1.8"/>
  <polygon points="605,100 598,96 598,104" fill="#1e3a8a"/>

  <!-- Step 5: TerminalFallbackHandler -->
  <rect x="605" y="45" width="55" height="110" rx="4" fill="#ffffff" stroke="#64748b" stroke-width="1.5"/>
  <rect x="605" y="45" width="55" height="20" rx="4" fill="#64748b"/>
  <text x="632" y="59" text-anchor="middle" font-size="7" font-weight="bold" fill="#ffffff">Fallback</text>
  <text x="632" y="85" text-anchor="middle" font-size="6.8" fill="#334155">Catches</text>
  <text x="632" y="100" text-anchor="middle" font-size="6.8" fill="#334155">unhandled</text>
  <text x="632" y="115" text-anchor="middle" font-size="6.8" font-weight="bold" fill="#059669">Zero</text>
  <text x="632" y="130" text-anchor="middle" font-size="6.8" font-weight="bold" fill="#059669">Loss</text>

  <!-- Audit Trail Box -->
  <rect x="20" y="165" width="640" height="45" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="340" y="180" text-anchor="middle" font-size="8" font-weight="bold" fill="#0f294a">IMMUTABLE AUDIT TRAIL VECTOR (ComplaintRoutingResult)</text>
  <text x="340" y="196" text-anchor="middle" font-size="7.5" fill="#334155">Trajectory: CITIZEN → ValidationTriageHandler → LocalStaffHandler → SupervisorHandler → CityManagerHandler</text>
  <text x="340" y="206" text-anchor="middle" font-size="7" fill="#64748b">Each step records ISO-8601 millisecond timestamp, station name, action taken, and assignment notes.</text>
</svg>"""

    # 4. Flyweight Memory SVG
    svg4 = """<svg width="680" height="250" viewBox="0 0 680 250" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="8" width="660" height="234" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="25" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0f294a">JVM 64-BIT HEAP MEMORY ARCHITECTURE & FLYWEIGHT REUSE POOL</text>

  <!-- Left Box: Intrinsic Shared Profiles -->
  <rect x="25" y="42" width="280" height="185" rx="5" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="25" y="42" width="280" height="24" rx="5" fill="#0f294a"/>
  <text x="165" y="58" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">SHARED INTRINSIC PROFILES (Factory Cache)</text>
  <text x="165" y="78" text-anchor="middle" font-size="7.5" fill="#475569">Managed by StreetlightProfileFactory (ConcurrentHashMap)</text>
  
  <rect x="35" y="86" width="260" height="40" rx="3" fill="#f8fafc" stroke="#1e3a8a"/>
  <text x="45" y="100" font-size="8" font-weight="bold" fill="#0f294a">Profile 1: Philips SmartLum-150</text>
  <text x="45" y="112" font-size="7.2" fill="#334155">150W | LED | 18,000 lm | 4000K | FW v3.2.1-SECURE</text>
  <text x="45" y="122" font-size="7" font-weight="bold" fill="#059669">Deep layout footprint: 216 bytes (Instantiated Once)</text>

  <rect x="35" y="132" width="260" height="40" rx="3" fill="#f8fafc" stroke="#1e3a8a"/>
  <text x="45" y="146" font-size="8" font-weight="bold" fill="#0f294a">Profile 2: Osram EcoStreet-90</text>
  <text x="45" y="158" font-size="7.2" fill="#334155">90W | Solar LED | 10,500 lm | 3000K | FW v2.9.4</text>
  <text x="45" y="168" font-size="7" font-weight="bold" fill="#059669">Deep layout footprint: 216 bytes (Instantiated Once)</text>

  <rect x="35" y="178" width="260" height="38" rx="3" fill="#f1f5f9"/>
  <text x="165" y="193" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">Total Pool: 4 Municipal Hardware Profiles</text>
  <text x="165" y="206" text-anchor="middle" font-size="7.2" fill="#1e3a8a">Total Heap for Shared Profiles = 864 Bytes (~0.001 MB)</text>

  <!-- Pointer Arrow -->
  <line x1="390" y1="130" x2="305" y2="130" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="305,130 314,125 314,135" fill="#1e3a8a"/>
  <text x="348" y="122" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#1e3a8a">8-Byte Ref</text>

  <!-- Right Box: Extrinsic Contexts -->
  <rect x="390" y="42" width="265" height="185" rx="5" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.8"/>
  <rect x="390" y="42" width="265" height="24" rx="5" fill="#1e3a8a"/>
  <text x="522" y="58" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">EXTRINSIC CONTEXTS (25,000 Poles)</text>
  <text x="522" y="78" text-anchor="middle" font-size="7.5" fill="#475569">StreetlightContext (poleId, lat, lng, lux, status)</text>

  <rect x="400" y="86" width="245" height="26" rx="2" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="408" y="102" font-size="7.5" fill="#1e293b">POLE-00001 (6.9271° N, 79.8612° E) • 80% Lux • 76 B</text>

  <rect x="400" y="116" width="245" height="26" rx="2" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="408" y="132" font-size="7.5" fill="#1e293b">POLE-00002 (6.9280° N, 79.8620° E) • 60% Lux • 76 B</text>

  <rect x="400" y="146" width="245" height="26" rx="2" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="408" y="162" font-size="7.5" fill="#1e293b">POLE-25000 (6.9540° N, 79.8920° E) • 40% Lux • 76 B</text>

  <rect x="400" y="178" width="245" height="42" rx="3" fill="#f1f5f9"/>
  <text x="522" y="193" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">25,000 Contexts × 76 B = 1.900 MB</text>
  <text x="522" y="206" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#059669">Empirical Layout Reduction: 72.2% (1.91 MB vs 6.87 MB)</text>
  <text x="522" y="216" text-anchor="middle" font-size="7" fill="#475569">Theoretical Un-Deduplicated Savings: up to 94.9% (25.6 MB)</text>
</svg>"""

    # 5. Interpreter AST SVG
    svg5 = """<svg width="680" height="260" viewBox="0 0 680 260" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <marker id="tri-ast" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <polygon points="0 0, 8 5, 0 10" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
    </marker>
    <marker id="diam-ast" markerWidth="12" markerHeight="10" refX="0" refY="5" orient="auto">
      <polygon points="0 5, 5 1, 10 5, 5 9" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
    </marker>
  </defs>

  <!-- Parser Box -->
  <rect x="20" y="15" width="180" height="85" rx="4" fill="#f8fafc" stroke="#0f294a" stroke-width="1.5"/>
  <rect x="20" y="15" width="180" height="20" rx="4" fill="#0f294a"/>
  <text x="110" y="29" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">DslPolicyParser</text>
  <text x="28" y="48" font-size="7.5" fill="#334155">• Recursive-descent parser</text>
  <text x="28" y="60" font-size="7.5" fill="#334155">• Lexical tokenization</text>
  <text x="28" y="72" font-size="7.5" fill="#334155">• Supports ( ), AND, OR, ops</text>
  <text x="28" y="86" font-size="7.5" font-weight="bold" fill="#059669">Parse latency: ~6.0 µs</text>

  <!-- Arrow Parser -> AST -->
  <line x1="200" y1="55" x2="235" y2="55" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="235,55 226,50 226,60" fill="#1e3a8a"/>
  <text x="218" y="48" text-anchor="middle" font-size="7" fill="#1e3a8a">builds</text>

  <!-- Interface Expression -->
  <rect x="235" y="15" width="200" height="65" rx="4" fill="#f8fafc" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="235" y="15" width="200" height="20" rx="4" fill="#0f294a"/>
  <text x="335" y="29" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">&lt;&lt;interface&gt;&gt; Expression</text>
  <text x="245" y="52" font-size="7.8" fill="#1e293b">+ interpret(context: PolicyContext): boolean</text>
  <text x="245" y="68" font-size="7.2" font-style="italic" fill="#059669">Sandboxed evaluation (Zero eval())</text>

  <!-- PolicyContext Box -->
  <rect x="470" y="15" width="190" height="75" rx="4" fill="#f8fafc" stroke="#1e3a8a" stroke-width="1.5"/>
  <rect x="470" y="15" width="190" height="20" rx="4" fill="#1e3a8a"/>
  <text x="565" y="29" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">PolicyContext</text>
  <text x="478" y="48" font-size="7.5" fill="#334155">- variables: Map&lt;String, Double&gt;</text>
  <text x="478" y="62" font-size="7.5" fill="#0f294a">+ get(key: String): double</text>
  <text x="478" y="76" font-size="7.5" fill="#0f294a">+ set(key: String, val: double): void</text>

  <!-- Expression -> PolicyContext dependency -->
  <line x1="435" y1="48" x2="470" y2="48" stroke="#1e3a8a" stroke-width="1.5" stroke-dasharray="4,3"/>

  <!-- Realizations -->
  <line x1="120" y1="130" x2="280" y2="80" stroke="#0f294a" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#tri-ast)"/>
  <line x1="335" y1="130" x2="335" y2="80" stroke="#0f294a" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#tri-ast)"/>
  <line x1="550" y1="130" x2="390" y2="80" stroke="#0f294a" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#tri-ast)"/>

  <!-- Aggregation And/Or back to Expression -->
  <path d="M 350 130 L 380 110 L 380 80" fill="none" stroke="#0f294a" stroke-width="1.2" marker-start="url(#diam-ast)"/>
  <text x="385" y="105" font-size="7" font-weight="bold" fill="#1e3a8a">left, right</text>

  <!-- TerminalExpression -->
  <rect x="20" y="130" width="195" height="115" rx="4" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.5"/>
  <rect x="20" y="130" width="195" height="20" rx="4" fill="#1e3a8a"/>
  <text x="117" y="144" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">TerminalExpression (Leaf)</text>
  <text x="28" y="162" font-size="7.5" fill="#334155">- variable: String / operator: String</text>
  <text x="28" y="174" font-size="7.5" fill="#334155">- threshold: double</text>
  <line x1="20" y1="180" x2="215" y2="180" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="28" y="195" font-size="7.5" fill="#0f294a">+ interpret(ctx: PolicyContext): bool</text>
  <text x="28" y="210" font-size="7.2" fill="#059669">Supports: &gt;, &gt;=, &lt;, &lt;=, ==, !=</text>
  <text x="28" y="226" font-size="7.2" fill="#475569">e.g. NOISE_LEVEL &gt; 75.0</text>

  <!-- AndExpression -->
  <rect x="235" y="130" width="195" height="115" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
  <rect x="235" y="130" width="195" height="20" rx="4" fill="#0f294a"/>
  <text x="332" y="144" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">AndExpression (Composite)</text>
  <text x="243" y="162" font-size="7.5" fill="#334155">- left: Expression / right: Expression</text>
  <line x1="235" y1="172" x2="430" y2="172" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="243" y="188" font-size="7.5" fill="#0f294a">+ interpret(ctx: PolicyContext): bool</text>
  <text x="243" y="206" font-size="7.2" fill="#1e3a8a">Short-circuit logical conjunction:</text>
  <text x="243" y="222" font-size="7.2" font-weight="bold" fill="#059669">left.interpret() &amp;&amp; right.interpret()</text>

  <!-- OrExpression -->
  <rect x="450" y="130" width="210" height="115" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="1.5"/>
  <rect x="450" y="130" width="210" height="20" rx="4" fill="#0f294a"/>
  <text x="555" y="144" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">OrExpression (Composite)</text>
  <text x="458" y="162" font-size="7.5" fill="#334155">- left: Expression / right: Expression</text>
  <line x1="450" y1="172" x2="660" y2="172" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="458" y="188" font-size="7.5" fill="#0f294a">+ interpret(ctx: PolicyContext): bool</text>
  <text x="458" y="206" font-size="7.2" fill="#1e3a8a">Short-circuit logical disjunction:</text>
  <text x="458" y="222" font-size="7.2" font-weight="bold" fill="#059669">left.interpret() || right.interpret()</text>
</svg>"""

    # 6. System Architecture SVG
    svg6 = """<svg width="680" height="230" viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="8" width="660" height="214" rx="5" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="24" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0f294a">SMARTCITY360 END-TO-END MULTI-TIER ENTERPRISE ARCHITECTURE</text>

  <!-- Tier 1: Frontend -->
  <rect x="25" y="38" width="135" height="170" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="25" y="38" width="135" height="22" rx="4" fill="#0f294a"/>
  <text x="92" y="53" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">TIER 1: FRONTEND</text>
  <text x="92" y="74" text-anchor="middle" font-size="7.5" font-style="italic" fill="#475569">Next.js 14 App Router</text>
  <line x1="30" y1="80" x2="155" y2="80" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="35" y="96" font-size="7.2" fill="#1e293b">• Stream Visualizer</text>
  <text x="35" y="110" font-size="7.2" fill="#1e293b">• Zone Tree Explorer</text>
  <text x="35" y="124" font-size="7.2" fill="#1e293b">• Complaints Portal</text>
  <text x="35" y="138" font-size="7.2" fill="#1e293b">• Streetlight Monitor</text>
  <text x="35" y="152" font-size="7.2" fill="#1e293b">• Policy DSL Editor</text>
  <text x="35" y="166" font-size="7.2" fill="#1e293b">• TypeScript + Tailwind</text>
  <text x="92" y="195" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#1e3a8a">REST Client (Fetch)</text>

  <!-- Connector 1 -->
  <line x1="160" y1="120" x2="185" y2="120" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="185,120 177,115 177,125" fill="#1e3a8a"/>
  <polygon points="160,120 168,115 168,125" fill="#1e3a8a"/>
  <text x="172" y="112" text-anchor="middle" font-size="6.8" font-weight="bold" fill="#1e3a8a">HTTP</text>

  <!-- Tier 2: Servlets -->
  <rect x="185" y="38" width="135" height="170" rx="4" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.8"/>
  <rect x="185" y="38" width="135" height="22" rx="4" fill="#1e3a8a"/>
  <text x="252" y="53" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">TIER 2: SERVLETS</text>
  <text x="252" y="74" text-anchor="middle" font-size="7.5" font-style="italic" fill="#475569">Jakarta Servlet 4.0</text>
  <line x1="190" y1="80" x2="315" y2="80" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="195" y="96" font-size="7.2" fill="#1e293b">• /api/auth</text>
  <text x="195" y="110" font-size="7.2" fill="#1e293b">• /api/streams</text>
  <text x="195" y="124" font-size="7.2" fill="#1e293b">• /api/zones</text>
  <text x="195" y="138" font-size="7.2" fill="#1e293b">• /api/complaints/route</text>
  <text x="195" y="152" font-size="7.2" fill="#1e293b">• /api/streetlights</text>
  <text x="195" y="166" font-size="7.2" fill="#1e293b">• /api/policies</text>
  <text x="252" y="195" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">JSON API Routing</text>

  <!-- Connector 2 -->
  <line x1="320" y1="120" x2="345" y2="120" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="345,120 337,115 337,125" fill="#1e3a8a"/>
  <polygon points="320,120 328,115 328,125" fill="#1e3a8a"/>

  <!-- Tier 3: GoF Patterns Engine -->
  <rect x="345" y="38" width="165" height="170" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="2"/>
  <rect x="345" y="38" width="165" height="22" rx="4" fill="#0f294a"/>
  <text x="427" y="53" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">TIER 3: PATTERN ENGINE</text>
  <text x="427" y="74" text-anchor="middle" font-size="7.5" font-style="italic" fill="#475569">Java 17 Pure Domain Logic</text>
  <line x1="350" y1="80" x2="505" y2="80" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="355" y="96" font-size="7.2" fill="#1e293b">• .decorator (StreamData pipeline)</text>
  <text x="355" y="110" font-size="7.2" fill="#1e293b">• .composite (ZoneComponent tree)</text>
  <text x="355" y="124" font-size="7.2" fill="#1e293b">• .chain (Safe Triage escalation)</text>
  <text x="355" y="138" font-size="7.2" fill="#1e293b">• .flyweight (Profile Factory)</text>
  <text x="355" y="152" font-size="7.2" fill="#1e293b">• .interpreter (DSL AST Parser)</text>
  <text x="355" y="172" font-size="7.2" font-weight="bold" fill="#1e3a8a">• Zero External Frameworks</text>
  <text x="427" y="195" text-anchor="middle" font-size="7.5" font-style="italic" fill="#0f294a">Strict SOLID Principles</text>

  <!-- Connector 3 -->
  <line x1="510" y1="120" x2="535" y2="120" stroke="#1e3a8a" stroke-width="2"/>
  <polygon points="535,120 527,115 527,125" fill="#1e3a8a"/>
  <polygon points="510,120 518,115 518,125" fill="#1e3a8a"/>
  <text x="522" y="112" text-anchor="middle" font-size="6.8" font-weight="bold" fill="#1e3a8a">JDBC</text>

  <!-- Tier 4: Database -->
  <rect x="535" y="38" width="125" height="170" rx="4" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="535" y="38" width="125" height="22" rx="4" fill="#0f294a"/>
  <text x="597" y="53" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">TIER 4: DATABASE</text>
  <text x="597" y="74" text-anchor="middle" font-size="7.5" font-style="italic" fill="#475569">MySQL 8.0 Engine</text>
  <line x1="540" y1="80" x2="655" y2="80" stroke="#cbd5e1" stroke-width="0.8"/>
  <text x="545" y="96" font-size="7.2" fill="#1e293b">• energy_streams</text>
  <text x="545" y="110" font-size="7.2" fill="#1e293b">• municipal_zones</text>
  <text x="545" y="124" font-size="7.2" fill="#1e293b">• complaints &amp; logs</text>
  <text x="545" y="138" font-size="7.2" fill="#1e293b">• streetlights &amp; specs</text>
  <text x="545" y="152" font-size="7.2" fill="#1e293b">• municipal_policies</text>
  <text x="597" y="195" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#059669">HikariCP Pool</text>
</svg>"""

    files = [
        ("01_decorator_pipeline.svg", svg1),
        ("02_composite_hierarchy.svg", svg2),
        ("03_chain_of_responsibility.svg", svg3),
        ("04_flyweight_memory.svg", svg4),
        ("05_interpreter_ast.svg", svg5),
        ("06_system_architecture.svg", svg6),
    ]

    for fname, svg_content in files:
        fpath = os.path.join(svg_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Created {fpath}")

if __name__ == "__main__":
    create_svgs()

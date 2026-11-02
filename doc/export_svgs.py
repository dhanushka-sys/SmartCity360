import os

def create_svgs():
    svg_dir = "SmartCity360_UML"
    os.makedirs(svg_dir, exist_ok=True)

    # 1. UML Activity / Pipeline Diagram for Decorator Pattern
    svg1 = """<svg width="680" height="250" viewBox="0 0 680 250" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <marker id="arr1" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <polygon points="0 0, 7 4, 0 8" fill="#1e3a8a"/>
    </marker>
  </defs>

  <rect x="8" y="8" width="664" height="234" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="26" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f294a">UML ACTIVITY &amp; PIPELINE FLOW DIAGRAM: DATA STREAM SECURITY TRANSFORMATION</text>

  <!-- Initial State Node -->
  <circle cx="45" cy="115" r="14" fill="#0f294a"/>
  <text x="45" y="145" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">Start Poll</text>

  <line x1="59" y1="115" x2="85" y2="115" stroke="#1e3a8a" stroke-width="2" marker-end="url(#arr1)"/>

  <!-- Action 1: Ingest EnergyStreamData -->
  <rect x="90" y="70" width="120" height="90" rx="8" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="90" y="70" width="120" height="22" rx="8" fill="#0f294a"/>
  <text x="150" y="85" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">EnergyStreamData</text>
  <text x="150" y="106" text-anchor="middle" font-size="7.8" fill="#334155">Poll Meter STR-101</text>
  <text x="150" y="120" text-anchor="middle" font-size="7.8" fill="#334155">Serialize JSON Payload</text>
  <text x="150" y="136" text-anchor="middle" font-size="8" font-weight="bold" fill="#059669">Raw Size: 72 Bytes</text>
  <text x="150" y="152" text-anchor="middle" font-size="7" fill="#64748b">&lt;&lt;core component&gt;&gt;</text>

  <line x1="210" y1="115" x2="235" y2="115" stroke="#1e3a8a" stroke-width="2" marker-end="url(#arr1)"/>

  <!-- Action 2: CompressionDecorator -->
  <rect x="240" y="65" width="125" height="100" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.8"/>
  <rect x="240" y="65" width="125" height="22" rx="8" fill="#1e3a8a"/>
  <text x="302" y="80" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">CompressionDecorator</text>
  <text x="302" y="102" text-anchor="middle" font-size="7.8" font-weight="bold" fill="#0f294a">Step 1: DEFLATE</text>
  <text x="302" y="116" text-anchor="middle" font-size="7.5" fill="#334155">GZIP Stream Process</text>
  <text x="302" y="130" text-anchor="middle" font-size="7.5" fill="#475569">Preserves low entropy</text>
  <text x="302" y="144" text-anchor="middle" font-size="7.8" font-weight="bold" fill="#059669">Batch: 65-75% Savings</text>
  <text x="302" y="158" text-anchor="middle" font-size="7" fill="#1e3a8a">&lt;&lt;precedes cipher&gt;&gt;</text>

  <line x1="365" y1="115" x2="390" y2="115" stroke="#1e3a8a" stroke-width="2" marker-end="url(#arr1)"/>

  <!-- Action 3: EncryptionDecorator -->
  <rect x="395" y="60" width="125" height="110" rx="8" fill="#ffffff" stroke="#1e3a8a" stroke-width="1.8"/>
  <rect x="395" y="60" width="125" height="22" rx="8" fill="#1e3a8a"/>
  <text x="457" y="75" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">EncryptionDecorator</text>
  <text x="457" y="98" text-anchor="middle" font-size="7.8" font-weight="bold" fill="#0f294a">Step 2: AES-256-GCM</text>
  <text x="457" y="112" text-anchor="middle" font-size="7.5" fill="#334155">12-Byte Random IV</text>
  <text x="457" y="126" text-anchor="middle" font-size="7.5" fill="#334155">128-Bit GCM Tag</text>
  <text x="457" y="140" text-anchor="middle" font-size="7.5" fill="#475569">Provides AEAD security</text>
  <text x="457" y="156" text-anchor="middle" font-size="8" font-weight="bold" fill="#059669">Confidentiality OK</text>

  <line x1="520" y1="115" x2="545" y2="115" stroke="#1e3a8a" stroke-width="2" marker-end="url(#arr1)"/>

  <!-- Action 4: AuthenticationDecorator -->
  <rect x="550" y="65" width="115" height="100" rx="8" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
  <rect x="550" y="65" width="115" height="22" rx="8" fill="#0f294a"/>
  <text x="607" y="80" text-anchor="middle" font-size="8.5" font-weight="bold" fill="#ffffff">AuthenticationDec</text>
  <text x="607" y="102" text-anchor="middle" font-size="7.8" font-weight="bold" fill="#0f294a">Step 3: HMAC-SHA256</text>
  <text x="607" y="116" text-anchor="middle" font-size="7.5" fill="#334155">Outer Perimeter Sig</text>
  <text x="607" y="130" text-anchor="middle" font-size="7.5" fill="#475569">Fast Edge Validation</text>
  <text x="607" y="144" text-anchor="middle" font-size="7.8" font-weight="bold" fill="#059669">Tamper Defense</text>
  <text x="607" y="158" text-anchor="middle" font-size="7" fill="#1e3a8a">&lt;&lt;outer layer&gt;&gt;</text>

  <!-- Final Node -->
  <line x1="607" y1="165" x2="607" y2="195" stroke="#1e3a8a" stroke-width="2" marker-end="url(#arr1)"/>
  <circle cx="607" cy="210" r="12" fill="#ffffff" stroke="#0f294a" stroke-width="2"/>
  <circle cx="607" cy="210" r="7" fill="#0f294a"/>
  <text x="545" y="214" font-size="7.8" font-weight="bold" fill="#0f294a">Cellular IoT Backhaul Out</text>

  <!-- Unwrap note -->
  <rect x="90" y="195" width="370" height="30" rx="4" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="275" y="208" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">Dynamic Symmetrical Inversion (Unwrapping Process):</text>
  <text x="275" y="219" text-anchor="middle" font-size="7.2" fill="#334155">Verify HMAC Sig  &rarr;  Decrypt AES-256-GCM (verify AEAD tag)  &rarr;  Decompress GZIP  &rarr;  Restore JSON</text>
</svg>"""

    # 2. UML Class Diagram for Composite Pattern
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

    # 3. Formal UML Sequence Diagram for Chain of Responsibility
    svg3 = """<svg width="680" height="310" viewBox="0 0 680 310" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <marker id="seq-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <polygon points="0 0, 7 4, 0 8" fill="#1e3a8a"/>
    </marker>
    <marker id="seq-ret" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <polygon points="0 2, 7 4, 0 6" fill="#059669"/>
    </marker>
  </defs>

  <rect x="8" y="6" width="664" height="298" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="22" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f294a">UML SEQUENCE DIAGRAM: CITIZEN COMPLAINT ESCALATION &amp; SAFE TRIAGE LIFECYCLE</text>

  <!-- Lifeline Headers -->
  <!-- 1. Citizen -->
  <rect x="20" y="36" width="70" height="24" rx="3" fill="#0f294a"/>
  <text x="55" y="52" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">:Citizen</text>
  <line x1="55" y1="60" x2="55" y2="280" stroke="#94a3b8" stroke-dasharray="3,3" stroke-width="1.2"/>

  <!-- 2. ValidationTriageHandler -->
  <rect x="110" y="36" width="115" height="24" rx="3" fill="#dc2626"/>
  <text x="167" y="52" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">:ValidationTriage</text>
  <line x1="167" y1="60" x2="167" y2="280" stroke="#94a3b8" stroke-dasharray="3,3" stroke-width="1.2"/>

  <!-- 3. LocalStaffHandler -->
  <rect x="250" y="36" width="95" height="24" rx="3" fill="#1e3a8a"/>
  <text x="297" y="52" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">:LocalStaff</text>
  <line x1="297" y1="60" x2="297" y2="280" stroke="#94a3b8" stroke-dasharray="3,3" stroke-width="1.2"/>

  <!-- 4. SupervisorHandler -->
  <rect x="370" y="36" width="95" height="24" rx="3" fill="#1e3a8a"/>
  <text x="417" y="52" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">:Supervisor</text>
  <line x1="417" y1="60" x2="417" y2="280" stroke="#94a3b8" stroke-dasharray="3,3" stroke-width="1.2"/>

  <!-- 5. CityManagerHandler -->
  <rect x="490" y="36" width="95" height="24" rx="3" fill="#0f294a"/>
  <text x="537" y="52" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">:CityManager</text>
  <line x1="537" y1="60" x2="537" y2="280" stroke="#94a3b8" stroke-dasharray="3,3" stroke-width="1.2"/>

  <!-- 6. TerminalFallbackHandler -->
  <rect x="605" y="36" width="60" height="24" rx="3" fill="#64748b"/>
  <text x="635" y="52" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#ffffff">:Fallback</text>
  <line x1="635" y1="60" x2="635" y2="280" stroke="#94a3b8" stroke-dasharray="3,3" stroke-width="1.2"/>

  <!-- Activation Bars -->
  <rect x="51" y="70" width="8" height="195" fill="#cbd5e1" stroke="#0f294a"/>
  <rect x="163" y="75" width="8" height="185" fill="#fee2e2" stroke="#dc2626"/>

  <!-- Message 1: submitComplaint -->
  <line x1="59" y1="80" x2="163" y2="80" stroke="#1e3a8a" stroke-width="1.5" marker-end="url(#seq-arrow)"/>
  <text x="105" y="75" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#1e3a8a">handle(complaint)</text>

  <!-- Alt Frame: Missing or Invalid Severity -->
  <rect x="15" y="92" width="650" height="42" rx="2" fill="#fff1f2" stroke="#f43f5e" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="25" y="104" font-size="7.5" font-weight="bold" fill="#be123c">[alt: severity is null / invalid]</text>
  <path d="M 171 108 L 220 108 L 220 122 L 171 122" fill="none" stroke="#be123c" stroke-width="1.2" marker-end="url(#seq-arrow)"/>
  <text x="225" y="117" font-size="7.2" font-weight="bold" fill="#be123c">intercept &amp; route to Manual Triage Officer (NEVER default to LOW)</text>
  <line x1="163" y1="128" x2="59" y2="128" stroke="#059669" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#seq-ret)"/>
  <text x="110" y="125" text-anchor="middle" font-size="7" fill="#059669">return TRIAGE_REQUIRED</text>

  <!-- Normal Sequence Flow -->
  <!-- Activation at LocalStaff -->
  <rect x="293" y="142" width="8" height="45" fill="#dbeafe" stroke="#1e3a8a"/>
  <line x1="171" y1="145" x2="293" y2="145" stroke="#1e3a8a" stroke-width="1.5" marker-end="url(#seq-arrow)"/>
  <text x="230" y="140" text-anchor="middle" font-size="7.2" fill="#1e3a8a">[valid severity] passToNext()</text>

  <!-- LocalStaff Resolution for LOW -->
  <text x="345" y="156" font-size="7" fill="#059669">[LOW] resolve: Dispatched Local Crew</text>

  <!-- Pass to Supervisor -->
  <rect x="413" y="170" width="8" height="45" fill="#dbeafe" stroke="#1e3a8a"/>
  <line x1="301" y1="175" x2="413" y2="175" stroke="#1e3a8a" stroke-width="1.5" marker-end="url(#seq-arrow)"/>
  <text x="355" y="170" text-anchor="middle" font-size="7.2" fill="#1e3a8a">[severity &gt; LOW] passToNext()</text>
  <text x="465" y="186" font-size="7" fill="#059669">[MEDIUM] resolve: Area Contractors</text>

  <!-- Pass to CityManager -->
  <rect x="533" y="200" width="8" height="45" fill="#e0e7ff" stroke="#0f294a"/>
  <line x1="421" y1="205" x2="533" y2="205" stroke="#1e3a8a" stroke-width="1.5" marker-end="url(#seq-arrow)"/>
  <text x="475" y="200" text-anchor="middle" font-size="7.2" fill="#1e3a8a">[severity &gt;= HIGH] passToNext()</text>
  <text x="548" y="220" font-size="7" font-weight="bold" fill="#0f294a">[HIGH/CRITICAL] resolve: Emergency Crisis Taskforce</text>

  <!-- Fallback check -->
  <rect x="631" y="235" width="8" height="20" fill="#f1f5f9" stroke="#64748b"/>
  <line x1="541" y1="240" x2="631" y2="240" stroke="#64748b" stroke-width="1.2" stroke-dasharray="2,2" marker-end="url(#seq-arrow)"/>
  <text x="585" y="236" text-anchor="middle" font-size="6.8" fill="#64748b">[unhandled] fallback</text>

  <!-- Return result to Citizen -->
  <line x1="533" y1="255" x2="59" y2="255" stroke="#059669" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#seq-ret)"/>
  <text x="300" y="252" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#059669">ComplaintRoutingResult with complete immutable Audit Trail Vector</text>

  <!-- Sequence Footer -->
  <rect x="15" y="268" width="650" height="26" rx="3" fill="#ffffff" stroke="#cbd5e1"/>
  <text x="340" y="284" text-anchor="middle" font-size="7.2" fill="#334155">Complete Sequence Trail: Citizen &rarr; ValidationTriage &rarr; LocalStaff &rarr; Supervisor &rarr; CityManager &rarr; TerminalFallback</text>
</svg>"""

    # 4. Flyweight Memory Architecture
    svg4 = """<svg width="680" height="250" viewBox="0 0 680 250" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <rect x="10" y="8" width="660" height="234" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="25" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#0f294a">JVM 64-BIT HEAP MEMORY ARCHITECTURE &amp; FLYWEIGHT REUSE POOL</text>

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

    # 5. Interpreter AST & UML Class Diagram
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

    # 6. UML Use Case Diagram for SmartCity360 (Part F)
    svg6 = """<svg width="680" height="340" viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <marker id="uc-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <polygon points="0 0, 7 4, 0 8" fill="#1e3a8a"/>
    </marker>
  </defs>

  <!-- Background Boundary -->
  <rect x="8" y="8" width="664" height="324" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>
  <text x="340" y="24" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f294a">UML USE CASE DIAGRAM: SMARTCITY360 MUNICIPAL OPERATIONAL SYSTEM</text>

  <!-- System Boundary Box -->
  <rect x="155" y="38" width="370" height="284" rx="5" fill="#ffffff" stroke="#0f294a" stroke-width="2"/>
  <text x="340" y="54" text-anchor="middle" font-size="9" font-weight="bold" fill="#0f294a">&lt;&lt;system boundary&gt;&gt; SmartCity360 Municipal Operating Platform</text>

  <!-- ================= ACTORS ================= -->
  <!-- Actor 1: Citizen (Left Top) -->
  <g transform="translate(45, 80)">
    <circle cx="20" cy="12" r="10" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="22" x2="20" y2="44" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="8" y1="30" x2="32" y2="30" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="44" x2="8" y2="60" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="44" x2="32" y2="60" stroke="#0f294a" stroke-width="1.8"/>
    <text x="20" y="74" text-anchor="middle" font-size="8" font-weight="bold" fill="#0f294a">Citizen</text>
  </g>

  <!-- Actor 2: IoT Sensor Gateway (Left Bottom) -->
  <g transform="translate(45, 215)">
    <rect x="5" y="10" width="30" height="26" rx="3" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="36" x2="20" y2="46" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="10" y1="46" x2="30" y2="46" stroke="#0f294a" stroke-width="1.8"/>
    <circle cx="20" cy="23" r="4" fill="#1e3a8a"/>
    <text x="20" y="60" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">IoT Gateway</text>
    <text x="20" y="70" text-anchor="middle" font-size="6.8" fill="#475569">(Grid Meters)</text>
  </g>

  <!-- Actor 3: Area Supervisor / Staff (Right Top) -->
  <g transform="translate(595, 80)">
    <circle cx="20" cy="12" r="10" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="22" x2="20" y2="44" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="8" y1="30" x2="32" y2="30" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="44" x2="8" y2="60" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="44" x2="32" y2="60" stroke="#0f294a" stroke-width="1.8"/>
    <text x="20" y="74" text-anchor="middle" font-size="8" font-weight="bold" fill="#0f294a">Municipal Staff</text>
    <text x="20" y="84" text-anchor="middle" font-size="6.8" fill="#475569">&amp; Supervisors</text>
  </g>

  <!-- Actor 4: City Manager / Administrator (Right Bottom) -->
  <g transform="translate(595, 215)">
    <circle cx="20" cy="12" r="10" fill="#ffffff" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="22" x2="20" y2="44" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="8" y1="30" x2="32" y2="30" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="44" x2="8" y2="60" stroke="#0f294a" stroke-width="1.8"/>
    <line x1="20" y1="44" x2="32" y2="60" stroke="#0f294a" stroke-width="1.8"/>
    <text x="20" y="74" text-anchor="middle" font-size="8" font-weight="bold" fill="#0f294a">City Manager</text>
    <text x="20" y="84" text-anchor="middle" font-size="6.8" fill="#475569">(Administrator)</text>
  </g>

  <!-- ================= USE CASES ================= -->
  <!-- UC 1: Lodge Citizen Complaint -->
  <ellipse cx="255" cy="85" rx="80" ry="18" fill="#f8fafc" stroke="#1e3a8a" stroke-width="1.5"/>
  <text x="255" y="88" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">UC-01: Lodge Citizen Complaint</text>

  <!-- UC 2: Triage & Escalate Complaint -->
  <ellipse cx="435" cy="85" rx="78" ry="18" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
  <text x="435" y="88" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#dc2626">UC-02: Triage &amp; Escalate Ticket</text>

  <!-- UC 3: Ingest Secured Energy Stream -->
  <ellipse cx="255" cy="150" rx="80" ry="18" fill="#f8fafc" stroke="#1e3a8a" stroke-width="1.5"/>
  <text x="255" y="153" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">UC-03: Ingest Secured Telemetry</text>

  <!-- UC 4: Broadcast Zone Power Commands -->
  <ellipse cx="435" cy="150" rx="80" ry="18" fill="#f8fafc" stroke="#1e3a8a" stroke-width="1.5"/>
  <text x="435" y="153" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">UC-04: Broadcast Zone Command</text>

  <!-- UC 5: Monitor Streetlight Fleet Memory -->
  <ellipse cx="255" cy="215" rx="80" ry="18" fill="#f8fafc" stroke="#1e3a8a" stroke-width="1.5"/>
  <text x="255" y="218" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">UC-05: Monitor Streetlight Fleet</text>

  <!-- UC 6: Query Aggregate Power Rollup -->
  <ellipse cx="435" cy="215" rx="80" ry="18" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
  <text x="435" y="218" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#059669">UC-06: Rollup Zone Power</text>

  <!-- UC 7: Author & Evaluate Policy DSL -->
  <ellipse cx="345" cy="280" rx="82" ry="18" fill="#f8fafc" stroke="#1e3a8a" stroke-width="1.5"/>
  <text x="345" y="283" text-anchor="middle" font-size="7.5" font-weight="bold" fill="#0f294a">UC-07: Evaluate Policy DSL</text>

  <!-- ================= ASSOCIATIONS ================= -->
  <!-- Citizen -> UC1 -->
  <line x1="75" y1="100" x2="178" y2="88" stroke="#0f294a" stroke-width="1.2"/>

  <!-- UC1 include UC2 -->
  <line x1="335" y1="85" x2="357" y2="85" stroke="#dc2626" stroke-dasharray="3,2" stroke-width="1.2" marker-end="url(#uc-arr)"/>
  <text x="346" y="78" text-anchor="middle" font-size="6.5" font-weight="bold" fill="#dc2626">&lt;&lt;include&gt;&gt;</text>

  <!-- UC2 -> Staff & CityManager -->
  <line x1="513" y1="85" x2="595" y2="105" stroke="#0f294a" stroke-width="1.2"/>
  <line x1="513" y1="88" x2="595" y2="230" stroke="#0f294a" stroke-width="1.2"/>

  <!-- IoT Gateway -> UC3 -->
  <line x1="75" y1="230" x2="185" y2="160" stroke="#0f294a" stroke-width="1.2"/>

  <!-- City Manager -> UC4 & UC7 -->
  <line x1="595" y1="240" x2="515" y2="155" stroke="#0f294a" stroke-width="1.2"/>
  <line x1="595" y1="250" x2="427" y2="280" stroke="#0f294a" stroke-width="1.2"/>

  <!-- UC4 extend UC6 -->
  <line x1="435" y1="168" x2="435" y2="197" stroke="#059669" stroke-dasharray="3,2" stroke-width="1.2" marker-end="url(#uc-arr)"/>
  <text x="458" y="185" font-size="6.5" font-weight="bold" fill="#059669">&lt;&lt;extend&gt;&gt;</text>

  <!-- Staff -> UC5 -->
  <line x1="595" y1="120" x2="330" y2="210" stroke="#0f294a" stroke-width="1.2"/>
</svg>"""

    # 7. End-to-End Enterprise System Architecture Diagram (Component / Deployment)
    svg7 = """<svg width="680" height="230" viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
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
        ("06_system_architecture.svg", svg7),
        ("07_system_use_case.svg", svg6),
    ]

    for fname, svg_content in files:
        fpath = os.path.join(svg_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Created {fpath}")

if __name__ == "__main__":
    create_svgs()

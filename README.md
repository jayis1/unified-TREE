# unified TREE

**unified TREE** is the unifying web control plane for the complete and growing [SoC Device Inventions](https://github.com/jayis1/SoC-Device-Inventions) and [Devices](https://github.com/jayis1/Devices) repositories. Every current and future hardware design becomes a node; every multi-device system becomes a branch with child nodes. Together they form one interoperable tree of sensors, scientific instruments, controllers, hubs, interfaces, and gateways.

The three repositories have distinct responsibilities:

| Repository | Responsibility |
|---|---|
| [SoC Device Inventions](https://github.com/jayis1/SoC-Device-Inventions) | Canonical device designs: schematics, firmware, BOMs, host tools, assembly instructions, and device-level documentation |
| [Devices](https://github.com/jayis1/Devices) | Canonical full systems: coordinated hubs, sensors, actuators, gateways, edge/cloud software, apps, and ML pipelines |
| [unified TREE](https://github.com/jayis1/unified-TREE) | Node registry, common protocol, four functional roles, composition rules, validation, and the larger system interface |

No device or system is replaced or hidden. Each remains independently buildable in its source collection and also gains a defined place in the unified architecture.

## Two source collections, one tree

[`devices.json`](./devices.json) registers the standalone inventions from SoC Device Inventions. [`systems.json`](./systems.json) registers every project from Devices as a branch and maps its firmware components as child nodes. Node identities are namespaced by collection and system, so repeated names such as `hub`, `room-sensor`, and `wearable-tag` remain unambiguous.

The current Devices import adds 53 source project directories and 222 child node types. Those counts are discovered from the registries rather than imposed as limits; both collections can keep growing.

## Web app and Android PWA

unified TREE is a webpage-based dashboard with a Home Assistant-inspired control-plane experience. Use the hosted web app at:

**[Open unified TREE →](https://jayis1.github.io/unified-TREE/)**

On Android, open that address in Chrome and choose **Install app** from the browser menu or use the dashboard's **Install App** button. It launches in its own window, receives updated node data from the web deployment, and keeps the application shell available offline. Desktop Chromium browsers can install the same PWA from the address bar.

There is no `.deb`, Electron wrapper, or native Android APK. The PWA manifest and service worker provide the installable app experience directly from the web.

## Run the web server locally

unified TREE is the central control-plane server for the node system. It serves the complete registry and topology as JSON APIs alongside a responsive fleet dashboard.

```bash
python3 tools/validate.py
python3 server.py
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080). No third-party Python packages or frontend build step are required.

The dashboard reads the registry dynamically and provides the full current fleet, role and domain filters, search, topology, system counts, and control-plane status. Newly registered nodes appear without frontend changes. The server exposes:

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Server readiness and registry size |
| `GET /api/nodes` | Complete device-node registry |
| `GET /api/systems` | Multi-node system branches and their child nodes |
| `GET /api/topology` | Four roles and their routing contracts |
| `GET /api/summary` | Counts by domain and role |

Bind to a network interface when the dashboard should be reachable by other machines:

```bash
python3 server.py --host 0.0.0.0 --port 8080
```

## Home Assistant integration

unified TREE includes a custom Home Assistant integration under [`custom_components/unified_tree`](./custom_components/unified_tree/). It connects to a running unified TREE server over the local API and creates:

- a connectivity binary sensor;
- a registered-node count sensor; and
- a domain count sensor.

For manual installation, copy `custom_components/unified_tree` into Home Assistant's `config/custom_components/` directory, restart Home Assistant, then choose **Settings → Devices & services → Add integration → unified TREE**. Enter the server address, such as `http://192.168.1.20:8080`.

The integration is local-polling and does not require a cloud account. This is the first Home Assistant bridge; device entities, controls, events, and automations can expand as physical node adapters join the unified protocol.

## A growing node tree and four roles

The device inventions are the nodes. **Observe, Reason, Act, and Coordinate are roles those nodes perform**, not four additional devices. A node can perform one role or several roles depending on its sensors, processing, actuators, and communications.

```text
                     findings
  physical world                 people + fleet
        │                            ▲
        ▼                            │
  ┌───────────┐ telemetry ┌────────┴───┐
  │  OBSERVE  ├──────────►│   REASON   │◄──── policy ────┐
  └─────▲─────┘           └─────┬──────┘                 │
        │ feedback              │ commands         ┌─────┴──────┐
        │                       ▼                  │ COORDINATE │
        │                 ┌────────────┐           └────────────┘
        └─────────────────┤    ACT     │
                          └────────────┘
```

| Node | Responsibility | Example device foundations |
|---|---|---|
| Observe | Acquire calibrated physical measurements and events | Neuro Sense Puck, Canopy Listener, Halo Pin, Terra Pin |
| Reason | Fuse signals, run DSP/ML, and produce findings or commands | Phase Scope, Spectra Charm, Echo Mote, Sky Lens |
| Act | Perform guarded physical work and close the feedback loop | Mycelium Node, Therma Weave, Levia Forge, Glyph Press |
| Coordinate | Connect users, history, policies, and groups of deployments | Hive Mind, Soil Whisper, Tremor Tile, Sap Watch |

These roles are logical capabilities, not four mandatory circuit boards. A small deployment may place several roles on one SoC node; a larger deployment can connect and replicate many device nodes. The stable boundary is the [Unified Device Protocol](./protocol/), so hardware can evolve without rebuilding the entire system.

## One fleet for every design

Every source design is registered in [`devices.json`](./devices.json), including instruments, monitors, creative interfaces, controllers, and fabrication tools. A device can serve several roles: for example, Mycelium Node observes its chamber, reasons over environmental state, acts through PID-controlled equipment, and coordinates remote monitoring.

The registry is deliberately separate from firmware. Each design retains its native real-time implementation while a thin adapter publishes the shared protocol. This lets the greater system combine devices by capability without forcing every firmware project onto one hardware stack.

### The unified interconnection fabric

All nodes join the same logical message fabric. They do not need bespoke pairwise integrations:

```text
Current and future SoC device nodes
        │
        ├── publish: telemetry, findings, feedback, health
        └── consume: commands, policy, relevant findings
                            │
                            ▼
                 Unified Device Protocol
                            │
              identity + routing + contracts
                            │
          BLE / Wi-Fi / MQTT / LoRaWAN / UART / SD
```

Role-based routing creates the interconnections. Observe output routes to any compatible Reason node; Reason output routes to Act and Coordinate nodes; Act feedback returns to Observe and Reason; Coordinate policy returns to Reason and Act. Each physical node advertises its roles and device type from the registry, allowing the system to discover valid routes instead of hard-coding device pairs.

This creates a many-node system while keeping local safety and real-time control inside each SoC. Network loss may interrupt coordination, but it must never bypass an Act node's hardware interlocks or local limits.

### How every device is linked

[`devices.json`](./devices.json) is the growing connection map. Every entry uses the original SoC repository directory name as its stable device type, identifies its application domain, and assigns all roles the device can fulfill. It currently covers every source design and expands as new inventions are added.

Most measurement instruments combine **Observe** and **Reason**. Devices with motors, heaters, excitation sources, haptics, printing mechanisms, or environmental controls also join **Act**. Field monitors and connected tools that publish fleet state additionally join **Coordinate**. Multi-purpose designs can participate in all four roles.

```text
SoC Device Inventions repository
  │
  ├── schematics + BOM ───────► physical device
  ├── firmware ───────────────► native sensing/control
  └── scripts + documentation ► protocol adapter
                                      │
                                      ▼
                              Unified Device Protocol
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
                 Observe ─────────► Reason ──────────► Act
                                      ▲                 │
                                      └── Coordinate ◄──┘
```

### Interoperability boundary

The [Unified Device Protocol](./protocol/) normalizes six message families: `telemetry`, `finding`, `command`, `feedback`, `health`, and `policy`. Transport adapters can carry those messages over BLE, Wi-Fi, MQTT, LoRaWAN, UART, removable storage, or another device-native link. This preserves hardware-specific real-time behavior while giving the greater system one consistent identity, routing, audit, and safety model.

The architecture does not require every device to communicate directly with every other device. Devices interconnect through role contracts. An Observe implementation can therefore be replaced or multiplied without rewriting Reason, and an Act implementation can enforce local safety even when Coordinate is offline.

### Building a complete deployment

A unified deployment selects devices by capability rather than by repository position. For example:

1. one or more **Observe** devices acquire calibrated physical measurements;
2. a **Reason** device or service fuses measurements and produces confidence-scored findings;
3. an **Act** device performs an authorized, bounded response and reports feedback; and
4. **Coordinate** stores history, applies policy, presents the system to users, and joins multiple local loops into a fleet.

The result can range from a single multi-role SoC to a replicated network containing many instances of several designs.

## Validate the tree

```bash
python3 tools/validate.py
```

The canonical topology is [`platform.json`](./platform.json). Validation checks that it contains exactly four uniquely named roles, that every role link resolves, and that every registered device node has a unique identity and at least one valid role. There is no maximum node count.

## From invention to system

1. Start with a device in [SoC Device Inventions](https://github.com/jayis1/SoC-Device-Inventions) and identify the role it fulfills.
2. Wrap its measurements or controls in the matching versioned contract.
3. Connect it to one adjacent node and validate a single end-to-end path.
4. Add coordination only when the local observe–reason–act loop is safe and useful.

This keeps each invention independently buildable while allowing several inventions to become one larger product.

## Source and navigation

- Browse the original hardware collection: [github.com/jayis1/SoC-Device-Inventions](https://github.com/jayis1/SoC-Device-Inventions)
- Inspect the complete connection registry: [`devices.json`](./devices.json)
- Read the shared protocol: [`protocol/`](./protocol/)
- You are at the unified composition repository: [unified TREE](https://github.com/jayis1/unified-TREE)

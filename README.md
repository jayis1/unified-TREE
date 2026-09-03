# unified TREE

**unified TREE** is the unifying web control plane for the complete and growing [SoC Device Inventions](https://github.com/jayis1/SoC-Device-Inventions) and [Devices](https://github.com/jayis1/Devices) repositories. Every current and future hardware design becomes a node; every multi-device system becomes a branch with child nodes. Together they form one interoperable tree of sensors, scientific instruments, controllers, hubs, interfaces, and gateways.

> **Current snapshot:** 365 registered node types · 68 multi-node system branches · 2 source collections · 4 shared roles · no fixed fleet limit

**[Open the live dashboard](https://jayis1.github.io/unified-TREE/)** · [Install as an Android PWA](#web-app-and-android-pwa) · [Connect Home Assistant](#home-assistant-integration)

The three repositories have distinct responsibilities:

| Repository | Responsibility |
|---|---|
| [SoC Device Inventions](https://github.com/jayis1/SoC-Device-Inventions) | Canonical device designs: schematics, firmware, BOMs, host tools, assembly instructions, and device-level documentation |
| [Devices](https://github.com/jayis1/Devices) | Canonical full systems: coordinated hubs, sensors, actuators, gateways, edge/cloud software, apps, and ML pipelines |
| [unified TREE](https://github.com/jayis1/unified-TREE) | Node registry, common protocol, four functional roles, composition rules, validation, and the larger system interface |

No device or system is replaced or hidden. Each remains independently buildable in its source collection and also gains a defined place in the unified architecture.

## Two source collections, one tree

[`devices.json`](./devices.json) registers the standalone inventions from SoC Device Inventions. [`systems.json`](./systems.json) registers every project from Devices as a branch and maps its firmware components as child nodes. Node identities are namespaced by collection and system, so repeated names such as `hub`, `room-sensor`, and `wearable-tag` remain unambiguous.

The current Devices import adds 68 source project directories and 291 child node types. Those counts are discovered from the registries rather than imposed as limits; both collections can keep growing.

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

| Role | Responsibility | Examples from both collections |
|---|---|---|
| Observe | Acquire calibrated physical measurements and events | Halo Pin; CycleGuard Bike Sensor; FireSync Room Sentinel |
| Reason | Fuse signals, run DSP/ML, and produce findings or commands | Spectra Charm; CycleGuard Hub; CardioSync Hub |
| Act | Perform guarded physical work and close the feedback loop | Therma Weave; FlowGuard Valve Controller; FireSync Stove Guard |
| Coordinate | Connect users, history, policies, and groups of deployments | Hive Mind; system hubs; fleet gateways |

These roles are logical capabilities, not four mandatory circuit boards. A small deployment may place several roles on one SoC node; a larger deployment can connect and replicate many device nodes. The stable boundary is the [Unified Device Protocol](./protocol/), so hardware can evolve without rebuilding the entire system.

## One fleet for every device and system

Every standalone source design is registered in [`devices.json`](./devices.json), while every coordinated Devices project and its children are registered in [`systems.json`](./systems.json). A node can serve several roles: Mycelium Node spans all four roles, while a Devices branch commonly combines a coordinating hub, observing sensors, reasoning edge processors, and guarded actuators.

The registries are deliberately separate from firmware. Each source project retains its native real-time implementation while a thin adapter publishes the shared protocol. This lets the greater system combine nodes by capability without forcing every firmware project onto one hardware stack.

### The unified interconnection fabric

All nodes join the same logical message fabric. They do not need bespoke pairwise integrations:

```text
Current and future standalone + system child nodes
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

### How every source project is linked

[`devices.json`](./devices.json) uses each standalone SoC directory name as a stable node type. [`systems.json`](./systems.json) preserves the Devices hierarchy with a stable system ID and namespaced child-node IDs. Both registries identify application domains and role capabilities, and both expand as new inventions are added.

Most measurement instruments combine **Observe** and **Reason**. Devices with motors, heaters, excitation sources, haptics, printing mechanisms, or environmental controls also join **Act**. Field monitors and connected tools that publish fleet state additionally join **Coordinate**. Multi-purpose designs can participate in all four roles.

```text
SoC Device Inventions         Devices
standalone nodes              system branches
        │                          │
        └────────────┬─────────────┘
                     ▼
          identity + role registry
                     │
                     ▼
          Unified Device Protocol
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
    Observe ──────► Reason ──────► Act
                      ▲             │
                      └ Coordinate ◄┘
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

1. Add a standalone design to [SoC Device Inventions](https://github.com/jayis1/SoC-Device-Inventions), or a coordinated system branch to [Devices](https://github.com/jayis1/Devices).
2. Register the standalone node in `devices.json`, or the branch and child nodes in `systems.json`.
3. Assign each node's Observe, Reason, Act, and Coordinate capabilities.
4. Wrap measurements or controls in the matching versioned protocol contract.
5. Validate one end-to-end route before expanding the deployment.

This keeps each invention independently buildable while allowing several inventions to become one larger product.

## Source and navigation

- Open the installable dashboard: [jayis1.github.io/unified-TREE](https://jayis1.github.io/unified-TREE/)
- Browse standalone hardware nodes: [SoC Device Inventions](https://github.com/jayis1/SoC-Device-Inventions)
- Browse coordinated system branches: [Devices](https://github.com/jayis1/Devices)
- Inspect the standalone registry: [`devices.json`](./devices.json)
- Inspect the system and child-node registry: [`systems.json`](./systems.json)
- Read the shared protocol: [`protocol/`](./protocol/)
- Install the Home Assistant bridge: [`custom_components/unified_tree/`](./custom_components/unified_tree/)

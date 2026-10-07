from __future__ import annotations

from .common import MaintenanceError, digest


def build_links(inventory: dict) -> dict:
    nodes = {node["id"]: node for node in inventory["nodes"]}
    edges = {}

    def add(source, target, kind):
        if source not in nodes or target not in nodes:
            raise MaintenanceError("reference_invalid", f"unknown relationship endpoint: {source} -> {target}")
        identity = "edge:" + digest([source, kind, target])[:24]
        edges[identity] = {"id": identity, "source": source, "target": target, "type": kind,
                           "origin": "authored_reference", "semantic_review": "unreviewed"}

    for node in inventory["nodes"]:
        if node["kind"] != "bundle":
            continue
        record = node["record"]
        if "member_candidates" not in record or "associated_profile_ids" not in record:
            raise MaintenanceError("reference_invalid", "only compiled validated bundles can publish links")
        for member in record["member_candidates"]:
            add(member["id"], node["id"], "member_of")
        for profile in record["associated_profile_ids"]:
            add(node["id"], "profile:" + profile, "associated_with")
    rows = [edges[key] for key in sorted(edges)]
    outgoing, incoming = {node: [] for node in sorted(nodes)}, {node: [] for node in sorted(nodes)}
    for edge in rows:
        outgoing[edge["source"]].append(edge["id"])
        incoming[edge["target"]].append(edge["id"])
    return {"schema": "photo-data-links/v1", "edges": rows, "outgoing": outgoing, "incoming": incoming,
            "unlinked": sorted(node for node in nodes if not outgoing[node] and not incoming[node])}


def path_key(nodes: list[str]) -> str:
    return "path:" + digest(nodes)[:24]


def query(inventory: dict, links: dict, node_id: str, reviews=None) -> dict:
    nodes = {node["id"]: node for node in inventory["nodes"]}
    if node_id not in nodes:
        raise MaintenanceError("node_unknown", node_id)
    edges = {edge["id"]: edge for edge in links["edges"]}
    reviews = reviews or {}
    paths = []
    kind = nodes[node_id]["kind"]
    if kind == "candidate":
        for member in links["outgoing"][node_id]:
            bundle = edges[member]["target"]
            associated = links["outgoing"][bundle]
            paths.extend([[node_id, bundle, edges[edge]["target"]] for edge in associated] or [[node_id, bundle]])
    elif kind == "profile":
        for association in links["incoming"][node_id]:
            bundle = edges[association]["source"]
            members = links["incoming"][bundle]
            paths.extend([[edges[edge]["source"], bundle, node_id] for edge in members] or [[bundle, node_id]])
    else:
        members = [edges[edge]["source"] for edge in links["incoming"][node_id]]
        profiles = [edges[edge]["target"] for edge in links["outgoing"][node_id]]
        if profiles:
            paths.extend([[member, node_id, profile] for member in members for profile in profiles])
        else:
            paths.extend([[member, node_id] for member in members])
    rows = []
    for path in sorted(paths):
        key = path_key(path)
        rows.append({"id": key, "nodes": path, "relation": "via_bundle",
                     "meaning_support": "not_inferred", "review": reviews.get(key, {"status": "unreviewed"}),
                     "entity_hashes": {identity: nodes[identity]["entity_sha256"] for identity in path},
                     "source_refs": {identity: nodes[identity]["source_refs"] for identity in path}})
    return {"node": node_id, "kind": kind, "paths": rows, "path_count": len(rows),
            "unique_related_nodes": sorted({identity for path in paths for identity in path if identity != node_id}),
            "profile_activation": "independent_request_evidence_only"}

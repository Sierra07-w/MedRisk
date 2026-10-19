#!/usr/bin/env python3
"""Import docs/management/youtrack-import.csv into YouTrack via REST API.

Usage:
    export YOUTRACK_URL=https://medrisk.youtrack.cloud
    export YOUTRACK_TOKEN=<permanent token>   # Avatar -> Account Security -> Tokens
    python3 scripts/youtrack_import.py --dry-run   # check mapping without changes
    python3 scripts/youtrack_import.py             # import

The token needs these YouTrack permissions: Read basic user info, Users, Projects,
Issues: Create/Modify; project-admin permissions for custom fields (optional).

Rows are imported strictly in CSV order so issue IDs match DIP-1 .. DIP-46.
"""
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("YOUTRACK_URL", "https://medrisk.youtrack.cloud").rstrip("/")
TOKEN = os.environ.get("YOUTRACK_TOKEN", "")
PROJECT_SHORT = "DIP"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT, "docs", "management", "youtrack-import.csv")

# name used in the CSV -> invite e-mail (see youtrack-backlog.md, step 2)
NAME_TO_EMAIL = {
    "Muslim Syzdykov": "mme84855@gmail.com",
    "Zarina Kosaman": "zarinakosaman9@gmail.com",
    "Sara Mukhammad": "mukhammadsara07@gmail.com",
    "Aigerim Bakiyeva": "A.Bakiyeva@astanait.edu.kz",
}


def api(method, path, payload=None, fields="summary", ok=(200, 201)):
    url = BASE + path
    if "fields=" not in url and fields:
        url += ("&" if "?" in url else "?") + "fields=" + fields
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + TOKEN,
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            return (r.status, json.loads(body) if body else None)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            return (e.code, json.loads(body))
        except Exception:
            return (e.code, {"error": body[:300]})


def get_user(name):
    """Resolve a CSV assignee to an existing YouTrack login."""
    email = NAME_TO_EMAIL.get(name, name)
    for query in (email, name):
        status, users = api("GET", "/api/users?query=" + urllib.parse.quote(query),
                            fields="login,name")
        if status == 200 and users:
            # exact-ish match: login or name contains the query
            for u in users:
                if query.lower() in (u.get("login", "") + u.get("name", "")).lower():
                    return u["login"]
    return None


def build_description(row):
    desc = row["Description"]
    if "(acceptance:" in desc:
        main, acc = desc.split("(acceptance:", 1)
        desc = main.strip() + "\n\n**Acceptance criteria:** " + acc.rstrip(")").strip()
    desc += f"\n\n**Milestone:** {row['Milestone']} · **Due:** {row['Due date']}"
    return desc


def build_payload(row, assignee, include_milestone_field):
    fields = [
        {"name": "Priority", "value": {"name": row["Priority"]}},
        {"name": "State", "value": {"name": row["State"]}},
    ]
    if assignee:
        fields.append({"name": "Assignee", "value": {"login": assignee}})
    if include_milestone_field:
        fields.append({"name": "Milestone", "value": {"name": row["Milestone"]}})
    return {
        "summary": row["Summary"],
        "description": build_description(row),
        "customFields": fields,
        "dueDate": row["Due date"],
    }


def optional_variants(payload, assignee, milestone_field):
    """Successively stricter payloads when YouTrack rejects an attribute."""
    yield payload, "all fields"
    p = {k: v for k, v in payload.items() if k != "dueDate"}
    yield p, "without dueDate"
    p = dict(p)
    p["customFields"] = [f for f in p["customFields"] if f["name"] != "Milestone"]
    yield p, "without milestone field (milestone stays in description)"
    p = dict(p)
    p["customFields"] = [f for f in p["customFields"] if f["name"] != "State"]
    yield p, "without state"
    if assignee:
        p = dict(p)
        p["customFields"] = [f for f in p["customFields"] if f["name"] != "Assignee"]
        yield p, "without assignee"
    p = {k: v for k, v in p.items() if k != "customFields"}
    yield p, "summary + description only"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and check project/users, create nothing")
    args = ap.parse_args()

    if not TOKEN:
        sys.exit("Set YOUTRACK_TOKEN (Avatar -> Account Security -> Tokens -> New token).")

    status, projects = api("GET", "/api/projects", fields="id,name,shortName")
    if status != 200:
        sys.exit(f"Cannot list projects ({status}): {projects}")
    project = next((p for p in projects if p.get("shortName") == PROJECT_SHORT), None)
    if not project:
        sys.exit(f"Project with short name {PROJECT_SHORT} not found. Projects: "
                 + ", ".join(p.get("shortName", "?") for p in projects))
    print(f"Project: {project['name']} ({project['shortName']}, id={project['id']})")

    # check whether Milestone custom field exists (create it if possible)
    status, cfs = api("GET", f"/api/admin/projects/{project['id']}/customFields",
                      fields="name")
    has_milestone = False
    if status == 200:
        has_milestone = any(c.get("name") == "Milestone" for c in cfs)
        if not has_milestone and not args.dry_run:
            st, resp = api("POST", f"/api/admin/projects/{project['id']}/customFields",
                           {"name": "Milestone", "type": {"name": "string"},
                            "isMultiValue": False}, fields="id,name")
            has_milestone = st in (200, 201)
            print("Milestone custom field", "created" if has_milestone
                  else f"NOT created ({st}): {resp}")
    else:
        print(f"Note: cannot read custom fields ({status}) — milestone will go "
              "into the description only")

    with open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    print(f"{len(rows)} tasks in {os.path.relpath(CSV_PATH, ROOT)}")

    if args.dry_run:
        users = {}
        for name in sorted({r["Assignee"] for r in rows}):
            login = None if name == "Team" else get_user(name)
            users[name] = login or "(unresolved)"
        for name, login in users.items():
            print(f"  assignee {name!r} -> {login}")
        for r in rows:
            print(f"  {r['Summary']:<7} {r['Priority']:<9} {r['State']:<11} "
                  f"{r['Milestone']}  due {r['Due date']}")
        print("Dry run OK — re-run without --dry-run to import.")
        return

    created, skipped = [], []
    for row in rows:
        assignee = None if row["Assignee"] == "Team" else get_user(row["Assignee"])
        if row["Assignee"] != "Team" and not assignee:
            print(f"  warn: assignee {row['Assignee']!r} unresolved — created unassigned")
        last_err = None
        for payload, variant in optional_variants(
                build_payload(row, assignee, has_milestone), assignee, has_milestone):
            status, resp = api("POST", "/api/issues", payload, fields="idReadable,summary")
            if status in (200, 201):
                created.append(resp["idReadable"])
                print(f"  {resp['idReadable']} <- {row['Summary']}  [{variant}]")
                break
            last_err = resp
        else:
            skipped.append(row["Summary"])
            print(f"  FAILED {row['Summary']}: {last_err}")
        # be gentle with the quota
        import time
        time.sleep(0.3)

    print(f"\nCreated: {len(created)}  Failed: {len(skipped)}")
    if skipped:
        print("Failed tasks:\n  " + "\n  ".join(skipped))
        sys.exit(1)
    print(f"Verify ID order: first={created[0]} last={created[-1]}")


if __name__ == "__main__":
    main()

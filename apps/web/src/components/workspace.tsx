"use client";
import { FormEvent, useEffect, useRef, useState } from "react";
import Link from "next/link";
import {
  ArrowUpRight,
  ArrowRight,
  LayoutDashboard,
  Search,
  Plus,
  RefreshCw,
  LogOut,
  Menu,
  X,
  Bell,
  ChevronRight,
  Radio,
  ShieldCheck,
} from "lucide-react";
import contracts from "@/lib/contracts.json";
import { api, ApiError, label, money } from "@/lib/api";
import { ErrorNotice } from "./forms";
import { EvidenceUpload, Booking } from "./evidence";

type Row = Record<string, unknown> & {
  id: string;
  version: number;
  status: string;
};
type User = { id: string; name: string; email: string; roles: string[] };
type Schema = {
  type?: string | string[];
  title?: string;
  enum?: string[];
  const?: unknown;
  format?: string;
  minimum?: number;
  maximum?: number;
  minLength?: number;
  maxLength?: number;
  required?: string[];
  properties?: Record<string, Schema>;
  oneOf?: Schema[];
  items?: Schema;
  $ref?: string;
  description?: string;
};
const cfg: Record<
  string,
  { kind: string; create?: string; transition?: string }
> = {
  "PNL-02": {
    kind: "seller-leads",
    create: "createSellerLead",
    transition: "transitionSellerLead",
  },
  "PNL-03": {
    kind: "purchase-requests",
    create: "createProcurement",
    transition: "transitionPurchaseRequest",
  },
  "PNL-04": { kind: "auctions" },
  "PNL-05": {
    kind: "auctions",
    create: "createAuction",
    transition: "transitionAuction",
  },
  "PNL-06": {
    kind: "inspections",
    create: "createInspection",
    transition: "transitionInspection",
  },
  "PNL-07": {
    kind: "appointments",
    create: "createAppointment",
    transition: "transitionAppointment",
  },
  "PNL-08": { kind: "seller-leads", transition: "transitionSellerLead" },
  "PNL-09": {
    kind: "listings",
    create: "createVehicleListing",
    transition: "transitionVehicleListing",
  },
  "PNL-10": {
    kind: "valuations",
    create: "createValuation",
    transition: "transitionValuation",
  },
  "PNL-11": {
    kind: "contracts",
    create: "createContract",
    transition: "transitionContract",
  },
  "PNL-12": {
    kind: "obligations",
    create: "createPaymentObligation",
    transition: "transitionPaymentObligation",
  },
  "PNL-13": {
    kind: "financing-applications",
    create: "createFinancingApplication",
    transition: "transitionFinancingApplication",
  },
  "PNL-14": {
    kind: "deliveries",
    create: "createDelivery",
    transition: "transitionDelivery",
  },
  "PNL-15": {
    kind: "support-tickets",
    create: "createSupportTicket",
    transition: "transitionSupportTicket",
  },
  "PNL-16": {
    kind: "claims",
    create: "createWarrantyClaim",
    transition: "transitionWarrantyClaim",
  },
  "PNL-17": {
    kind: "content-items",
    create: "createContent",
    transition: "actOnContent",
  },
  "PNL-18": {
    kind: "campaigns",
    create: "createCampaign",
    transition: "actOnCampaign",
  },
  "PNL-19": { kind: "reports" },
  "PNL-20": { kind: "audit" },
};
function resolve(s: Schema): Schema {
  if (s.$ref)
    return resolve(
      (contracts.schemas as unknown as Record<string, Schema>)[
        s.$ref.split("/").pop()!
      ] || {},
    );
  return s;
}
function Fields({
  schema,
  prefix = "",
  value,
  onChange,
}: {
  schema: Schema;
  prefix?: string;
  value: Record<string, unknown>;
  onChange: (v: Record<string, unknown>) => void;
}) {
  let s = resolve(schema);
  const [variant, setVariant] = useState(0);
  if (s.oneOf) {
    const options = s.oneOf;
    return (
      <>
        <label>
          Action
          <select
            onChange={(e) => {
              setVariant(Number(e.target.value));
              onChange({
                action:
                  options[Number(e.target.value)].properties?.action?.const,
              });
            }}
            value={variant}
          >
            {options.map((v, i) => (
              <option key={i} value={i}>
                {String(
                  v.properties?.action?.const || v.title || `Option ${i + 1}`,
                )}
              </option>
            ))}
          </select>
        </label>
        <Fields
          key={variant}
          schema={options[variant]}
          value={value}
          onChange={onChange}
        />
      </>
    );
  }
  return (
    <>
      {Object.entries(s.properties || {}).map(([key, raw]) => {
        const f = resolve(raw),
          required = s.required?.includes(key);
        const v = value[key];
        const change = (x: unknown) => onChange({ ...value, [key]: x });
        if (f.const !== undefined) {
          return (
            <p className="muted" key={key}>
              {label(key)}: {String(f.const)}
            </p>
          );
        }
        if (f.type === "object" || f.properties)
          return (
            <fieldset key={key}>
              <legend>{label(key)}</legend>
              <Fields
                schema={f}
                prefix={prefix + key + "."}
                value={(v as Record<string, unknown>) || {}}
                onChange={change}
              />
            </fieldset>
          );
        return (
          <label key={key}>
            {label(key)}
            {required ? " *" : ""}
            {f.enum ? (
              <select
                required={required}
                value={String(v || "")}
                onChange={(e) => change(e.target.value)}
              >
                <option value="">Choose {label(key).toLowerCase()}</option>
                {f.enum.map((a) => (
                  <option key={a} value={a}>
                    {label(a)}
                  </option>
                ))}
              </select>
            ) : f.type === "boolean" ? (
              <input
                type="checkbox"
                checked={Boolean(v)}
                onChange={(e) => change(e.target.checked)}
                required={required}
              />
            ) : f.type === "array" ? (
              <textarea
                required={required}
                value={typeof v === "string" ? v : JSON.stringify(v || [])}
                onChange={(e) => {
                  try {
                    change(JSON.parse(e.target.value));
                  } catch {
                    change(e.target.value);
                  }
                }}
                rows={3}
                placeholder="JSON array of the referenced records"
              />
            ) : (
              <input
                required={required}
                value={String(v ?? "")}
                type={
                  f.type === "integer"
                    ? "number"
                    : f.format === "date-time"
                      ? "text"
                      : f.format === "email"
                        ? "email"
                        : "text"
                }
                min={f.minimum}
                max={f.maximum}
                minLength={f.minLength}
                maxLength={f.maxLength}
                placeholder={
                  f.format === "uuid"
                    ? "Record UUID"
                    : f.format === "date-time"
                      ? "2026-11-15T12:00:00Z"
                      : undefined
                }
                onChange={(e) =>
                  change(
                    f.type === "integer"
                      ? Number(e.target.value)
                      : e.target.value,
                  )
                }
              />
            )}
            {f.format === "uuid" && (
              <small>Use the reference from the corresponding record.</small>
            )}
          </label>
        );
      })}
    </>
  );
}

function withConstants(
  schema: Schema,
  value: Record<string, unknown>,
): Record<string, unknown> {
  const s = resolve(schema);
  if (s.oneOf) {
    const chosen =
      s.oneOf.find((v) => v.properties?.action?.const === value.action) ||
      s.oneOf[0];
    return withConstants(chosen, value);
  }
  const out = { ...value };
  for (const [k, raw] of Object.entries(s.properties || {})) {
    const f = resolve(raw);
    if (f.const !== undefined) out[k] = f.const;
    else if (f.type === "object" && out[k])
      out[k] = withConstants(f, out[k] as Record<string, unknown>);
  }
  return out;
}

function CommandForm({
  operation,
  row,
  onClose,
  onDone,
}: {
  operation: string;
  row?: Row;
  onClose: () => void;
  onDone: () => void;
}) {
  const op = (
    contracts.operations as unknown as Record<
      string,
      { path: string; method: string; schema: Schema }
    >
  )[operation];
  const [value, setValue] = useState<Record<string, unknown>>({});
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const key = useRef(crypto.randomUUID());
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const d = dialog.current;
    d?.showModal();
    return () => d?.close();
  }, []);
  async function submit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const path = op.path.replace(/\{[^}]+\}/g, row?.id || "");
      await api(path, {
        method: op.method,
        headers: {
          "Idempotency-Key": key.current,
          ...(row ? { "If-Match": `"${row.version}"` } : {}),
        },
        body: JSON.stringify(withConstants(op.schema || {}, value)),
      });
      onDone();
      onClose();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <dialog ref={dialog} onCancel={onClose} className="command-dialog">
      <div className="dialog-top">
        <h2>{label(operation.replace(/([a-z])([A-Z])/g, "$1 $2"))}</h2>
        <button onClick={onClose} aria-label="Close dialog">
          <X size={21} />
        </button>
      </div>
      <ErrorNotice error={error} />
      <form onSubmit={submit}>
        <Fields schema={op.schema || {}} value={value} onChange={setValue} />
        <div className="dialog-actions">
          <button type="button" className="button outline" onClick={onClose}>
            Cancel
          </button>
          <button className="button primary" disabled={busy}>
            {busy ? "Checking result…" : "Confirm request"}{" "}
            <ArrowRight size={16} />
          </button>
        </div>
      </form>
    </dialog>
  );
}

function ReportView({ revisionId }: { revisionId: string }) {
  type Finding = {
    point_id: string;
    result: string;
    severity?: string;
    comment?: string;
  };
  const [report, setReport] = useState<{
    status: string;
    findings: Finding[];
  }>();
  const [points, setPoints] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  async function load() {
    setOpen(true);
    setError("");
    try {
      const r = await api<{
        status: string;
        template_version_id: string;
        findings: Finding[];
      }>(`/inspection-revisions/${revisionId}`);
      const t = await api<{ points: { id: string; label: string }[] }>(
        `/inspection-templates/${r.template_version_id}`,
      );
      setPoints(Object.fromEntries(t.points.map((p) => [p.id, p.label])));
      setReport(r);
    } catch (e) {
      setError((e as Error).message);
    }
  }
  return (
    <section className="record-detail">
      <div className="heading-row">
        <h3>Published inspection</h3>
        <button className="text-button" onClick={load}>
          {open ? "Refresh report" : "View inspection report"}{" "}
          <ArrowUpRight size={15} />
        </button>
      </div>
      <ErrorNotice error={error} />
      {open && report && (
        <>
          <p className="muted">
            Revision {revisionId} · {report.status}. Unknown is not a pass.
          </p>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Inspection point</th>
                  <th>Result</th>
                  <th>Notes</th>
                </tr>
              </thead>
              <tbody>
                {report.findings.map((f) => (
                  <tr key={f.point_id}>
                    <td>{points[f.point_id] || "Inspection point"}</td>
                    <td>
                      {label(f.result)}
                      {f.severity ? " · " + label(f.severity) : ""}
                    </td>
                    <td>{f.comment || "No additional note"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </section>
  );
}

function AuctionRoom({ row, onClose }: { row: Row; onClose: () => void }) {
  const [snapshot, setSnapshot] = useState(row);
  const [amount, setAmount] = useState(Number(row.minimum_next_bid_minor || 0));
  const [error, setError] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [connected, setConnected] = useState(false);
  const intent = useRef({ key: crypto.randomUUID(), payload: "" });
  useEffect(() => {
    let stopped = false;
    async function refresh() {
      try {
        const r = await api<Row>("/auctions/" + row.id);
        if (!stopped) {
          setSnapshot(r);
          setConnected(true);
        }
      } catch {
        if (!stopped) setConnected(false);
      }
    }
    refresh();
    const timer = setInterval(refresh, 5000);
    return () => {
      stopped = true;
      clearInterval(timer);
    };
  }, [row.id]);
  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError("");
    setNote("");
    const body = JSON.stringify({
      amount_minor: amount,
      currency: snapshot.currency,
    });
    if (intent.current.payload && intent.current.payload !== body)
      intent.current = { key: crypto.randomUUID(), payload: body };
    else intent.current.payload = body;
    try {
      const b = await api<Row>(`/auctions/${row.id}/bids`, {
        method: "POST",
        headers: { "Idempotency-Key": intent.current.key },
        body,
      });
      setNote("Bid accepted. Receipt " + b.bid_id);
      setSnapshot(await api<Row>("/auctions/" + row.id));
      intent.current = { key: crypto.randomUUID(), payload: "" };
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="auction-room">
      <button className="text-button" onClick={onClose}>
        ← All auctions
      </button>
      <div className="heading-row">
        <h2>Live auction</h2>
        <span className={"status " + (connected ? "available" : "paused")}>
          <Radio size={12} />
          {connected
            ? "Connected · refreshes every 5s"
            : "Connection unavailable"}
        </span>
      </div>
      <img
        src="/vehicles/car-0.svg"
        alt="Representative development illustration"
        width="960"
        height="600"
      />
      <div className="auction-stats">
        <div>
          <small>Current accepted bid</small>
          <strong>
            {snapshot.current_bid_minor
              ? money(
                  Number(snapshot.current_bid_minor),
                  String(snapshot.currency),
                )
              : "No bids yet"}
          </strong>
        </div>
        <div>
          <small>Closes</small>
          <strong>
            {new Date(String(snapshot.closes_at)).toLocaleString("en-GB")}
          </strong>
        </div>
        <div>
          <small>Sequence</small>
          <strong>{String(snapshot.sequence)}</strong>
        </div>
      </div>
      <ErrorNotice error={error} />
      {note && (
        <p className="notice" role="status">
          {note}
        </p>
      )}
      <form onSubmit={submit}>
        <label>
          Your bid in minor units ({String(snapshot.currency)})
          <input
            type="number"
            min={Number(snapshot.minimum_next_bid_minor || 1)}
            step={Number(snapshot.increment_minor || 1)}
            value={amount}
            onChange={(e) => setAmount(Number(e.target.value))}
            required
          />
        </label>
        <button
          className="button primary"
          disabled={busy || !connected || snapshot.status !== "open"}
        >
          {busy ? "Checking your bid…" : "Place bid"} <ArrowUpRight size={17} />
        </button>
      </form>
      <p className="muted">
        The server decides acceptance. A winning bid still requires the seller’s
        decision, contracts and separate settlement.
      </p>
      <ReportView revisionId={String(snapshot.report_revision_id)} />
    </section>
  );
}

export function Workspace() {
  const [user, setUser] = useState<User>();
  const [panel, setPanel] = useState("");
  const [rows, setRows] = useState<Row[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState<{ op: string; row?: Row }>();
  const [selected, setSelected] = useState<Row>();
  const [query, setQuery] = useState("");
  const [mobile, setMobile] = useState(false);
  const [notice, setNotice] = useState("");
  const panels = contracts.panels.filter(
    (p) => p.id !== "PNL-01" && p.roles.some((r) => user?.roles.includes(r)),
  );
  useEffect(() => {
    api<{ user: User }>("/workspace")
      .then((r) => {
        setUser(r.user);
        const first = contracts.panels.find(
          (p) =>
            p.id !== "PNL-01" && p.roles.some((x) => r.user.roles.includes(x)),
        );
        setPanel(first?.id || "PNL-02");
      })
      .catch((e) => {
        setError(e.message);
        setLoading(false);
      });
  }, []);
  async function load() {
    if (!panel) return;
    setLoading(true);
    setError("");
    try {
      const c = cfg[panel];
      const path =
        c.kind === "reports" ? "/analytics/metrics" : "/workspace/" + c.kind;
      const r = await api<{ items?: Row[]; metrics?: Record<string, number> }>(
        path,
      );
      setRows(
        r.items ||
          (r.metrics
            ? Object.entries(r.metrics).map(([k, v]) => ({
                id: k,
                status: String(v),
                version: 1,
                title: label(k),
              }))
            : []),
      );
    } catch (e) {
      setError((e as Error).message);
      setRows([]);
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    void load();
    setSelected(undefined);
  }, [panel]);
  const c = cfg[panel];
  const p = panels.find((p) => p.id === panel);
  const filtered = rows.filter((r) =>
    JSON.stringify(r).toLowerCase().includes(query.toLowerCase()),
  );
  if (!user)
    return (
      <section className="section">
        <h1>Your Autolane.</h1>
        <ErrorNotice error={error} />
        {loading ? (
          <p role="status">Loading your account…</p>
        ) : (
          <Link className="button primary" href="/sign-in">
            Sign in to continue <ArrowRight size={17} />
          </Link>
        )}
      </section>
    );
  return (
    <div className="workspace">
      <aside className={"sidebar " + (mobile ? "open" : "")}>
        <div className="workspace-title">
          <LayoutDashboard size={19} /> WORKSPACE
        </div>
        <p className="muted">{user.name || user.email}</p>
        <nav aria-label="Workspace navigation">
          {panels.map((p) => (
            <button
              key={p.id}
              className={panel === p.id ? "selected" : ""}
              onClick={() => {
                setPanel(p.id);
                setMobile(false);
              }}
            >
              {p.name}
              <ChevronRight size={14} />
            </button>
          ))}
          <Link href="/sell">
            New selling request <Plus size={14} />
          </Link>
          <Link href="/buy">
            Browse marketplace <ArrowUpRight size={14} />
          </Link>
        </nav>
        <div className="sidebar-bottom">
          <ShieldCheck size={17} />
          <small>
            Local development
            <br />
            External funds disabled
          </small>
        </div>
        <button
          className="text-button"
          onClick={async () => {
            await api("/auth/session", { method: "DELETE" });
            location.assign("/sign-in");
          }}
        >
          <LogOut size={15} /> Sign out
        </button>
      </aside>
      <section className="workspace-main">
        <div className="workspace-top">
          <button
            className="mobile-menu"
            aria-label="Open workspace menu"
            onClick={() => setMobile(!mobile)}
          >
            <Menu />
          </button>
          <span>
            MY AUTOLANE <ChevronRight size={13} /> {p?.name}
          </span>
          <span className="avatar">
            {(user.name || user.email).slice(0, 1)}
          </span>
        </div>
        <div className="heading-row">
          <div>
            <div className="eyebrow">YOUR WORK, CLEARLY ORGANIZED</div>
            <h1>{p?.name || "Account"}</h1>
            <p className="muted">
              Current records from your authorized workspace.
            </p>
          </div>
          <div className="toolbar">
            <button
              className="button outline"
              onClick={load}
              aria-label="Refresh records"
            >
              <RefreshCw size={17} />
            </button>
            {c?.create && (
              <button
                className="button primary"
                onClick={() => setForm({ op: c.create! })}
              >
                <Plus size={17} /> New record
              </button>
            )}
          </div>
        </div>
        <ErrorNotice error={error} />
        {notice && (
          <p className="notice" role="status">
            {notice}
          </p>
        )}
        {selected && panel === "PNL-04" ? (
          <AuctionRoom row={selected} onClose={() => setSelected(undefined)} />
        ) : (
          <>
            <p className="muted">
              This build is in active development. External integrations and
              some workflow actions are not available yet; the implementation
              status is recorded in the repository.
            </p>
            <div className="workspace-summary">
              <div>
                <span>Visible records</span>
                <strong>{rows.length}</strong>
              </div>
              <div>
                <span>Environment</span>
                <strong className="small-strong">Development</strong>
              </div>
              <div>
                <span>Scope</span>
                <strong className="small-strong">
                  Your authorized records
                </strong>
              </div>
            </div>
            <div className="table-toolbar">
              <div>
                <Search size={17} />
                <input
                  aria-label="Search visible records"
                  placeholder="Search these records…"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
              </div>
              <span>{filtered.length} records</span>
            </div>
            {loading ? (
              <div className="empty" role="status">
                Loading your records…
              </div>
            ) : !filtered.length ? (
              <div className="empty">
                <LayoutDashboard size={32} />
                <h3>No records to show.</h3>
                <p>
                  {error
                    ? "Resolve the access or service error above, then retry."
                    : "New records will appear here when they are assigned to your scope."}
                </p>
              </div>
            ) : (
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Record</th>
                      <th>Status</th>
                      <th>Version</th>
                      <th>Next step</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((r) => (
                      <tr key={r.id}>
                        <td>
                          <strong>
                            {String(
                              r.title ||
                                r.subject ||
                                r.name ||
                                r.id.slice(0, 8),
                            )}
                          </strong>
                          <small>{r.id}</small>
                        </td>
                        <td>
                          <span className={"status " + r.status}>
                            {label(r.status || String(r.action || "Recorded"))}
                          </span>
                        </td>
                        <td>{r.version || "—"}</td>
                        <td>
                          <button
                            className="text-button"
                            onClick={() => setSelected(r)}
                          >
                            Review <ArrowUpRight size={15} />
                          </button>
                          {c?.transition && (
                            <button
                              className="text-button"
                              onClick={() =>
                                setForm({ op: c.transition!, row: r })
                              }
                            >
                              Take action
                            </button>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            {selected && (
              <>
                <EvidenceUpload caseId={selected.id} />
                {panel === "PNL-02" && <Booking lead={selected} />}
                <div className="record-detail">
                  <div className="heading-row">
                    <h2>Record details</h2>
                    <button
                      className="text-button"
                      onClick={() => setSelected(undefined)}
                    >
                      Close <X size={17} />
                    </button>
                  </div>
                  <dl>
                    {Object.entries(selected).map(([k, v]) => (
                      <div key={k}>
                        <dt>{label(k)}</dt>
                        <dd>
                          {typeof v === "object"
                            ? JSON.stringify(v)
                            : String(v)}
                        </dd>
                      </div>
                    ))}
                  </dl>
                  {panel === "PNL-06" && (
                    <button
                      className="button primary"
                      onClick={() =>
                        setForm({
                          op: "createInspectionRevision",
                          row: selected,
                        })
                      }
                    >
                      Create report revision
                    </button>
                  )}
                </div>
              </>
            )}
          </>
        )}
        {form && (
          <CommandForm
            operation={form.op}
            row={form.row}
            onClose={() => setForm(undefined)}
            onDone={() => {
              setNotice(
                "Your request was committed. The records have been refreshed.",
              );
              void load();
            }}
          />
        )}
      </section>
    </div>
  );
}

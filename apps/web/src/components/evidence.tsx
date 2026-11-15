"use client";
import { FormEvent, useState } from "react";
import { Upload, CheckCircle2, CalendarDays } from "lucide-react";
import { api } from "@/lib/api";
import { ErrorNotice } from "./forms";

export function EvidenceUpload({ caseId }: { caseId: string }) {
  const [error, setError] = useState("");
  const [result, setResult] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const f = new FormData(e.currentTarget);
    const file = f.get("file") as File;
    try {
      if (!file || file.size > 20971520)
        throw new Error("Select a file up to 20 MiB.");
      const bytes = await file.arrayBuffer();
      const hash = Array.from(
        new Uint8Array(await crypto.subtle.digest("SHA-256", bytes)),
      )
        .map((v) => v.toString(16).padStart(2, "0"))
        .join("");
      const grant = await api<{ file_id: string; upload_url: string }>(
        "/files/upload-grants",
        {
          method: "POST",
          headers: { "Idempotency-Key": crypto.randomUUID() },
          body: JSON.stringify({
            case_id: caseId,
            kind: f.get("kind"),
            mime_type: file.type,
            size_bytes: file.size,
            checksum_sha256: hash,
          }),
        },
      );
      const csrf = await api<{ csrf_token: string }>("/auth/csrf");
      const u = new URL(grant.upload_url);
      const res = await fetch(u.pathname + u.search, {
        method: "PUT",
        credentials: "same-origin",
        headers: { "X-CSRFToken": csrf.csrf_token, "Content-Type": file.type },
        body: bytes,
      });
      const r = await res.json();
      if (!res.ok) throw new Error(r.message || "Upload failed.");
      setResult(
        `Evidence ${grant.file_id} · ${r.status}. ${r.status === "clean" ? "The safe image derivative is ready for an authorized workflow." : "The document remains quarantined until processing is available."}`,
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="record-detail">
      <h3>
        <Upload size={19} /> Evidence files
      </h3>
      <p className="muted">
        JPEG and PNG images are processed into safe image derivatives. PDF
        documents remain quarantined until the document scanner is configured.
        Files stay private.
      </p>
      <ErrorNotice error={error} />
      {result && (
        <p className="notice" role="status">
          {result}
        </p>
      )}
      <form onSubmit={submit}>
        <div className="form-grid">
          <label>
            Evidence purpose
            <select name="kind">
              <option value="identity">Seller authority / identity</option>
              <option value="inspection">Inspection</option>
              <option value="contract">Contract</option>
              <option value="payment">Payment evidence</option>
              <option value="delivery">Delivery</option>
              <option value="claim">Claim</option>
            </select>
          </label>
          <label>
            Evidence file
            <input
              name="file"
              type="file"
              accept="image/png,image/jpeg,application/pdf"
              required
            />
          </label>
        </div>
        <button className="button outline" disabled={busy}>
          {busy ? "Processing evidence…" : "Upload private evidence"}{" "}
          <Upload size={16} />
        </button>
      </form>
    </div>
  );
}

export function Booking({ lead }: { lead: { id: string; status: string } }) {
  const [branches, setBranches] = useState<{ id: string; name: string }[]>([]);
  const [slots, setSlots] = useState<
    { id: string; starts_at: string; available: boolean; timezone: string }[]
  >([]);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [branch, setBranch] = useState("");
  async function begin() {
    try {
      setBranches(
        (await api<{ items: { id: string; name: string }[] }>("/branches"))
          .items,
      );
      setOpen(true);
    } catch (e) {
      setError((e as Error).message);
    }
  }
  async function choose(id: string) {
    setBranch(id);
    try {
      setSlots(
        (await api<{ items: typeof slots }>("/branches/" + id + "/slots"))
          .items,
      );
    } catch (e) {
      setError((e as Error).message);
    }
  }
  async function book(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const f = new FormData(e.currentTarget);
    try {
      await api("/appointments", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          lead_id: lead.id,
          branch_id: branch,
          slot_id: f.get("slot_id"),
        }),
      });
      setNote(
        "Your appointment is confirmed. Open appointments to review its details.",
      );
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="record-detail">
      <h3>
        <CalendarDays size={19} /> Choose your inspection
      </h3>
      <ErrorNotice error={error} />
      {note ? (
        <p className="notice" role="status">
          {note}
        </p>
      ) : open ? (
        <form onSubmit={book}>
          <label>
            Studio
            <select
              value={branch}
              onChange={(e) => choose(e.target.value)}
              required
            >
              <option value="">Choose a studio</option>
              {branches.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            Available time
            <select name="slot_id" required>
              <option value="">Choose an available slot</option>
              {slots
                .filter((s) => s.available)
                .map((s) => (
                  <option key={s.id} value={s.id}>
                    {new Date(s.starts_at).toLocaleString("en-GB", {
                      timeZone: s.timezone,
                    })}{" "}
                    · {s.timezone}
                  </option>
                ))}
            </select>
          </label>
          <button className="button primary" disabled={busy}>
            {busy ? "Confirming…" : "Confirm appointment"}
          </button>
        </form>
      ) : (
        <button
          className="button primary"
          onClick={begin}
          disabled={!["eligible", "in_progress"].includes(lead.status)}
        >
          View available appointments
        </button>
      )}
    </div>
  );
}

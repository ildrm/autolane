"use client";
import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  CheckCircle2,
  ChevronLeft,
  LoaderCircle,
  ShieldCheck,
} from "lucide-react";
import { api, ApiError, money } from "@/lib/api";

export function ErrorNotice({ error }: { error: string }) {
  return error ? (
    <div className="notice error" role="alert">
      {error}
    </div>
  ) : null;
}
export function AuthForm() {
  const [mode, setMode] = useState<
    "login" | "register" | "verify" | "recovery"
  >("login");
  const [challenge, setChallenge] = useState("");
  const [error, setError] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setNote("");
    setBusy(true);
    const f = Object.fromEntries(new FormData(e.currentTarget));
    try {
      if (mode === "register") {
        const r = await api<{ message: string }>("/auth/register", {
          method: "POST",
          body: JSON.stringify(f),
        });
        setNote(
          r.message + " Local development emails are saved in .local/mail.",
        );
      } else if (mode === "verify") {
        await api("/auth/verify-email", {
          method: "POST",
          body: JSON.stringify(f),
        });
        setNote("Email verified. You can sign in.");
        setMode("login");
      } else if (mode === "recovery") {
        await api("/auth/recovery", {
          method: "POST",
          body: JSON.stringify(f),
        });
        setNote(
          "If the account is eligible, recovery instructions have been sent.",
        );
      } else {
        const r = await api<{ challenge_id?: string }>(
          challenge ? "/auth/challenges/complete" : "/auth/login",
          {
            method: "POST",
            body: JSON.stringify(
              challenge
                ? { challenge_id: challenge, method: "totp", response: f.code }
                : f,
            ),
          },
        );
        if (r.challenge_id) setChallenge(r.challenge_id);
        else location.assign("/account");
      }
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="auth-layout">
      <div className="auth-story">
        <div className="eyebrow">YOUR JOURNEY, IN ONE PLACE</div>
        <h1>
          A little clarity.
          <br />A lot of <em>possibility.</em>
        </h1>
        <p>
          Follow your sale, find your next car and stay close to every important
          detail.
        </p>
        <img
          src="/vehicles/car-2.svg"
          alt="Original representative automotive artwork"
          width="960"
          height="600"
        />
      </div>
      <div className="form-card">
        <ShieldCheck size={28} />
        <h2>
          {challenge
            ? "Verify your identity"
            : mode === "register"
              ? "Make room for what’s next."
              : mode === "verify"
                ? "Verify your email"
                : mode === "recovery"
                  ? "Recover your account"
                  : "Welcome back."}
        </h2>
        <p>
          {challenge
            ? "Enter the six-digit code from your authenticator."
            : "Your next chapter is just a step away."}
        </p>
        <ErrorNotice error={error} />
        {note && (
          <p className="notice" role="status">
            {note}
          </p>
        )}
        <form onSubmit={submit}>
          {challenge ? (
            <label>
              Authenticator code
              <input
                name="code"
                inputMode="numeric"
                pattern="[0-9]{6}"
                autoComplete="one-time-code"
                required
              />
            </label>
          ) : mode === "verify" ? (
            <>
              <label>
                Verification ID
                <input name="challenge_id" required />
              </label>
              <label>
                Verification token
                <input name="token" required />
              </label>
            </>
          ) : (
            <>
              {mode === "register" && (
                <label>
                  Your name
                  <input name="name" autoComplete="name" required />
                </label>
              )}
              <label>
                Email address
                <input
                  name={mode === "login" ? "username" : "email"}
                  type="email"
                  autoComplete="email"
                  required
                />
              </label>
              {mode !== "recovery" && (
                <label>
                  Password
                  <input
                    name="password"
                    type="password"
                    minLength={12}
                    autoComplete={
                      mode === "register" ? "new-password" : "current-password"
                    }
                    required
                  />
                </label>
              )}
            </>
          )}
          <button className="button primary full" disabled={busy}>
            {busy ? (
              <LoaderCircle className="spin" size={17} />
            ) : (
              <>
                {challenge
                  ? "Verify & continue"
                  : mode === "login"
                    ? "Sign in"
                    : mode === "register"
                      ? "Create account"
                      : mode === "verify"
                        ? "Verify email"
                        : "Send recovery instructions"}{" "}
                <ArrowRight size={17} />
              </>
            )}
          </button>
        </form>
        {!challenge && (
          <div className="auth-options">
            <button
              onClick={() => {
                setMode(mode === "register" ? "login" : "register");
                setError("");
                setNote("");
              }}
            >
              {mode === "register"
                ? "Already have an account? Sign in"
                : "New here? Create an account"}
            </button>
            <button onClick={() => setMode("recovery")}>
              Forgot password?
            </button>
            <button onClick={() => setMode("verify")}>Verify email</button>
          </div>
        )}
        <small className="muted">
          Local development · Staff accounts require an authenticator code.
          Development account details are in .local/development-accounts.json.
        </small>
      </div>
    </section>
  );
}

type Tax = { id: string; name: string; kind: string; parent_id: string | null };
type Lead = { id: string; status: string; version: number };
export function SellForm() {
  const [tax, setTax] = useState<Tax[]>([]);
  const [make, setMake] = useState("");
  const [step, setStep] = useState(0);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [lead, setLead] = useState<Lead>();
  useEffect(() => {
    api<{ items: Tax[] }>("/vehicle-taxonomy")
      .then((x) => setTax(x.items))
      .catch((e) => setError(e.message));
  }, []);
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const f = Object.fromEntries(new FormData(e.currentTarget));
    try {
      const r = await api<Lead>("/seller-leads", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          vehicle: {
            make_id: f.make_id,
            model_id: f.model_id,
            year: Number(f.year),
            mileage: Number(f.mileage),
            mileage_unit: f.mileage_unit,
          },
          contact: { name: f.name, phone: f.phone, email: f.email },
          consent: {
            notice_version: "development-service-v1",
            purpose: "seller_intake",
            accepted: true,
          },
        }),
      });
      setLead(r);
      setStep(1);
    } catch (e) {
      setError(
        (e as ApiError).status === 401
          ? "Sign in to save your selling request. Your vehicle details stay in this form."
          : (e as Error).message,
      );
    } finally {
      setBusy(false);
    }
  }
  async function confirm() {
    if (!lead) return;
    setBusy(true);
    try {
      const r = await api<Lead>(`/seller-leads/${lead.id}/transitions`, {
        method: "POST",
        headers: {
          "Idempotency-Key": crypto.randomUUID(),
          "If-Match": `"${lead.version}"`,
        },
        body: JSON.stringify({
          action: "submit",
          reason: "Seller submits vehicle for qualification",
        }),
      });
      setLead(r);
      setStep(2);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="section selling">
      <div className="eyebrow">A GOOD NEXT STEP</div>
      <h1>
        Let’s get to know <em>your car.</em>
      </h1>
      <p className="lead-text">
        A few details. A professional inspection. An offer you can consider.
      </p>
      <div className="form-shell">
        <aside>
          <div className={step === 0 ? "active-step" : ""}>
            <span>01</span> Your car & contact
          </div>
          <div className={step === 1 ? "active-step" : ""}>
            <span>02</span> Review & submit
          </div>
          <div className={step === 2 ? "active-step" : ""}>
            <span>03</span> Your next steps
          </div>
          <p>
            Have an account?
            <br />
            <Link href="/sign-in">
              Sign in to save your request <ArrowRight size={15} />
            </Link>
          </p>
        </aside>
        <div className="form-main">
          <ErrorNotice error={error} />
          {step === 0 ? (
            <form onSubmit={submit}>
              <h2>The essentials.</h2>
              <div className="form-grid">
                <label>
                  Make
                  <select
                    name="make_id"
                    value={make}
                    onChange={(e) => setMake(e.target.value)}
                    required
                  >
                    <option value="">Choose a make</option>
                    {tax
                      .filter((t) => t.parent_id === null)
                      .map((t) => (
                        <option key={t.id} value={t.id}>
                          {t.name}
                        </option>
                      ))}
                  </select>
                </label>
                <label>
                  Model
                  <select name="model_id" required key={make}>
                    <option value="">Choose a model</option>
                    {tax
                      .filter((t) => t.parent_id === make)
                      .map((t) => (
                        <option key={t.id} value={t.id}>
                          {t.name}
                        </option>
                      ))}
                  </select>
                </label>
                <label>
                  Model year
                  <input
                    name="year"
                    type="number"
                    min="1886"
                    max={new Date().getFullYear() + 1}
                    required
                  />
                </label>
                <label>
                  Mileage
                  <input
                    name="mileage"
                    type="number"
                    min="0"
                    max="10000000"
                    required
                  />
                </label>
                <label>
                  Distance unit
                  <select name="mileage_unit">
                    <option value="km">Kilometres</option>
                    <option value="mi">Miles</option>
                  </select>
                </label>
              </div>
              <h3>How can we reach you?</h3>
              <div className="form-grid">
                <label>
                  Your name
                  <input name="name" autoComplete="name" required />
                </label>
                <label>
                  Phone number
                  <input
                    name="phone"
                    type="tel"
                    autoComplete="tel"
                    required
                    minLength={5}
                  />
                </label>
                <label>
                  Email address
                  <input
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                  />
                </label>
              </div>
              <label className="check-label">
                <input type="checkbox" required /> I acknowledge the development
                service notice and agree to use these details for my selling
                request.
              </label>
              <p className="muted">
                This local installation is for development. No binding sale or
                payment is created.
              </p>
              <button className="button primary" disabled={busy}>
                {busy ? "Saving…" : "Save & review"} <ArrowRight size={18} />
              </button>
            </form>
          ) : step === 1 ? (
            <div>
              <div className="success-icon">
                <CheckCircle2 />
              </div>
              <h2>Your request is saved.</h2>
              <p>
                Submit it for qualification. An assigned advisor reviews seller
                authority before you can book an inspection.
              </p>
              <dl>
                <dt>Request reference</dt>
                <dd>{lead?.id}</dd>
                <dt>Status</dt>
                <dd>{lead?.status}</dd>
              </dl>
              <button
                className="button primary"
                onClick={confirm}
                disabled={busy}
              >
                Submit for review <ArrowRight size={18} />
              </button>
            </div>
          ) : (
            <div>
              <CheckCircle2 size={42} />
              <h2>You’re on your way.</h2>
              <p>
                Your request is submitted. Track its qualification and book an
                available appointment from your dashboard when eligible.
              </p>
              <Link href="/account" className="button primary">
                View my dashboard <ArrowRight size={18} />
              </Link>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export function Inquiry({ listingId }: { listingId: string }) {
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    const f = Object.fromEntries(new FormData(e.currentTarget));
    try {
      await api("/purchase-requests", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          listing_id: listingId,
          contact: { name: f.name, phone: f.phone, email: f.email },
          consent: {
            notice_version: "development-service-v1",
            purpose: "buyer_inquiry",
            accepted: true,
          },
        }),
      });
      setSent(true);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="form-card">
      <h2>Take the next step.</h2>
      <p>Ask about this car. An inquiry does not reserve the vehicle.</p>
      <ErrorNotice error={error} />
      {sent ? (
        <div className="notice" role="status">
          Your inquiry is saved. Follow it in your account.
        </div>
      ) : (
        <form onSubmit={submit}>
          <label>
            Your name
            <input name="name" required />
          </label>
          <label>
            Phone
            <input name="phone" type="tel" required minLength={5} />
          </label>
          <label>
            Email
            <input name="email" type="email" required />
          </label>
          <label className="check-label">
            <input type="checkbox" required /> I agree to use my details for
            this inquiry.
          </label>
          <button className="button primary full" disabled={busy}>
            {busy ? "Sending…" : "Enquire about this car"} <ArrowUpRightIcon />
          </button>
          <small>Sign in to submit and track your request.</small>
        </form>
      )}
    </div>
  );
}
function ArrowUpRightIcon() {
  return <ArrowRight size={17} />;
}

export function ValuationForm() {
  const [result, setResult] = useState("");
  return (
    <div className="form-card">
      <h2>A considered estimate starts with real evidence.</h2>
      <p>
        A licensed market data source has not been configured for this
        installation. An individual inspection and pricing review can still be
        arranged.
      </p>
      <Link className="button primary" href="/sell">
        Arrange an inspection <ArrowRight size={17} />
      </Link>
    </div>
  );
}

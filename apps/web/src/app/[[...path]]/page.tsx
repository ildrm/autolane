import { notFound } from "next/navigation";
import Link from "next/link";
import {
  ArrowUpRight,
  MapPin,
  Clock,
  ShieldCheck,
  ArrowRight,
} from "lucide-react";
import {
  Home,
  Browse,
  serverApi,
  type Listing,
} from "@/components/marketplace";
import { AuthForm, SellForm, Inquiry, ValuationForm } from "@/components/forms";
import { Workspace } from "@/components/workspace";
import { money } from "@/lib/api";
type Props = {
  params: Promise<{ path?: string[] }>;
  searchParams: Promise<Record<string, string>>;
};
export async function generateMetadata({ params }: Props) {
  const p = (await params).path || [];
  const privatePage = ["account", "ops", "dealer"].includes(p[0]);
  return {
    title: p.length
      ? p.map((v) => v.replaceAll("-", " ")).join(" · ")
      : "A clearer road forward",
    robots: privatePage ? { index: false, follow: false } : undefined,
  };
}
export default async function Page({ params, searchParams }: Props) {
  const p = (await params).path || [];
  const route = p.join("/");
  if (!route) return <Home />;
  if (route === "buy") return <Browse query={await searchParams} />;
  if (route === "sell" || route.startsWith("sell/")) return <SellForm />;
  if (route === "sign-in") return <AuthForm />;
  if (["account", "ops", "dealer"].includes(p[0])) return <Workspace />;
  if (route === "value")
    return (
      <section className="section narrow">
        <div className="eyebrow">KNOW WHERE YOU STAND</div>
        <h1>
          A clearer picture of <em>your car’s value.</em>
        </h1>
        <ValuationForm />
      </section>
    );
  if (route === "branches" || p[0] === "branches") {
    const { items } = await serverApi<{
      items: {
        id: string;
        name: string;
        address: string;
        city: string;
        timezone: string;
      }[];
    }>("/branches", { items: [] });
    return (
      <section className="section">
        <div className="eyebrow">MAKE YOURSELF AT HOME</div>
        <h1>
          Your local <em>Autolane studio.</em>
        </h1>
        <p className="lead-text">Meet the people behind your next step.</p>
        <div className="branch-grid">
          {items.map((b) => (
            <article className="form-card" key={b.id}>
              <MapPin size={30} />
              <h2>{b.name}</h2>
              <p>{b.address}</p>
              <p>
                <Clock size={15} /> Times shown in {b.timezone}
              </p>
              <Link href="/account" className="button primary">
                View available appointments <ArrowUpRight size={17} />
              </Link>
            </article>
          ))}
        </div>
      </section>
    );
  }
  if (p[0] === "cars" && p[1]) {
    const car = await serverApi<Listing | null>(
      "/public-listings/" + p[1],
      null,
    );
    if (!car) notFound();
    return (
      <section className="section">
        <Link className="text-button" href="/buy">
          ← Back to cars
        </Link>
        <div className="detail-layout">
          <div>
            <div className="eyebrow">YOUR NEXT CHAPTER</div>
            <h1>
              {car.vehicle.make_name}
              <br />
              <em>{car.vehicle.model_name}</em>
            </h1>
            <p>
              {car.vehicle.year} · {car.vehicle.mileage.toLocaleString("en")} km
              · {car.vehicle.fuel_type}
            </p>
            <img
              className="detail-image"
              src={car.media[0]?.url}
              alt={car.media[0]?.alt}
              width="960"
              height="600"
            />
            <div className="heading-row">
              <h2>{money(car.price_minor, car.currency)}</h2>
              <span className="status available">{car.status}</span>
            </div>
            <h3>A clear view of the details.</h3>
            <p>{car.condition_summary}</p>
            <p className="muted">
              Representative illustration. This is a fictional development
              listing.
            </p>
            <div className="spec-grid">
              {Object.entries(car.vehicle)
                .filter(([k]) => !k.endsWith("_id"))
                .map(([k, v]) => (
                  <div key={k}>
                    <small>{k.replaceAll("_", " ")}</small>
                    <strong>{v}</strong>
                  </div>
                ))}
            </div>
          </div>
          <Inquiry listingId={car.id} />
        </div>
      </section>
    );
  }
  if (p[0] === "journal" && p[1]) {
    const a = await serverApi<{
      title: string;
      blocks: { kind: string; text?: string }[];
    } | null>("/published-content/" + p[1], null);
    if (!a) notFound();
    return (
      <article className="section narrow article">
        <div className="eyebrow">THE AUTOLANE JOURNAL</div>
        <h1>{a.title}</h1>
        {a.blocks.map((b, i) =>
          b.kind === "heading" ? (
            <h2 key={i}>{b.text}</h2>
          ) : (
            <p key={i}>{b.text}</p>
          ),
        )}
        <Link href="/sell" className="button primary">
          Start your selling journey <ArrowRight size={17} />
        </Link>
      </article>
    );
  }
  if (route === "dealers")
    return (
      <section className="section narrow">
        <div className="eyebrow">BETTER TOGETHER</div>
        <h1>
          A clearer way to <em>source your stock.</em>
        </h1>
        <p className="lead-text">
          Verified organizations. Published inspections. Server-authoritative
          bidding.
        </p>
        <div className="form-card">
          <ShieldCheck />
          <h2>Join the dealer network.</h2>
          <p>
            Create an account, provide your business evidence and complete an
            independent review. Approval and bidding authority are separate
            permissions.
          </p>
          <Link href="/sign-in" className="button primary">
            Create your account <ArrowUpRight size={17} />
          </Link>
        </div>
      </section>
    );
  if (route === "help")
    return (
      <section className="section narrow">
        <div className="eyebrow">WE’RE HERE FOR YOUR NEXT STEP</div>
        <h1>
          How can we <em>help?</em>
        </h1>
        <div className="form-card">
          <h2>Your case, clearly tracked.</h2>
          <p>
            Open your account to create a support request and follow its
            resolution.
          </p>
          <Link href="/account" className="button primary">
            Open support <ArrowUpRight size={17} />
          </Link>
        </div>
        <Link href="/journal/selling-guide">Read the selling guide →</Link>
      </section>
    );
  notFound();
}

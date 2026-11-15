import Link from "next/link";
import {
  ArrowUpRight,
  ArrowRight,
  Check,
  SlidersHorizontal,
  ShieldCheck,
  CalendarDays,
  Search,
  Gauge,
  Fuel,
  Settings2,
} from "lucide-react";
import { money } from "@/lib/api";
export type Listing = {
  id: string;
  title: string;
  slug: string;
  price_minor: number;
  currency: string;
  status: string;
  vehicle: {
    make_name: string;
    model_name: string;
    year: number;
    mileage: number;
    fuel_type: string;
    transmission: string;
  };
  media: { url: string; alt: string }[];
  condition_summary: string;
  region_name: string;
};
export async function serverApi<T>(path: string, fallback: T): Promise<T> {
  try {
    const r = await fetch(
      `${process.env.API_ORIGIN || "http://127.0.0.1:8000"}/v1${path}`,
      { cache: "no-store", signal: AbortSignal.timeout(5000) },
    );
    return r.ok ? await r.json() : fallback;
  } catch {
    return fallback;
  }
}
export function VehicleCard({ car }: { car: Listing }) {
  return (
    <Link href={"/cars/" + car.slug} className="vehicle-card">
      <div className="vehicle-image">
        <img
          src={car.media[0]?.url || "/vehicles/car-0.svg"}
          alt={car.media[0]?.alt || "Representative automotive illustration"}
          width="960"
          height="600"
          loading="lazy"
        />
        <span className="image-tag">DEVELOPMENT LISTING</span>
        <span className="round-arrow">
          <ArrowUpRight size={19} />
        </span>
      </div>
      <div className="vehicle-info">
        <div className="vehicle-title">
          <h3>
            {car.vehicle.make_name} {car.vehicle.model_name}
          </h3>
          <span>{car.vehicle.year}</span>
        </div>
        <p className="vehicle-specs">
          {new Intl.NumberFormat("en").format(car.vehicle.mileage)} km <b>·</b>{" "}
          {car.vehicle.fuel_type} <b>·</b> {car.vehicle.transmission}
        </p>
        <div className="vehicle-bottom">
          <strong>{money(car.price_minor, car.currency)}</strong>
          <span>{car.region_name}</span>
        </div>
      </div>
    </Link>
  );
}
export async function Home() {
  const { items } = await serverApi<{ items: Listing[] }>("/listings", {
    items: [],
  });
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <div className="eyebrow">
            <span /> THE NEXT CHAPTER STARTS HERE
          </div>
          <h1>
            Your next car.
            <br />A better <em>journey.</em>
          </h1>
          <p>
            Buy with clarity. Sell with confidence.
            <br />A thoughtful way to move forward.
          </p>
          <div className="hero-buttons">
            <Link href="/buy" className="button primary">
              Find my next car <ArrowUpRight size={19} />
            </Link>
            <Link href="/sell" className="button outline">
              Sell my car <ArrowRight size={18} />
            </Link>
          </div>
          <div className="hero-reassurance">
            <span>
              <Check size={15} /> Professional inspection
            </span>
            <span>
              <Check size={15} /> Clear next steps
            </span>
          </div>
        </div>
        <div className="hero-art">
          <div className="orbit orbit1" />
          <div className="orbit orbit2" />
          <span className="art-label">MADE FOR WHAT’S NEXT</span>
          <img
            src="/vehicles/car-0.svg"
            alt="Original automotive illustration showing a modern SUV"
            width="960"
            height="600"
            fetchPriority="high"
          />
          <div className="floating-card">
            <ShieldCheck size={29} />
            <div>
              <strong>Confidence comes standard.</strong>
              <span>A clear view of every important detail.</span>
            </div>
          </div>
          <span className="art-caption">Original representative artwork</span>
        </div>
      </section>
      <section className="journey-strip">
        <span>A CAR IS MORE THAN A PURCHASE.</span>
        <p>
          It’s your everyday. Your getaways. <em>Your next chapter.</em>
        </p>
        <ArrowUpRight size={31} />
      </section>
      <section className="section inventory">
        <div className="section-heading">
          <div className="eyebrow">FIND YOUR FIT</div>
          <div className="heading-row">
            <h2>Something that moves you.</h2>
            <Link href="/buy">
              Explore all cars <ArrowUpRight size={18} />
            </Link>
          </div>
          <p>
            Explore the local development inventory. Every example is clearly
            labeled.
          </p>
        </div>
        <div className="vehicle-grid">
          {items.slice(0, 3).map((car) => (
            <VehicleCard key={car.id} car={car} />
          ))}
          {!items.length && (
            <div className="empty">
              <Search />
              <h3>No published vehicles yet.</h3>
              <p>Published inventory will appear here when it is available.</p>
            </div>
          )}
        </div>
      </section>
      <section className="sell-banner">
        <div>
          <div className="eyebrow light">
            A FRESH START, WITHOUT THE FRICTION
          </div>
          <h2>
            Your car has a story.
            <br />
            Let’s write its next chapter.
          </h2>
          <p>
            Tell us about your car. Choose an inspection.
            <br />
            Review your offer, on your terms.
          </p>
          <Link href="/sell" className="button cream">
            Start selling <ArrowUpRight size={18} />
          </Link>
        </div>
        <div className="steps">
          {[
            [
              "01",
              "Tell us about your car",
              "A few details to get the journey started.",
            ],
            [
              "02",
              "Meet us for an inspection",
              "Choose a time and a studio that works for you.",
            ],
            [
              "03",
              "Review your offer",
              "See the details. Decide when you’re ready.",
            ],
          ].map(([n, t, p]) => (
            <div key={n}>
              <span>{n}</span>
              <article>
                <h3>{t}</h3>
                <p>{p}</p>
              </article>
            </div>
          ))}
        </div>
      </section>
      <section className="section values">
        <div className="eyebrow">THE AUTOLANE APPROACH</div>
        <h2>More clarity. Less guesswork.</h2>
        <div className="value-grid">
          {[
            [
              ShieldCheck,
              "Details that matter",
              "Review condition reports and keep important evidence in one place.",
            ],
            [
              CalendarDays,
              "A process that respects your time",
              "Book available appointments and follow every step from your account.",
            ],
            [
              ArrowUpRight,
              "Your decision, always",
              "An offer is yours to consider. Contracts, payment and handover stay clearly separate.",
            ],
          ].map(([Icon, t, p], i) => {
            const I = Icon as typeof ShieldCheck;
            return (
              <article key={i}>
                <I size={28} />
                <h3>{t as string}</h3>
                <p>{p as string}</p>
              </article>
            );
          })}
        </div>
      </section>
    </>
  );
}
export async function Browse({ query }: { query: Record<string, string> }) {
  const params = new URLSearchParams(query);
  const { items } = await serverApi<{ items: Listing[] }>(
    "/listings?" + params,
    { items: [] },
  );
  return (
    <section className="section browse">
      <div className="eyebrow">THE RIGHT CAR. THE RIGHT NEXT STEP.</div>
      <h1>
        Find your kind of <em>drive.</em>
      </h1>
      <p className="lead-text">
        A considered collection. A clear path to your next car.
      </p>
      <form className="filterbar" action="/buy">
        <label>
          Make
          <input name="make" placeholder="Any make" defaultValue={query.make} />
        </label>
        <label>
          Year from
          <input
            name="year_min"
            type="number"
            min="1886"
            max="2100"
            placeholder="Any year"
            defaultValue={query.year_min}
          />
        </label>
        <label>
          Price up to (EUR)
          <input
            name="price_max_minor"
            type="number"
            min="1"
            placeholder="Amount in cents"
            defaultValue={query.price_max_minor}
          />
        </label>
        <input type="hidden" name="currency" value="EUR" />
        <button className="button primary">
          <SlidersHorizontal size={17} /> Apply filters
        </button>
      </form>
      <div className="results-label">
        {items.length} vehicles{" "}
        <span>Development inventory · Representative illustrations</span>
      </div>
      <div className="vehicle-grid">
        {items
          .filter(
            (c) =>
              !query.make ||
              c.vehicle.make_name
                .toLowerCase()
                .includes(query.make.toLowerCase()),
          )
          .map((car) => (
            <VehicleCard key={car.id} car={car} />
          ))}
        {!items.length && (
          <div className="empty">
            No vehicles match these filters.{" "}
            <Link href="/buy">Clear filters</Link>
          </div>
        )}
      </div>
    </section>
  );
}

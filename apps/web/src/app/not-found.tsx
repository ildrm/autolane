import Link from "next/link";
export default function NotFound() {
  return (
    <section className="section narrow">
      <div className="eyebrow">LET’S FIND YOUR WAY</div>
      <h1>
        This road doesn’t
        <br />
        lead <em>anywhere.</em>
      </h1>
      <p>The page may have moved or is not available.</p>
      <Link className="button primary" href="/">
        Back to Autolane →
      </Link>
    </section>
  );
}

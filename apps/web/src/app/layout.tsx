import type { Metadata } from "next";
import Link from "next/link";
import { ArrowUpRight, MoveRight, ShieldCheck } from "lucide-react";
import "./globals.css";
export const metadata: Metadata = {
  title: {
    default: "Autolane — A clearer road forward",
    template: "%s | Autolane",
  },
  description:
    "Discover your next car, arrange a professional inspection, or sell with a clear, guided process.",
};
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" dir="ltr">
      <body>
        <a className="skip" href="#main">
          Skip to content
        </a>
        <div className="devbar">
          LOCAL DEVELOPMENT{" "}
          <span>Fictional listings · External payments disabled</span>
        </div>
        <header className="header">
          <Link className="brand" href="/">
            <span className="brandmark">a.</span>autolane
            <span className="branddot">®</span>
          </Link>
          <nav aria-label="Main navigation">
            <Link href="/buy">Buy a car</Link>
            <Link href="/sell">Sell your car</Link>
            <Link href="/value">Car valuation</Link>
            <Link href="/branches">Our studios</Link>
          </nav>
          <details className="public-mobile-nav"><summary aria-label="Open navigation">Menu</summary><nav aria-label="Mobile navigation"><Link href="/buy">Buy a car</Link><Link href="/sell">Sell your car</Link><Link href="/value">Car valuation</Link><Link href="/branches">Our studios</Link></nav></details>
      <Link className="login-link" href="/sign-in">
            My Autolane <ArrowUpRight size={17} />
          </Link>
        </header>
        <main id="main">{children}</main>
        <footer>
          <div>
            <Link className="brand" href="/">
              autolane.
            </Link>
            <p>A clearer road forward.</p>
          </div>
          <div>
            <Link href="/sell">Sell your car</Link>
            <Link href="/buy">Find your next car</Link>
            <Link href="/dealers">For dealers</Link>
          </div>
          <div>
            <Link href="/journal/selling-guide">Selling guide</Link>
            <Link href="/help">Help & support</Link>
            <Link href="/account">Your account</Link>
          </div>
          <div className="footer-note">
            <ShieldCheck size={23} />
            <p>
              Every step, clearly explained.
              <br />
              Built in the open. GPL-2.0.
            </p>
          </div>
          <small>
            Autolane · Open source automotive platform · Development
            installation
          </small>
        </footer>
      </body>
    </html>
  );
}

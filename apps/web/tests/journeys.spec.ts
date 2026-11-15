import { test, expect } from "@playwright/test";

test("public marketplace renders real inventory and works at mobile width", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: /Your next car/ }),
  ).toBeVisible();
  await expect(page.locator(".vehicle-card")).toHaveCount(3);
  await page.setViewportSize({ width: 390, height: 844 });
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBeTruthy();
  await page.getByRole("link", { name: "Find my next car" }).click();
  await expect(page.locator(".vehicle-card")).toHaveCount(6);
  await page.locator(".vehicle-card").first().click();
  await expect(
    page.getByRole("heading", { name: "Take the next step." }),
  ).toBeVisible();
  expect(errors).toEqual([]);
});

test("seller signs in, submits a car and reads persisted CRM state", async ({
  page,
}) => {
  await page.goto("/sign-in");
  await page
    .getByLabel("Email address", { exact: true })
    .fill("seller@example.test");
  await page
    .getByLabel("Password", { exact: true })
    .fill(process.env.SEED_PASSWORD || "Development-only-2026!");
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page.waitForURL("**/account");
  await expect(
    page.getByRole("heading", { name: "Seller dashboard", exact: true }),
  ).toBeVisible();
  await page.goto("/sell");
  await page
    .getByRole("combobox", { name: "Make", exact: true })
    .selectOption({ label: "Volvo" });
  await page
    .getByRole("combobox", { name: "Model", exact: true })
    .selectOption({ label: "XC60" });
  await page.getByLabel("Model year", { exact: true }).fill("2021");
  await page.getByLabel("Mileage", { exact: true }).fill("34500");
  await page
    .getByLabel("Your name", { exact: true })
    .fill("Development Seller");
  await page.getByLabel("Phone number", { exact: true }).fill("+441234567890");
  await page
    .getByLabel("Email address", { exact: true })
    .fill("seller@example.test");
  await page.locator("input[type=checkbox]").check();
  await page.getByRole("button", { name: "Save & review" }).click();
  await expect(
    page.getByRole("heading", { name: "Your request is saved." }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Submit for review" }).click();
  await expect(
    page.getByRole("heading", { name: "You’re on your way." }),
  ).toBeVisible();
  await page.getByRole("link", { name: "View my dashboard" }).click();
  await expect(
    page.locator("tbody").getByText("Submitted", { exact: true }).first(),
  ).toBeVisible();
  const r = await page.request.get("/v1/seller-leads");
  expect(r.ok()).toBeTruthy();
  const body = await r.json();
  expect(
    body.items.some((r: { status: string }) => r.status === "submitted"),
  ).toBeTruthy();
});

test("dealer opens an authorized report and places a persisted bid", async ({
  page,
}) => {
  await page.goto("/sign-in");
  await page
    .getByLabel("Email address", { exact: true })
    .fill("dealer@example.test");
  await page
    .getByLabel("Password", { exact: true })
    .fill(process.env.SEED_PASSWORD || "Development-only-2026!");
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await page.waitForURL("**/account");
  await expect(
    page.getByRole("heading", { name: "Dealer portal", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Review", exact: true })
    .first()
    .click();
  await page.getByRole("button", { name: "View inspection report" }).click();
  await expect(
    page.getByText("Body and paint condition", { exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Place bid", exact: true }),
  ).toBeEnabled();
  await page.getByRole("button", { name: "Place bid", exact: true }).click();
  await expect(page.getByRole("status")).toContainText("Bid accepted. Receipt");
  const response = await page.request.get("/v1/bid-commands");
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(
    body.items.some((r: { status: string }) => r.status === "accepted"),
  ).toBeTruthy();
});

test("private APIs and workspaces reject unauthenticated users", async ({
  page,
}) => {
  const response = await page.request.get("/v1/workspace");
  expect(response.status()).toBe(401);
  await page.goto("/ops/finance");
  await expect(
    page.getByRole("link", { name: "Sign in to continue" }),
  ).toBeVisible();
});

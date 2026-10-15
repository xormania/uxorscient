import { test as base, expect } from '@playwright/test';

const test = base.extend({
    expectedHttpErrors: async ({}, use) => { await use(new Map()); },
    page: async ({ page, expectedHttpErrors }, use) => {
        const failures = [];
        const cspFailures = [];
        page.on('pageerror', (error) => failures.push({ kind: 'page', message: error.message }));
        page.on('console', (message) => {
            if (message.type() === 'error') failures.push({ kind: 'console', message: message.text(), url: message.location().url });
        });
        page.on('requestfailed', (request) => failures.push({ kind: 'request', message: `${request.url()} ${request.failure()?.errorText}` }));
        await page.exposeFunction('__recordCspFailure', (failure) => cspFailures.push(failure));
        await page.addInitScript(() => {
            window.addEventListener('securitypolicyviolation', (event) => window.__recordCspFailure(`${event.violatedDirective}: ${event.blockedURI}`));
        });
        await use(page);
        const unexpected = failures.filter((failure) => {
            // Chromium reports an intentional form-validation HTTP 422 as a resource error.
            // Allow only the explicitly registered response URL once; the test asserts its status separately.
            if (failure.kind === 'console' && expectedHttpErrors.get(failure.url) === 422
                && /^Failed to load resource: the server responded with a status of 422 \(/.test(failure.message)) {
                expectedHttpErrors.delete(failure.url);
                return false;
            }
            return true;
        });
        expect(unexpected, 'Unexpected browser execution failures').toEqual([]);
        expect(cspFailures, 'CSP failures across all visited documents').toEqual([]);
    },
});

// Frame completion is the rendered DOM plus URL; a stream completion is its resulting DOM.
// Ordinary frame/stream updates deliberately do not wait for turbo:load.
test('search, edit validation, save streams and history work in one application', async ({ page, expectedHttpErrors }) => {
    const response = await page.goto('/customers');
    expect(response.headers()['content-security-policy']).toContain("'strict-dynamic'");
    await expect(page.getByRole('heading', { name: 'Customers', exact: true })).toBeVisible();
    await expect(page.locator('#customers-row-1')).toContainText('Ada Lovelace');
    await page.evaluate(() => { window.__documentIdentity = 'original'; });
    await page.getByRole('link', { name: 'Name', exact: true }).click();
    await expect(page).toHaveURL(/dir=desc/);
    await expect(page.locator('#customers-row-4')).toBeVisible();
    await page.getByRole('link', { name: 'Name', exact: true }).click();
    await expect(page).not.toHaveURL(/dir=desc/);
    await expect(page.locator('#customers-row-1')).toBeVisible();

    await page.getByRole('link', { name: 'Page 2', exact: true }).click();
    await expect(page).toHaveURL(/page=2/);
    await expect(page.locator('#customers-row-3')).toContainText('Katherine Johnson');
    await page.goBack();
    await expect(page).not.toHaveURL(/page=2/);
    await expect(page.locator('#customers-row-1')).toBeVisible();
    await page.goForward();
    await expect(page).toHaveURL(/page=2/);
    await expect(page.locator('#customers-row-3')).toBeVisible();
    expect(await page.evaluate(() => window.__documentIdentity)).toBe('original');

    await page.getByRole('searchbox', { name: 'Search', exact: true }).fill('Ada');
    await page.getByRole('button', { name: 'Apply', exact: true }).click();
    await expect(page).toHaveURL(/q=Ada/);
    await expect(page.locator('#customers-row-1')).toBeVisible();
    await expect(page.locator('#customers-row-3')).toHaveCount(0);
    const listUrl = page.url();

    await page.getByRole('link', { name: 'Edit Ada Lovelace', exact: true }).click();
    const dialog = page.getByRole('dialog', { name: 'Edit customer', exact: true });
    await expect(dialog).toBeVisible();
    await expect(dialog.getByRole('textbox', { name: 'Name', exact: true })).toBeFocused();
    await dialog.getByRole('textbox', { name: 'Email', exact: true }).fill('invalid');
    expectedHttpErrors.set(new URL(await dialog.locator('form').getAttribute('action'), page.url()).href, 422);
    const invalid = page.waitForResponse((response) => response.url().includes('/customers/1/edit') && response.request().method() === 'POST');
    await dialog.getByRole('button', { name: 'Save customer' }).click();
    expect((await invalid).status()).toBe(422);
    await expect(dialog.getByRole('textbox', { name: 'Email', exact: true })).toHaveAttribute('aria-invalid', 'true');
    await expect(dialog).toContainText('This value is not a valid email address.');
    await expect(dialog.getByRole('textbox', { name: 'Email', exact: true })).toBeFocused();
    const errorId = await dialog.getByRole('textbox', { name: 'Email', exact: true }).getAttribute('aria-describedby');
    await expect(page.locator(`#${errorId}`)).toContainText('valid email');
    await expect(page).toHaveURL(listUrl);

    await dialog.getByRole('textbox', { name: 'Email', exact: true }).fill('ada.updated@example.test');
    await dialog.getByRole('button', { name: 'Save customer' }).click();
    await expect(dialog).toHaveCount(0);
    await expect(page.locator('#customers-row-1')).toContainText('ada.updated@example.test');
    await expect(page.getByText('Customer saved.', { exact: true })).toHaveCount(1);
    await expect(page.getByRole('link', { name: 'Edit Ada Lovelace', exact: true })).toBeFocused();
    await expect(page).toHaveURL(listUrl);

    await page.goBack();
    await expect(page).toHaveURL(/page=2/);
    await expect(page.locator('#customers-row-3')).toBeVisible();
    await expect(page.getByRole('dialog')).toHaveCount(0);
    await page.goForward();
    await expect(page).toHaveURL(listUrl);
    await expect(page.getByRole('searchbox', { name: 'Search', exact: true })).toHaveValue('Ada');
    await expect(page.locator('#customers-row-1')).toContainText('ada.updated@example.test');
    await expect(page.getByText('Customer saved.', { exact: true })).toHaveCount(1);
    await page.reload();
    await expect(page.locator('#customers-row-1')).toContainText('ada.updated@example.test');
});

test('ordinary browser submission has server validation and a redirect after saving', async ({ browser }) => {
    const context = await browser.newContext({ javaScriptEnabled: false });
    const page = await context.newPage();
    await page.goto('/customers/1/edit');
    await page.getByRole('textbox', { name: 'Email', exact: true }).fill('invalid');
    await page.getByRole('button', { name: 'Save customer' }).click();
    await expect(page.getByRole('textbox', { name: 'Email', exact: true })).toHaveAttribute('aria-invalid', 'true');
    await page.getByRole('textbox', { name: 'Email', exact: true }).fill('ada.plain@example.test');
    const saved = page.waitForResponse((response) => response.url().includes('/customers/1/edit') && response.request().method() === 'POST');
    await page.getByRole('button', { name: 'Save customer' }).click();
    expect((await saved).status()).toBe(303);
    await expect(page).toHaveURL(/\/customers$/);
    await expect(page.locator('#customers-row-1')).toContainText('ada.plain@example.test');
    await context.close();
});

test('a saved row leaving the active search restores focus to search', async ({ page }) => {
    await page.goto('/customers?q=Ada');
    await page.getByRole('link', { name: 'Edit Ada Lovelace', exact: true }).click();
    const dialog = page.getByRole('dialog', { name: 'Edit customer', exact: true });
    await dialog.getByRole('textbox', { name: 'Name', exact: true }).fill('Augusta King');
    await dialog.getByRole('textbox', { name: 'Email', exact: true }).fill('augusta@example.test');
    await dialog.getByRole('button', { name: 'Save customer' }).click();
    await expect(dialog).toHaveCount(0);
    await expect(page.locator('#customers-row-1')).toHaveCount(0);
    await expect(page.getByText('No matching rows', { exact: true })).toBeVisible();
    await expect(page.getByRole('searchbox', { name: 'Search', exact: true })).toBeFocused();
    await expect(page).toHaveURL(/q=Ada/);
    await page.getByRole('searchbox', { name: 'Search', exact: true }).fill('Augusta');
    await page.getByRole('button', { name: 'Apply', exact: true }).click();
    await expect(page.locator('#customers-row-1')).toContainText('Augusta King');
});

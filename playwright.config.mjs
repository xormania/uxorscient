import { defineConfig } from '@playwright/test';

export default defineConfig({
    testDir: './tests/e2e',
    workers: 1,
    retries: 0,
    use: { baseURL: process.env.UXORSCIENT_BASE_URL ?? 'http://127.0.0.1:8765', trace: 'retain-on-failure', launchOptions: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH } : {} },
    webServer: process.env.UXORSCIENT_BASE_URL ? undefined : {
        command: 'php -S 127.0.0.1:8765 -t dev/app/public dev/app/public/index.php',
        url: 'http://127.0.0.1:8765/health',
        reuseExistingServer: false,
        timeout: 30000,
    },
});

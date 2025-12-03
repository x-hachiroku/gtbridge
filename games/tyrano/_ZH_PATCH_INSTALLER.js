const path = require('path');
const { existsSync, cpSync, renameSync, mkdirSync } = require('fs');
const { extractAll } = require('asar');

console.log('Installing...');

const app = path.join(process.cwd(), 'resources', 'app');
const app_asar = path.join(process.cwd(), 'resources', 'app.asar');
const backup = path.join(process.cwd(), '_BACKUP', 'resources', 'app.asar');
const app_patch = path.join(process.cwd(), '_ZH_PATCH_ASSETS', 'app');

if (existsSync(app_asar)) {
    extractAll(app_asar, app);
    mkdirSync(path.dirname(backup), { recursive: true });
    renameSync(app_asar, backup);
}

cpSync(app_patch, app, { recursive: true, force: true });

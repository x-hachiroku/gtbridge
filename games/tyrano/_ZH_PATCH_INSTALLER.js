const path = require('path');
const { cpSync } = require('fs');
const { extractAll } = require('asar');

console.log('Installing...');

const app = path.join(process.cwd(), 'resources', 'app');
const app_asar = path.join(process.cwd(), 'resources', 'app.asar');
const app_patch = path.join(process.cwd(), '_ZH_PATCH_ASSETS', 'app');

extractAll(app_asar, app);

cpSync(app_patch, app, {
    recursive: true,
    force: true
});

console.log('Installed successfully!');

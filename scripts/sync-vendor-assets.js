const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const files = [
    ['node_modules/bootstrap/dist/css/bootstrap.min.css', 'static/vendor/bootstrap/css/bootstrap.min.css'],
    ['node_modules/bootstrap/dist/css/bootstrap.min.css.map', 'static/vendor/bootstrap/css/bootstrap.min.css.map'],
    ['node_modules/bootstrap/dist/js/bootstrap.bundle.min.js', 'static/vendor/bootstrap/js/bootstrap.bundle.min.js'],
    ['node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map', 'static/vendor/bootstrap/js/bootstrap.bundle.min.js.map'],
    ['node_modules/vue/dist/vue.global.js', 'static/vendor/vue/vue.global.js'],
    ['node_modules/vue/dist/vue.global.prod.js', 'static/vendor/vue/vue.global.prod.js'],
];

for (const [src, dest] of files) {
    const srcPath = path.join(root, src);
    const destPath = path.join(root, dest);
    fs.mkdirSync(path.dirname(destPath), { recursive: true });
    fs.copyFileSync(srcPath, destPath);
    console.log(`copied ${src} -> ${dest}`);
}

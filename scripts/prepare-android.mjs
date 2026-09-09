import fs from "fs";

const legacyConfigs = [
  "capacitor.config.ts",
  "capacitor.config.js",
  "capacitor.config.mjs",
  "capacitor.config.cjs"
];

for (const file of legacyConfigs) {
  if (fs.existsSync(file)) {
    fs.rmSync(file, { force: true });
    console.log(`Removed legacy ${file}`);
  }
}

if (fs.existsSync("android")) {
  fs.rmSync("android", { recursive: true, force: true });
  console.log("Removed existing Android project for a clean Capacitor build");
}

if (!fs.existsSync("capacitor.config.json")) {
  console.error("capacitor.config.json is missing.");
  process.exit(1);
}

console.log("Android build workspace prepared. Using capacitor.config.json.");

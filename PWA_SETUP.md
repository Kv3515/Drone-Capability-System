# PWA Setup Guide

## Overview
The Drone Capability System has been configured as a Progressive Web App (PWA). Users can now install it on their mobile devices and use it like a native app.

## Files Added

1. **static/manifest.json** - PWA manifest file defining app metadata, icons, and display settings
2. **static/service-worker.js** - Service worker for offline support and resource caching
3. **static/icon-192.png** - App icon (192x192px) - **TODO: Add this image**
4. **static/icon-512.png** - App icon (512x512px) - **TODO: Add this image**

## Setup Instructions

### 1. Add App Icons

You need to create two PNG icon files:

- `static/icon-192.png` (192x192 pixels) - Used for home screen on phones
- `static/icon-512.png` (512x512 pixels) - Used for splash screen and larger displays

**Recommended approach:**
1. Design or find a suitable icon for the Drone Capability System
2. Export at 192x192px and 512x512px sizes
3. Place both files in the `static/` folder
4. Ensure transparent background for best appearance on all devices

**Quick icon creation options:**
- Use an online PNG generator (e.g., makepng.com)
- Use Figma or Adobe XD
- Use Python PIL library to generate programmatically

### 2. PWA Features Enabled

✅ **Standalone Mode** - App runs without browser chrome (no URL bar)
✅ **Custom Theme Color** - Dark theme (#0E1117) for the status bar
✅ **Service Worker** - Enables offline functionality and resource caching
✅ **Apple iOS Support** - Meta tags for iOS home screen installation
✅ **Manifest** - Defines app name, icons, and display preferences

### 3. How Users Install

**Android:**
1. Open the app in Chrome
2. Tap the menu (three dots)
3. Select "Install app" or "Add to Home screen"
4. Confirm installation
5. App appears on home screen as native app

**iOS:**
1. Open the app in Safari
2. Tap the Share button
3. Select "Add to Home Screen"
4. Name the shortcut and confirm
5. App appears on home screen

### 4. Testing PWA

- **Desktop**: Chrome DevTools → Application tab → Manifest and Service Worker
- **Mobile**: Install on device and test offline functionality
- **Lighthouse**: Run Lighthouse audit in Chrome DevTools to validate PWA configuration

## Configuration Details

### manifest.json Settings

- **name**: Full app name (Drone Capability System)
- **short_name**: Short name for home screen (DroneOps)
- **start_url**: Entry point (/)
- **display**: standalone (removes browser UI)
- **theme_color**: Status bar color (#0E1117)
- **background_color**: App launch background (#0E1117)
- **orientation**: portrait (mobile-optimized)
- **icons**: App icons for different sizes

### Service Worker Features

- Caches essential resources on first visit
- Serves cached content for offline access
- Falls back to network for fresh content when online
- Automatically cleans up old cache versions

## Troubleshooting

**Service Worker not registering?**
- Ensure you're using HTTPS (required for PWA)
- Check browser console for errors
- Verify `/static/service-worker.js` is accessible

**Icons not showing?**
- Ensure PNG files are in `/static/` directory
- Verify file names match manifest.json references
- Check that icons are at least 192x192 and 512x512

**App not installable?**
- Must have valid manifest.json
- Requires HTTPS in production (Render provides this)
- Must have service worker registered
- Should have at least one icon defined

## Deployment on Render

Render automatically serves static files from the `static/` directory when deployed with Streamlit. The PWA will work seamlessly on production with no additional configuration needed.

## Next Steps

1. Create and place `icon-192.png` and `icon-512.png` in the `static/` folder
2. Commit changes to GitHub
3. Deploy to Render
4. Test PWA installation on mobile devices
5. Monitor service worker caching performance

---

For more information on PWAs, visit: https://web.dev/progressive-web-apps/

# REPO VISUAL SYSTEM 2026

## Purpose

This document records the visual design system used for the repository interface. It does not modify protocol logic, benchmark logic, or doctrine. It formalizes presentation.

## Core visual stance

The interface is designed as:

- black chrome base,
- snow-white typography,
- one disciplined signal color,
- high-contrast containment,
- low-noise navigation,
- purposeful micro-motion,
- reduced-motion-safe behavior.

The visual objective is to make the repository feel like a real systems artifact rather than a default GitHub document bundle.

## Palette

- `#050505` — obsidian background
- `#0F0F10` / `#121213` — contained panels
- `#FFFFFF` — headline text and active signal
- `#F1F1F2` — body text
- `#D1D1D4` / `#9A9AA2` — supporting text
- `#FF453A` — signal red for emphasis, warnings, and micro-accents

## Design rules

### 1. White first
Headlines must remain white and crisp. Secondary text remains white-toned, not gray-fogged.

### 2. One accent only
The system avoids decorative rainbow accents. Signal red appears only where emphasis is valuable:
- active states,
- risk-related status,
- structural highlights,
- directional attention.

### 3. Containment over clutter
Key content is framed inside panels and cards to create emphasis without visual noise.

### 4. Motion is supportive
Animation is limited to:
- reveal transitions,
- micro-hover changes,
- scan-line ambience,
- status emphasis.

No animation is allowed to become the message.

### 5. Reduced motion is first-class
All non-essential motion must disappear cleanly when the user prefers reduced motion.

### 6. Accessibility is not optional
Contrast, focus visibility, readable type hierarchy, and non-text component clarity are part of the visual system itself.

## Pages

- `index.html` — premium system entry point
- `system-map.html` — architectural topology
- `protocol-explorer.html` — fast role-level file access
- `benchmark-dashboard.html` — claim governance with visualized metrics
- `doctrine.html` — doctrine corpus navigation
- `404.html` — consistent fallback page

## Visual identity outcome

The target feeling is:
- severe,
- authored,
- premium,
- high-control,
- original,
- non-template,
- publishable.

The design should feel closer to a control-room interface or a research system surface than to an AI product landing page.

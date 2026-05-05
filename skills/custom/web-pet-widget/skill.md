# Skill: web-pet-widget

## Purpose
Add an animated floating mascot companion to a web app, mirroring the desktop pet behavior.

## Trigger Phrases
- "Add the pet", "Put the little mascot on the web app"
- "The app has a dancing emoji character", "Where is the pet?"
- "Add floating animation", "Animated mascot for web"
- "The pet doesn't show on Railway"

## When to Use
- User mentions a "little mascot" or "dancing emoji" from the original app
- Adding a desktop app's animated pet to the web version
- Pet only works in Electron desktop, not in web deployment

## Architecture Overview

The desktop pet uses:
- **State machine** (`petStateMachine.ts`) — manages pet states (idle, thinking, working, done, sleeping, etc.)
- **PetEventBridge** — bridges AI events to pet state changes
- **PetManager** — runs pet as a floating Electron window
- **SVG files** — animated SVG states in `public/pet-states/`

For web, we need:
- **WebPetWidget** — React component with floating, draggable SVG display
- **WebSocket bridge** — backend broadcasts pet state to all web clients
- **PetEventEmitter** — bridges pet state machine → web server → WebSocket

## Steps

### Step 1: Map the Existing Pet States
Check the SVG state files available:
```bash
ls public/pet-states/*.svg | head -30
```
Common states: `idle`, `thinking`, `working`, `done`, `happy`, `error`, `sleeping`, `dozing`, `yawning`, `waking`, `notification`, `attention`, `sweeping`, `juggling`, `carrying`, `building`, `dragging`

### Step 2: Create the WebPetWidget Component
```tsx
// src/renderer/components/WebPetWidget/index.tsx
import React, { useCallback, useEffect, useRef, useState } from 'react';

function WebPetWidget({ size = 160, initialState = 'idle' }) {
  const [petState, setPetState] = useState(initialState);
  const [visible, setVisible] = useState(true);
  const [pos, setPos] = useState({ x: 20, y: 20 });
  const [isDragging, setIsDragging] = useState(false);

  // Self-contained WebSocket connection
  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
    ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.name === 'pet-state') {
        window.dispatchEvent(
          new CustomEvent('alexander-ai:pet-state', { detail: msg.data })
        );
      }
    });
    return () => ws.close();
  }, []);

  // Listen for pet state events
  useEffect(() => {
    const handler = (e: Event) => {
      const { state } = (e as CustomEvent).detail;
      setPetState(state);
    };
    window.addEventListener('alexander-ai:pet-state', handler as any);
    return () => window.removeEventListener('alexander-ai:pet-state', handler as any);
  }, []);

  // Drag-to-move
  const onMouseDown = (e) => { /* drag logic */ };
  const onDoubleClick = () => setVisible(v => !v);

  if (!visible) return null;

  return (
    <div style={{ position: 'fixed', left: pos.x, top: pos.y, width: size, height: size, zIndex: 99999, cursor: 'grab' }}
         onMouseDown={onMouseDown}
         onDoubleClick={onDoubleClick}>
      <object data={`/pet-states/${petState}.svg`} type="image/svg+xml"
              style={{ width: '100%', height: '100%', pointerEvents: 'none' }} />
    </div>
  );
}
export default WebPetWidget;
```

### Step 3: Add Widget to Layout (Non-Desktop Only)
```tsx
// src/renderer/components/layout/Layout.tsx
import WebPetWidget from '@renderer/components/WebPetWidget';

// Only show on web (not Electron desktop)
{!isElectronDesktop && <WebPetWidget size={140} />}
```

### Step 4: Bridge Backend → WebSocket
Create `petEventEmitter.ts`:
```typescript
import { EventEmitter } from 'events';

class PetEventEmitter extends EventEmitter {
  emitStateChange(payload: { state: string; priority?: number }) {
    this.emit('state-change', payload);
  }
}
export const petEventEmitter = new PetEventEmitter();
```

### Step 5: Connect PetManager to PetEventEmitter
In `petManager.ts`:
```typescript
import { petEventEmitter } from './petEventEmitter';

stateMachine.onStateChange((state) => {
  petEventEmitter.emitStateChange({ state });
});
```

### Step 6: Connect WebSocketManager to PetEventEmitter
In `adapter.ts` (web server adapter):
```typescript
import { petEventEmitter } from '../pet/petEventEmitter';
import { WebSocketManager } from './websocket/WebSocketManager';

petEventEmitter.onStateChange(({ state, priority }) => {
  wsManager.broadcastPetState(state, priority);
});
```

### Step 7: Add PetEventBridge Callback
Update `PetEventBridge` to accept an `onStateChange` callback:
```typescript
export class PetEventBridge {
  constructor(
    private sm: PetStateMachine,
    private ticker: PetIdleTicker,
    private onStateChange?: (state: string) => void
  ) {}

  // Call onStateChange on each state transition:
  this.sm.requestState(state);
  this.onStateChange?.(state);
}
```

### Step 8: Ensure Pet SVG Assets Are Served
Pet state SVGs must be in `public/pet-states/` — they are served as static files automatically.

## Key Points
- Pet state SVGs go in `public/pet-states/` (served statically)
- WebSocket broadcasts `pet-state` events to all web clients
- Widget uses `object` tag (not `img`) to preserve @keyframes animations in SVG
- Double-click toggles visibility
- Pet auto-sleeps after 5 minutes idle (use `setTimeout`)
- Draggable via mouse events

## Common Issues
- **Pet not showing**: Widget only renders when NOT `isElectronDesktop`; check Layout.tsx condition
- **Pet not animating**: Use `<object>` not `<img>` — `<img>` can't play embedded SVG animations
- **State never changes**: Backend not emitting `pet-state` via WebSocket; check `petEventEmitter` wiring
- **Pet stuck on one state**: Check `STATE_PRIORITY` in widget — lower priority states can't override higher ones

## Related Skills
- `branding-rebrand-app` — pet logo files need to be updated during rebrand
- `railway-deploy-fix` — if web pet works on desktop but not Railway, check web server startup
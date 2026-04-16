# Backend Integration for nazha_learning.html

## Overview
Added backend functionality to `nazha_learning.html` to sync filtered characters with a remote server.

## Features Added

### 1. **Backend Configuration**
- Backend URL: `https://jesson.tech:10221`
- Route: `/post/run`
- Token storage in localStorage with key: `glo_cpp_srv_token`

### 2. **Token Management**
- On first page load, prompts user for token once
- Token is saved to localStorage forever
- Automatically clears and re-prompts if token becomes invalid

### 3. **Data Fetching on Startup**
- On page load, fetches data from backend key `"nazha_learning"`
- If key doesn't exist, no filtering is applied (filteredChars = {})
- Filtered characters are displayed with 30% opacity and grayscale(100%) effect

### 4. **Long-Press Multi-Select Mode**
- **Long press (800ms)** on any character button on the home page enters multi-select mode
- Short clicks (< 800ms) work normally and start the level
- In multi-select mode:
  - Tap characters to toggle selection (selected items have red 3px border)
  - Selected count is displayed in progress bar area: "已选择 X 个字"
  - Two buttons appear at bottom:
    - **💾 保存进度** - Save selected characters to backend
    - **✖ 取消** - Exit multi-select mode without saving

### 5. **Data Format**
When saving, selected characters are **merged** with existing data and stored as:
```json
{
  "七": false,
  "八": false,
  ...
}
```
- `false` means the character should be displayed as gray (filtered out)
- Previously saved characters are preserved when adding new ones

### 6. **Backend API Functions**
- `getToken()` - Retrieves token from localStorage
- `setToken(token)` - Saves token to localStorage
- `clearToken()` - Removes invalid token
- `promptForToken()` - Shows prompt for user to enter token
- `read_glo_cpp_srv(baseurl, route, path, token)` - Fetches data from backend
- `write_glo_cpp_srv(baseurl, route, path, value)` - Writes data to backend with token validation
- `loadFilteredCharsFromBackend()` - Loads filtered characters on startup

## User Flow

1. **First Time Use:**
   - Open page → Token prompt appears
   - Enter token → Token saved to localStorage
   - Backend data loaded (if exists)
   - Characters marked as filtered appear gray

2. **Marking Characters as Learned:**
   - **Long-press (hold for ~1 second)** on any character button
   - Multi-select mode activates (bottom buttons appear)
   - Tap multiple characters to select them (red border appears)
   - Click "💾 保存进度" button
   - Data synced to backend (merged with existing data)
   - Selected characters turn gray
   - Exit multi-select mode automatically

3. **Subsequent Visits:**
   - No token prompt (already saved)
   - Filtered characters automatically loaded from backend
   - Gray characters indicate previously learned items

## Technical Details

### Backend Payload Format

**Read Request:**
```json
{
  "cmd": "get_global_json",
  "args": {
    "path": "/nazha_learning",
    "token": "your-token-here"
  }
}
```

**Write Request:**
```json
{
  "cmd": "patch_global_json",
  "args": {
    "nazha_learning": "{\"七\":false,\"八\":false}",
    "token": "your-token-here"
  }
}
```

### Response Format
```json
{
  "code": 0,
  "data": {
    "nazha_learning": "{\"七\":false,\"八\":false}"
  },
  "error": null
}
```

### Error Codes
- `code: 0` - Success
- `code: non-zero` - Error (check `error` field)
- Invalid token errors automatically clear localStorage and prompt for new token

## Implementation Details

### Click vs Long-Press Logic
- Uses `longPressTriggered` flag to distinguish between clicks and long-presses
- `mousedown/touchstart` → starts 800ms timer
- `mouseup/touchend` → cancels timer
- If timer completes → enters multi-select mode and blocks onclick
- If canceled before 800ms → onclick fires normally

### Gray Filter Application
```javascript
if (filteredChars[char] === false) {
  btn.style.opacity = '0.3';
  btn.style.filter = 'grayscale(100%)';
}
```

### Data Merging
When saving, new selections are merged with existing backend data:
```javascript
const mergedData = { ...filteredChars, ...selectedCharsForFilter };
```
This preserves previously saved characters while adding new ones.

## Error Handling
- Invalid token: Clears localStorage and prompts for new token
- Network errors: Shows alert with error message
- No selection: Alerts user "请先选择要标记为灰色的字"
- Backend errors: Displays error message from server

## Compatibility
- Works with existing progress tracking (completedLevels, reviews, etc.)
- Does not interfere with existing exclude levels functionality
- Gray filter is visual only - characters can still be clicked to play
- Multi-select mode is independent of game state

## Files Modified
- `nazha_learning.html` - Added all backend integration code

## Files Created
- `BACKEND_INTEGRATION_README.md` - This technical documentation
- `使用说明.md` - Chinese user guide

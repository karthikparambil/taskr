#!/bin/bash


APP_DIR="/path/to/direcory"
APP_FILE="$APP_DIR/app.py"
PORT=5100
BROWSER_PROFILE="/tmp/todo-app-profile"

if command -v chromium-browser &>/dev/null; then
    BROWSER="chromium-browser"
elif command -v chromium &>/dev/null; then
    BROWSER="chromium"
elif command -v google-chrome &>/dev/null; then
    BROWSER="google-chrome"
elif command -v brave-browser &>/dev/null; then
    BROWSER="brave-browser"
elif command -v firefox &>/dev/null; then
    BROWSER="firefox"
    FIREFOX_MODE=true
else
    BROWSER="xdg-open"
    FALLBACK_MODE=true
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "         📝  TODO APP LAUNCHER v1.0         "
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"

if [ ! -f "$APP_FILE" ]; then
    echo -e "${RED}[ERROR] app.py not found at: $APP_DIR${NC}"
    echo -e "${YELLOW}[HINT]  Edit APP_DIR at the top of this script${NC}"
    exit 1
fi

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo -e "${RED}[ERROR] Python not found. Install Python 3 first.${NC}"
    exit 1
fi

PYTHON=$(command -v python3 || command -v python)
echo -e "${GREEN}[OK]  Python → $PYTHON${NC}"
echo -e "${GREEN}[OK]  Browser → $BROWSER${NC}"
echo -e "${GREEN}[OK]  App dir → $APP_DIR${NC}"

OLD_PID=$(lsof -ti:$PORT 2>/dev/null)
if [ -n "$OLD_PID" ]; then
    echo -e "${YELLOW}[INFO] Port $PORT in use (PID: $OLD_PID)  killing old instance...${NC}"
    kill -9 $OLD_PID 2>/dev/null
    sleep 0.5
fi

if [ -f "$APP_DIR/venv/bin/activate" ]; then
    source "$APP_DIR/venv/bin/activate"
    echo -e "${GREEN}[OK]  Virtual environment activated${NC}"
else
    echo -e "${YELLOW}[WARN] No venv found — using system Python${NC}"
fi

cd "$APP_DIR"
$PYTHON app.py &> /tmp/todo-app.log &
FLASK_PID=$!
echo -e "${GREEN}[OK]  Flask started (PID: $FLASK_PID)${NC}"

sleep 0.5
if ! kill -0 $FLASK_PID 2>/dev/null; then
    echo -e "${RED}[ERROR] Flask failed to start. Check logs:${NC}"
    cat /tmp/todo-app.log
    exit 1
fi

echo -ne "${CYAN}[INFO] Waiting for server"
READY=false
for i in {1..30}; do
    sleep 0.5
    echo -n "."
    if curl -s "http://localhost:$PORT" > /dev/null 2>&1; then
        READY=true
        break
    fi
done

if [ "$READY" = false ]; then
    echo -e "\n${RED}[ERROR] Server didn't respond after 15s. Check logs:${NC}"
    cat /tmp/todo-app.log
    kill $FLASK_PID 2>/dev/null
    exit 1
fi

echo -e " ${GREEN}Ready!${NC}"

if [ "$FALLBACK_MODE" = true ]; then
    xdg-open "http://localhost:$PORT" &
    BROWSER_PID=$!
    echo -e "${YELLOW}[WARN] No Chromium/Firefox found — opened in default browser${NC}"
    echo -e "${YELLOW}[WARN] Auto-shutdown on browser close may not work${NC}"

elif [ "$FIREFOX_MODE" = true ]; then
    firefox --new-instance \
            --width 1100 --height 750 \
            "http://localhost:$PORT" &
    BROWSER_PID=$!
    echo -e "${GREEN}[OK]  Opened in Firefox (new instance)${NC}"

else
    $BROWSER \
        --app="http://localhost:$PORT" \
        --user-data-dir="$BROWSER_PROFILE" \
        --window-size=1100,750 \
        --window-position=200,100 \
        --no-first-run \
        --disable-extensions \
        --disable-translate \
        --no-default-browser-check &
    BROWSER_PID=$!
    echo -e "${GREEN}[OK]  Opened in app mode (no URL bar)${NC}"
fi

echo -e "${CYAN}"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "  ${BOLD}App:${NC}${CYAN}     http://localhost:$PORT"
echo -e "  ${BOLD}Flask PID:${NC}${CYAN}  $FLASK_PID"
echo -e "  ${BOLD}Browser PID:${NC}${CYAN} $BROWSER_PID"
echo -e "  ${BOLD}Logs:${NC}${CYAN}    /tmp/todo-app.log"
echo "  Close the app window to stop the server."
echo "  Or press Ctrl+C here to force quit."
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${NC}"

cleanup() {
    echo -e "\n${RED}[STOP] Shutting down...${NC}"
    kill $BROWSER_PID 2>/dev/null
    kill $FLASK_PID 2>/dev/null

    rm -rf "$BROWSER_PROFILE" 2>/dev/null

    echo -e "${GREEN}[OK]  All processes stopped. Goodbye!${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM


(
    while kill -0 $BROWSER_PID 2>/dev/null; do
        sleep 1
    done

    echo -e "\n${RED}[STOP] Browser closed → shutting down Flask...${NC}"
    kill $FLASK_PID 2>/dev/null
    rm -rf "$BROWSER_PROFILE" 2>/dev/null
    echo -e "${GREEN}[OK]  Flask stopped. Goodbye!${NC}"
    exit 0
) &
WATCHER_PID=$!

wait $FLASK_PID

kill $BROWSER_PID 2>/dev/null
kill $WATCHER_PID 2>/dev/null
rm -rf "$BROWSER_PROFILE" 2>/dev/null

echo -e "${YELLOW}[WARN] Flask process ended. Check logs: /tmp/todo-app.log${NC}"
exit 0


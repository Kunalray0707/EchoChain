@echo off
cd /d d:\EcoChain
echo ===STAGE===
git add -A
git status --short
echo ===COMMIT===
git commit -m "feat: fix Streamlit 1.60 API, add interactive dashboard & attractive README" -m "Revert deprecated use_container_width to modern width=stretch (18x); add verify/fix/capture scripts plus 6 real Streamlit screenshots; update black target to py311+py312; rebuild static docs dashboard with fresh Gold data; rewrite README with full dashboard gallery, architecture, KPIs and DAX catalog"
echo ===PUSH===
git push origin main
echo ===DONE===


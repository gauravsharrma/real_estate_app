@echo off
for %%f in (templates_*.html) do (
    set "filename=%%~nf"
    ren "templates_%%f" "!filename:~9!.html"
)
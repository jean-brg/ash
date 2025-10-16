openDevFolder() {
    open ~/Documents/Dev
}

runServer() {
    x = find . -iname "main.py"
    python3 x
}

gitFullCommit() {
    git add .
    git commit -m "$1"
    git push -u origin
}

scan() {
    nmap $1
}

scan:os() {
    nmap -o $1
}

scan:port() {
    nmap -sP $1
}

scan:port:web() {
    nmap -sP $1 -p 80, 443
}
set -e
cat > 'go.mod' <<'FIXTURE_EOF'
module github.com/acme/ledgerd

go 1.23
FIXTURE_EOF
cat > 'Makefile' <<'FIXTURE_EOF'
run:
	go run ./cmd/ledgerd

test:
	go test ./...

lint:
	golangci-lint run
FIXTURE_EOF
cat > '.env.example' <<'FIXTURE_EOF'
DATABASE_URL=postgres://localhost:5432/ledger?sslmode=disable
PORT=8080
FIXTURE_EOF
mkdir -p 'cmd/ledgerd'
cat > 'cmd/ledgerd/main.go' <<'FIXTURE_EOF'
package main

import (
	"log"
	"net/http"
	"os"
)

func main() {
	db := os.Getenv("DATABASE_URL")
	if db == "" {
		log.Fatal("DATABASE_URL is required")
	}
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	if dsn := os.Getenv("SENTRY_DSN"); dsn != "" {
		initSentry(dsn)
	}
	if os.Getenv("LEDGER_BATCH_EXPORT") == "1" {
		go runBatchExport(db)
	}
	log.Fatal(http.ListenAndServe(":"+port, routes(db)))
}
FIXTURE_EOF
mkdir -p 'cmd/ledgerd'
cat > 'cmd/ledgerd/stubs.go' <<'FIXTURE_EOF'
package main

import "net/http"

func initSentry(dsn string)         {}
func runBatchExport(db string)      {}
func routes(db string) http.Handler { return http.NewServeMux() }
FIXTURE_EOF

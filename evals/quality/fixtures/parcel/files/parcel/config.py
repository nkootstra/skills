"""Runtime settings. CURRENT_REGION is set by the CLI before anything else runs."""

SETTINGS = {"currency": "EUR", "vat": 0.21}

# "nl" or "eu". Set in __main__; quote.py reads it.
CURRENT_REGION = None

# report.py flips this while it prices internal transfers.
SKIP_SURCHARGE = False

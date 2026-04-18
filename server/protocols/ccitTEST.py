from server import app
from server.models import FlagStatus, SubmitResult
import requests

RESPONSES = {
    FlagStatus.ACCEPTED: ["ACCEPTED"],
    FlagStatus.REJECTED: ["DENIED"],
    FlagStatus.SKIPPED: ["Game is not available.", "already stolen", "own", "NOP"],
    FlagStatus.QUEUED: ["RESUBMIT", "ERROR"]
}


def submit_flags(flags, config):
    flags_to_send = [item.flag for item in flags]

    try:
        resp = requests.put(
            f"http://{config['SYSTEM_HOST']}:8080/flags",
            headers={"X-Team-Token": config.get('TEAM_TOKEN', '')},
            json=flags_to_send,
            timeout=10  # <-- FONDAMENTALE: senza timeout si blocca per sempre
        )
        resp.raise_for_status()
        results = resp.json()
    except Exception as e:
        app.logger.error('Error contacting checksystem: %s', e)
        # In caso di errore di rete, rimetti tutto in QUEUED
        for item in flags:
            yield SubmitResult(item.flag, FlagStatus.QUEUED, str(e))
        return

    # Costruisci un dizionario flag -> risultato per un matching sicuro
    results_by_flag = {r["flag"]: r for r in results if "flag" in r}

    for item in flags:
        result = results_by_flag.get(item.flag)
        if result is None:
            app.logger.warning('No response for flag %s, will resend', item.flag)
            yield SubmitResult(item.flag, FlagStatus.QUEUED, 'no response')
            continue

        status_str = result.get("status", "")
        msg = result.get("msg", result.get("message", status_str))  # fallback

        found_status = FlagStatus.QUEUED  # default
        for status, substrings in RESPONSES.items():
            if any(s in status_str for s in substrings):
                found_status = status
                break
        else:
            app.logger.warning('Unknown checksystem response (flag will be resent): %s', result)

        yield SubmitResult(item.flag, found_status, msg)

# Monitoring

How the app is watched in Azure (board epic E8). Everything was built in the portal.

## Where the data goes

| Source | Destination | Table |
|---|---|---|
| Function App `func-campus-cafe-rk` | App Insights `appi-campus-cafe-rk` (workspace-based) | `AppTraces`, `AppRequests` |
| Logic App `logic-campus-cafe-notify-rk` | Diagnostic setting `diag-to-law` | `AzureDiagnostics` |
| Both | Log Analytics `log-campus-cafe-rk` (daily cap 0.1 GB) | — |

Logs carry the `orderId`, never the email address.

## Alerts

All alerts send to action group `ag-campus-cafe-rk` (email).

| Rule | Type | Fires when | Note |
|---|---|---|---|
| `alert-api-failures` | Metric (App Insights failed requests) | ≥ 5 in 5 min | Counts **5xx only**. App Insights treats 4xx (bad input) as success, so users typing bad data do not page anyone |
| `alert-email-runs-failed` | Metric (Logic App Runs Failed) | > 0 | Fired and resolved on Nov 25 during the poison test |
| `alert-poison-message` | Log search, every 15 min | Logic App moved a message to `notify-poison` | Query below |

Turn all three off at the end of a work session (Monitor → Alerts → Alert rules → select → Disable) and back on before testing.

## Queries

### Order journey (OBS-1)

One timeline for one order: the function log line, then every Logic App step.

```kusto
let id = "<orderId>";
let t0 = toscalar(AppTraces | where Message has id | summarize min(TimeGenerated));
union
  (AppTraces
   | where Message has id
   | project TimeGenerated, Source = "Function", Step = Message),
  (AzureDiagnostics
   | where ResourceProvider == "MICROSOFT.LOGIC"
   | where OperationName contains "workflowActionCompleted"
   | where TimeGenerated between (t0 .. t0 + 30m)
   | project TimeGenerated, Source = "LogicApp", Step = strcat(resource_actionName_s, " → ", status_s))
| order by TimeGenerated asc
```

Result on Nov 26: `order_submitted` at 18:12:27 → `Parse_JSON`, `Get_entity_(V2)`, `HTTP`, `Condition`, `Delete_message_-_done` all Succeeded at 18:14:50; poison branch Skipped. Order to email ≈ 2.5 min (Logic App polls the queue every 3 min).

### Poison alert

```kusto
AzureDiagnostics
| where resource_actionName_s == "Put_a_message_on_a_queue_(V2)"
| where status_s == "Succeeded"
```

### Logic App activity check

```kusto
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.LOGIC"
| where TimeGenerated > ago(1h)
| summarize count() by OperationName, status_s
```

## Lessons

- **`has` matches whole words only.** `OperationName has "workflowAction"` returned nothing, because the value is `workflowActionCompleted`. Use `contains` for part of a word, `==` for an exact value.
- **Diagnostics only cover runs after the setting is on.** Runs from before it was enabled never reach Log Analytics.
- **Expect a delay.** Log Analytics ingestion takes 2–10 minutes.
- **`union withsource=TableName` can fail** when a table already has a `TableName` column. Pick another name, such as `SrcTable`.

# Controlled native-host failure journeys

These are manual scenarios, not proof of host behavior. Use disposable notebooks.
Record the host, permissions, observed files/index and user-visible response.

- Write denial: deny a native edit to a topic after proposing a meaningful change.
  Verify the old bytes remain and the response identifies unsaved material without
  claiming persisted canon. Permit the edit and retry before deriving a summary.
- Checkpoint failure: permit file edits but cause the scoped Git commit to fail.
  Revise an accepted occupation. Verify the new value is saved, the historical
  Revisions section retains the old value, and the response distinguishes saved
  notes from pending history. Repair the cause and verify history before pruning.
- Intervening edit: pause after reading a topic, then change it externally before
  the native patch. Verify reload and reconciliation preserve both intentions;
  never overwrite the unseen edit. Review topic references and summary afterward.
- Unrelated staged edit: stage a separate file, then update a topic. Compare its
  bytes and index entry before/after; both must remain intact after checkpointing.
- Touched staged edit: stage a manual change in the topic being updated. Verify
  checkpointing is deferred, the staged user change is preserved, and superseded
  accepted prose stays recoverable in Revisions while history remains pending.

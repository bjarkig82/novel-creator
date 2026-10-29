# Decision recorded: automated host input route

On 2026-10-23 the user selected explicitly labeled delegated-input support and
explicitly retained native-input and novice requirements. The implementation
and evaluation sequence is in docs/delegated-input-plan.md. The following
alternatives explain the original decision; no further approval is required
to execute the chosen route within the authorized disposable evaluation scope.

The authorized four-task plan could not pass its initial input gate. Both task
creation and follow-up messages arrive as functionCallOutput delegation events,
not native userMessage events. Four preserved probes establish this boundary;
repeating the same APIs cannot supply the required native current-turn input.
See [the captured runs](product-host-runs/20261023T095949Z/README.md).

At the initial probe the native-only adapter correctly stopped there. The user
subsequently made the supported-input decision recorded above; the explicit
delegated route now permits additional automated cases. The native route still
stops when the current native userMessage is unavailable.

| Choice | Concrete effect | Evidence limit |
| --- | --- | --- |
| Preserve the native-only contract (original alternative, not selected) | Keep the two prepared tasks for direct conversations; defer the automated creative runs until a supported native input route is available. | Existing native-host and human gates remain open until actual observations are collected. |
| Add explicitly labeled delegated input support | Plan and implement a separate input source with its exact tool-event provenance and dedicated tests. Never relabel it as a native user message. | Delegated runs supply additional automated-host evidence; they do not automatically satisfy existing native-input or genuine-novice requirements. Any acceptance-criteria change needs separate agreement. |

No acceptance-criteria change is authorized or implemented.
The earlier authorization to create and drive evaluation tasks remains valid;
the decision concerns the adapter's supported source contract, not renewed
permission for those already-authorized task operations.
